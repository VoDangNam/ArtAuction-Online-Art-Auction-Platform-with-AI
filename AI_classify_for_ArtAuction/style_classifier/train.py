import argparse
import os
from typing import Optional

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from dataset import get_dataloaders
from model import get_model


class FocalLoss(nn.Module):
    def __init__(self, gamma: float = 2.0, alpha: Optional[torch.Tensor] = None, reduction: str = "mean"):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = reduction
        self.ce = nn.CrossEntropyLoss(reduction="none")

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        ce_loss = self.ce(inputs, targets)
        pt = torch.exp(-ce_loss)
        focal_term = (1 - pt) ** self.gamma

        if self.alpha is not None:
            alpha_t = self.alpha.gather(0, targets)
            focal_term = focal_term * alpha_t

        loss = focal_term * ce_loss
        if self.reduction == "mean":
            return loss.mean()
        if self.reduction == "sum":
            return loss.sum()
        return loss


def _save_checkpoint(path: str, *, epoch: int, model: nn.Module, optimizer: optim.Optimizer,
                     scheduler: optim.lr_scheduler.ReduceLROnPlateau, best_acc: float, best_epoch: int,
                     epochs_no_improve: int) -> None:
    torch.save(
        {
            "epoch": epoch,
            "model_state": model.state_dict(),
            "optim_state": optimizer.state_dict(),
            "scheduler_state": scheduler.state_dict(),
            "best_acc": best_acc,
            "best_epoch": best_epoch,
            "epochs_no_improve": epochs_no_improve,
        },
        path,
    )


def train(
    data_dir: str = "./style_data",
    out_dir: str = "./style_outputs",
    epochs: int = 50,
    patience: int = 10,
    lr: float = 1e-4,
    batch_size: int = 32,
    num_workers: int = 4,
    weight_decay: float = 1e-3,
    dropout_rate: float = 0.2,
    resume: Optional[str] = None,
    resume_from: str = "last",
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)
    print("=== ART STYLE TRAINING CONFIGURATION ===")
    print(f"Epochs: {epochs}, Patience: {patience}")
    print(f"Learning Rate: {lr:.2e}, Batch Size: {batch_size}")
    print(f"Weight Decay: {weight_decay:.2e}, Dropout Rate: {dropout_rate}")
    print(f"Resume From: {resume_from}")
    print("========================================")

    ckpt_dir = os.path.join(out_dir, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "logs"), exist_ok=True)
    writer = SummaryWriter(log_dir=os.path.join(out_dir, "logs"))

    train_loader, val_loader, classes = get_dataloaders(
        data_dir=data_dir,
        batch_size=batch_size,
        num_workers=num_workers,
        img_size=224,
        val_center_crop=True,
        balance_classes=True,
    )

    print(f"[INFO] Loaded {len(classes)} art styles: {classes}")

    model = get_model("convnext_tiny", num_classes=len(classes), dropout_rate=dropout_rate).to(device)
    criterion = FocalLoss(gamma=2.0)
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.3, patience=5, min_lr=1e-7)
    max_grad_norm = 1.0

    best_acc = 0.0
    best_epoch = -1
    epochs_no_improve = 0
    start_epoch = 0

    last_path = os.path.join(ckpt_dir, "last.pth")
    best_path = os.path.join(ckpt_dir, "best_model.pth")

    chosen_resume = None
    if resume:
        chosen_resume = resume
    else:
        if resume_from == "last" and os.path.exists(last_path):
            chosen_resume = last_path
        elif resume_from == "best" and os.path.exists(best_path):
            chosen_resume = best_path

    if chosen_resume:
        print(f"[INFO] Resuming from checkpoint: {chosen_resume}")
        ckpt = torch.load(chosen_resume, map_location=device)
        model_state = ckpt.get("model_state", ckpt)
        architecture_changed = False
        try:
            model.load_state_dict(model_state, strict=True)
            print("[OK] Loaded full model state.")
        except RuntimeError as exc:
            print(f"[WARN] Full load failed: {exc}. Loading backbone only.")
            architecture_changed = True
            backbone_state = {k: v for k, v in model_state.items() if not k.startswith("classifier")}
            model.load_state_dict(backbone_state, strict=False)

        if not architecture_changed and "optim_state" in ckpt:
            try:
                optimizer.load_state_dict(ckpt["optim_state"])
                print("[OK] Optimizer state loaded.")
            except Exception as exc:
                print("[WARN] Optimizer state incompatible:", exc)

        if "scheduler_state" in ckpt:
            try:
                scheduler.load_state_dict(ckpt["scheduler_state"])
            except Exception as exc:
                print("[WARN] Scheduler state incompatible:", exc)

        start_epoch = ckpt.get("epoch", -1) + 1
        best_acc = ckpt.get("best_acc", best_acc)
        best_epoch = ckpt.get("best_epoch", best_epoch)
        epochs_no_improve = ckpt.get("epochs_no_improve", epochs_no_improve)
        print(f"[INFO] Resume summary -> start_epoch: {start_epoch + 1}, best_epoch: {best_epoch + 1}, best_acc: {best_acc:.4f}")

    for epoch in range(start_epoch, epochs):
        print(f"\nEpoch {epoch + 1}/{epochs}")
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        for x, y in tqdm(train_loader, desc="Training"):
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()

            train_loss += loss.item() * x.size(0)
            _, pred = logits.max(1)
            train_correct += pred.eq(y).sum().item()
            train_total += y.size(0)

        train_loss /= max(train_total, 1)
        train_acc = train_correct / max(train_total, 1)

        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for x, y in tqdm(val_loader, desc="Validation"):
                x, y = x.to(device), y.to(device)
                logits = model(x)
                loss = criterion(logits, y)
                val_loss += loss.item() * x.size(0)
                _, pred = logits.max(1)
                val_correct += pred.eq(y).sum().item()
                val_total += y.size(0)

        val_loss /= max(val_total, 1)
        val_acc = val_correct / max(val_total, 1)

        print(f"Train loss: {train_loss:.4f} | Train acc: {train_acc:.4f}")
        print(f"Val   loss: {val_loss:.4f} | Val   acc: {val_acc:.4f}")
        print(f"LR: {optimizer.param_groups[0]['lr']:.2e}")

        writer.add_scalar("loss/train", train_loss, epoch)
        writer.add_scalar("loss/val", val_loss, epoch)
        writer.add_scalar("acc/train", train_acc, epoch)
        writer.add_scalar("acc/val", val_acc, epoch)
        writer.add_scalar("lr", optimizer.param_groups[0]["lr"], epoch)

        prev_lr = optimizer.param_groups[0]["lr"]
        scheduler.step(val_acc)
        if optimizer.param_groups[0]["lr"] != prev_lr:
            print(f"[INFO] LR reduced {prev_lr:.2e} -> {optimizer.param_groups[0]['lr']:.2e}")

        grad_norm = 0.0
        for p in model.parameters():
            if p.grad is not None:
                grad_norm += p.grad.data.norm(2).item() ** 2
        writer.add_scalar("grad_norm", grad_norm ** 0.5, epoch)

        if val_acc > best_acc:
            best_acc = val_acc
            best_epoch = epoch
            _save_checkpoint(
                best_path,
                epoch=epoch,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                best_acc=best_acc,
                best_epoch=best_epoch,
                epochs_no_improve=0,
            )
            print(f"[INFO] Saved new best model at epoch {epoch + 1} with acc {best_acc:.4f}")
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        _save_checkpoint(
            last_path,
            epoch=epoch,
            model=model,
            optimizer=optimizer,
            scheduler=scheduler,
            best_acc=best_acc,
            best_epoch=best_epoch,
            epochs_no_improve=epochs_no_improve,
        )

        if epochs_no_improve >= patience:
            print("[INFO] Early stopping triggered.")
            break

    print("\nTraining finished.")
    print(f"Best validation accuracy: {best_acc:.4f} at epoch {best_epoch + 1}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ConvNeXt-Tiny Art Style Classifier")
    parser.add_argument("--data_dir", type=str, default="./style_data")
    parser.add_argument("--out_dir", type=str, default="./style_outputs")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--patience", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--weight_decay", type=float, default=1e-3)
    parser.add_argument("--dropout_rate", type=float, default=0.2)
    parser.add_argument("--resume", type=str, default=None)
    parser.add_argument("--resume_from", type=str, choices=["last", "best", "none"], default="last")
    args = parser.parse_args()

    train(
        data_dir=args.data_dir,
        out_dir=args.out_dir,
        epochs=args.epochs,
        patience=args.patience,
        lr=args.lr,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        weight_decay=args.weight_decay,
        dropout_rate=args.dropout_rate,
        resume=args.resume,
        resume_from=None if args.resume_from == "none" else args.resume_from,
    )


