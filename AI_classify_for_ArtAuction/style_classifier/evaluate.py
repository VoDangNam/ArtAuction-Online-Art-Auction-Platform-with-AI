import argparse
import torch
import torch.nn as nn
from tqdm import tqdm

from dataset import get_dataloaders
from model import get_model


def load_checkpoint(model: nn.Module, path: str, device: torch.device) -> None:
    ckpt = torch.load(path, map_location=device)
    state = ckpt.get("model_state", ckpt)
    try:
        model.load_state_dict(state, strict=True)
        print("[OK] Loaded full checkpoint.")
    except RuntimeError as exc:
        print("[WARN] Full load failed:", exc)
        backbone_state = {k: v for k, v in state.items() if not k.startswith("classifier")}
        model.load_state_dict(backbone_state, strict=False)
        print("[OK] Backbone weights restored; classifier left as initialized.")


def evaluate(
    checkpoint: str = "./style_outputs/checkpoints/best_model.pth",
    data_dir: str = "./style_data",
    batch_size: int = 32,
    img_size: int = 224,
) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    _, val_loader, classes = get_dataloaders(
        data_dir=data_dir,
        img_size=img_size,
        batch_size=batch_size,
        num_workers=4,
        val_center_crop=True,
        balance_classes=False,
    )

    model = get_model("convnext_tiny", num_classes=len(classes)).to(device)
    print(f"[INFO] Evaluating {len(classes)} classes using checkpoint: {checkpoint}")
    load_checkpoint(model, checkpoint, device)
    model.eval()

    criterion = nn.CrossEntropyLoss()
    val_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for x, y in tqdm(val_loader, desc="Evaluating"):
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = criterion(logits, y)
            val_loss += loss.item() * x.size(0)
            _, pred = logits.max(1)
            val_correct += pred.eq(y).sum().item()
            val_total += y.size(0)

    accuracy = val_correct / max(val_total, 1)
    avg_loss = val_loss / max(val_total, 1)
    print(f"Validation accuracy: {accuracy * 100:.2f}%")
    print(f"Validation loss: {avg_loss:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate art style classifier")
    parser.add_argument("--data_dir", type=str, default="./style_data")
    parser.add_argument("--checkpoint", type=str, default="./style_outputs/checkpoints/best_model.pth")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--img_size", type=int, default=224)
    args = parser.parse_args()

    evaluate(
        checkpoint=args.checkpoint,
        data_dir=args.data_dir,
        batch_size=args.batch_size,
        img_size=args.img_size,
    )


