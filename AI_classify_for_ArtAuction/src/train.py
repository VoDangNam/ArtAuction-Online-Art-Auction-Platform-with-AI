import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from model import get_model
from dataset import get_dataloaders
from focal_loss import FocalLoss
from tqdm import tqdm

def train(data_dir="./data", out_dir="./outputs", epochs=50, patience=10,
          lr=1e-4, batch_size=32, num_workers=4, resume=None, resume_from="last", 
          weight_decay=1e-3, dropout_rate=0.2, cleanup_report=True):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)
    print("=== TRAINING CONFIGURATION ===")
    print(f"Epochs: {epochs}, Patience: {patience}")
    print(f"Learning Rate: {lr:.2e}, Batch Size: {batch_size}")
    print(f"Weight Decay: {weight_decay:.2e}, Dropout Rate: {dropout_rate}")
    print(f"Resume From: {resume_from}")
    print("===============================")

    os.makedirs(out_dir + "/checkpoints", exist_ok=True)
    os.makedirs(out_dir + "/epoch_checkpoints", exist_ok=True)
    writer = SummaryWriter(log_dir=out_dir + "/logs")

    train_loader, val_loader, classes = get_dataloaders(
        data_dir, 
        batch_size=batch_size, 
        num_workers=num_workers,
        use_report_data=True,  # Merge report data vào training
        report_weight=3.0  # Report images có weight cao gấp 3 lần
    )
    model = get_model("convnext_tiny", num_classes=len(classes), dropout_rate=dropout_rate).to(device)

    # Sử dụng Focal Loss thay vì CrossEntropyLoss thông thường
    # Focal Loss giúp model học kỹ hơn từ những ảnh khó (bị dán nhãn sai)
    criterion = FocalLoss(alpha=None, gamma=2.0, reduction='mean')
    print("✓ Using Focal Loss (gamma=2.0) to focus on hard examples")
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    
    # Learning rate scheduler tối ưu
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.3, patience=5, 
        min_lr=1e-7
    )
    
    # Gradient clipping để tránh gradient explosion
    max_grad_norm = 1.0

    best_acc = 0.0
    best_epoch = -1
    # Track best since improvement window (epoch >= 14 => index 13)
    best2_acc = None
    best2_epoch = None
    epochs_no_improve = 0
    start_epoch = 0

    # Probe available checkpoints for logging
    ckpt_dir = os.path.join(out_dir, "checkpoints")
    last_path = os.path.join(ckpt_dir, "last.pth")
    best_path = os.path.join(ckpt_dir, "best_model.pth")
    best2_path = os.path.join(ckpt_dir, "best_model2.pth")
    last_probe = None
    best_probe = None
    best2_probe = None
    if os.path.exists(last_path):
        try:
            last_probe = torch.load(last_path, map_location="cpu")
        except Exception:
            last_probe = None
    if os.path.exists(best_path):
        try:
            best_probe = torch.load(best_path, map_location="cpu")
        except Exception:
            best_probe = None
    if os.path.exists(best2_path):
        try:
            best2_probe = torch.load(best2_path, map_location="cpu")
        except Exception:
            best2_probe = None

    if best_probe is not None:
        print("Found best checkpoint:", {
            "best_epoch_1based": (best_probe.get("best_epoch", best_probe.get("epoch", -1)) + 1),
            "stored_epoch_index0": best_probe.get("epoch", -1),
            "best_acc": round(float(best_probe.get("best_acc", 0.0)), 6)
        })
    if best2_probe is not None:
        print("Found best2 checkpoint:", {
            "best_epoch_1based": (best2_probe.get("best_epoch", best2_probe.get("epoch", -1)) + 1),
            "stored_epoch_index0": best2_probe.get("epoch", -1),
            "best_acc": round(float(best2_probe.get("best_acc", 0.0)), 6)
        })
    if last_probe is not None:
        print("Found last checkpoint:", {
            "last_epoch_1based": (last_probe.get("epoch", -1) + 1),
            "stored_epoch_index0": last_probe.get("epoch", -1),
            "best_acc": round(float(last_probe.get("best_acc", 0.0)), 6),
            "best_epoch_1based": (last_probe.get("best_epoch", -1) + 1)
        })

    # Decide resume source
    chosen_resume = None
    if resume:
        chosen_resume = resume
    else:
        if resume_from == "last":
            if os.path.exists(last_path):
                chosen_resume = last_path
            elif os.path.exists(best_path):
                # fallback: if last missing, start from best to continue
                chosen_resume = best_path
        elif resume_from == "best" and os.path.exists(best_path):
            chosen_resume = best_path

    # resume training
    if chosen_resume:
        ckpt = torch.load(chosen_resume, map_location=device)
        
        # Thử load full model state trước (nếu architecture giống nhau)
        model_state = ckpt["model_state"]
        architecture_changed = False
        
        try:
            # Thử load full model với strict=True
            model.load_state_dict(model_state, strict=True)
            print("✓ Full model state loaded successfully (architecture matches)")
        except RuntimeError as e:
            # Nếu fail, có nghĩa là architecture khác → chỉ load backbone
            print(f"⚠️  Full model load failed: {str(e).splitlines()[0]}")
            print("⚠️  Model architecture changed, loading backbone only...")
            architecture_changed = True
            
            # Load only backbone (features), skip classifier
            backbone_state = {k: v for k, v in model_state.items() if not k.startswith('classifier')}
            missing, unexpected = model.load_state_dict(backbone_state, strict=False)
            
            if missing:
                missing_important = [k for k in missing if not k.startswith("classifier")]
                if missing_important:
                    print(f"  ⚠️  Missing backbone keys: {missing_important[:3]}...")
            if unexpected:
                print(f"  ⚠️  Unexpected keys ignored: {unexpected[:3]}...")
            
            print("✓ Backbone loaded, classifier will be trained from scratch")
        
        # Load optimizer state - chỉ khi architecture giống nhau
        if not architecture_changed:
            if "optim_state" in ckpt:
                try:
                    optimizer.load_state_dict(ckpt["optim_state"])
                    print("✓ Optimizer state loaded successfully")
                except Exception as e:
                    print(f"⚠️  Optimizer state incompatible: {e}")
                    print("  Starting fresh optimizer state")
            else:
                print("⚠️  No optimizer state in checkpoint, starting fresh")
        else:
            print("⚠️  Optimizer state incompatible due to architecture change, starting fresh")
            # Don't load optimizer state when classifier architecture changes
        
        # Load scheduler state
        if "scheduler_state" in ckpt:
            try:
                scheduler.load_state_dict(ckpt["scheduler_state"])
                print("✓ Scheduler state loaded successfully")
            except Exception as e:
                print(f"⚠️  Scheduler state incompatible: {e}, starting fresh")
        else:
            print("⚠️  No scheduler state in checkpoint, starting fresh")
        
        start_epoch = ckpt["epoch"] + 1
        best_acc = ckpt.get("best_acc", best_acc)
        best_epoch = ckpt.get("best_epoch", best_epoch)
        epochs_no_improve = ckpt.get("epochs_no_improve", epochs_no_improve)
        # Restore best2 tracking if available (safe default: None)
        best2_acc = ckpt.get("best2_acc", best2_acc)
        best2_epoch = ckpt.get("best2_epoch", best2_epoch)
        # display 1-based indices for readability
        print(f"Resumed from {chosen_resume}, starting_epoch={start_epoch+1}, best_epoch={(best_epoch+1) if best_epoch>=0 else 'N/A'}, best_acc={best_acc:.4f}")

    # Track if we've cleaned up report images
    report_cleaned_up = False
    
    for epoch in range(start_epoch, epochs):
        print(f"Epoch {epoch+1}/{epochs}")

        # Cleanup report images sau epochs đầu (để model học kỹ nhưng không overfit)
        if epoch == 4 and not report_cleaned_up and cleanup_report:  # Sau epoch 5
            print(f"\n✓ Cleaning up report images after epoch {epoch+1}")
            try:
                from cleanup_report_after_training import cleanup_report_images
                moved_count = cleanup_report_images(data_dir)
                if moved_count > 0:
                    print(f"  Moved {moved_count} report images to training data")
                    report_cleaned_up = True
                    
                    # Reload dataset (không có report images nữa)
                    train_loader, val_loader, classes = get_dataloaders(
                        data_dir,
                        batch_size=batch_size,
                        num_workers=num_workers,
                        use_report_data=True,  # Vẫn check nhưng folder trống rồi
                        report_weight=3.0
                    )
                    print(f"  Reloaded dataset (report images now in train/, weight=1.0)")
            except Exception as e:
                print(f"⚠️  Cleanup failed: {e}")

        # train
        model.train()
        train_loss, correct, total = 0.0, 0, 0
        for x,y in tqdm(train_loader, desc="Training"):
            x,y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out,y)
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()

            train_loss += loss.item()*x.size(0)
            _,pred = out.max(1)
            correct += pred.eq(y).sum().item()
            total += y.size(0)

        train_acc = correct/total
        train_loss = train_loss/total

        # validate
        model.eval()
        val_loss, correct, total = 0.0, 0, 0
        with torch.no_grad():
            for x,y in tqdm(val_loader, desc="Validation"):
                x,y = x.to(device), y.to(device)
                out = model(x)
                loss = criterion(out,y)
                val_loss += loss.item()*x.size(0)
                _,pred = out.max(1)
                correct += pred.eq(y).sum().item()
                total += y.size(0)
        val_acc = correct/total
        val_loss = val_loss/total

        print(f"Train loss: {train_loss:.4f} acc: {train_acc:.4f}")
        print(f"Val loss: {val_loss:.4f} acc: {val_acc:.4f}")
        print(f"Learning rate: {optimizer.param_groups[0]['lr']:.2e}")

        writer.add_scalar("Loss/train", train_loss, epoch)
        writer.add_scalar("Loss/val", val_loss, epoch)
        writer.add_scalar("Acc/train", train_acc, epoch)
        writer.add_scalar("Acc/val", val_acc, epoch)
        writer.add_scalar("Learning_Rate", optimizer.param_groups[0]['lr'], epoch)
        
        # Update learning rate với warmup
        old_lr = optimizer.param_groups[0]['lr']
        scheduler.step(val_acc)
        new_lr = optimizer.param_groups[0]['lr']
        
        # Thông báo khi learning rate thay đổi
        if new_lr != old_lr:
            print(f"Learning rate reduced: {old_lr:.2e} → {new_lr:.2e}")
            
        # Log gradient norm để theo dõi
        total_norm = 0
        for p in model.parameters():
            if p.grad is not None:
                param_norm = p.grad.data.norm(2)
                total_norm += param_norm.item() ** 2
        total_norm = total_norm ** (1. / 2)
        writer.add_scalar("Gradient_Norm", total_norm, epoch)

        # save best overall (tạo best_overall.pth mới, không động tới best_model.pth và best_model2.pth)
        if val_acc > best_acc:
            best_acc = val_acc
            best_epoch = epoch
            torch.save({
                "epoch": epoch,
                "model_state": model.state_dict(),
                "optim_state": optimizer.state_dict(),
                "scheduler_state": scheduler.state_dict(),
                "best_acc": best_acc,
                "best_epoch": best_epoch,
                "best2_acc": best2_acc,
                "best2_epoch": best2_epoch,
                "epochs_no_improve": 0
            }, f"{out_dir}/checkpoints/best_model3.pth")
            print("Saved improved model (best_model3) at epoch", epoch+1)
            epochs_no_improve = 0
        
        # save best since improvement window start (epoch >= 14) - giữ nguyên best_model2.pth
        if epoch >= 13:  # index-0 epoch 13 == epoch 14 human-readable
            if (best2_acc is None) or (val_acc > best2_acc):
                best2_acc = val_acc
                best2_epoch = epoch
                torch.save({
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "optim_state": optimizer.state_dict(),
                    "scheduler_state": scheduler.state_dict(),
                    "best_acc": best_acc,
                    "best_epoch": best_epoch,
                    "best2_acc": best2_acc,
                    "best2_epoch": best2_epoch,
                    "epochs_no_improve": epochs_no_improve
                }, f"{out_dir}/checkpoints/best_model2.pth")
                print("Saved best_model2 (since epoch 14 window) at epoch", epoch+1)
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                print("Early stopping triggered.")
                # save last state before stopping
                torch.save({
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "optim_state": optimizer.state_dict(),
                    "scheduler_state": scheduler.state_dict(),
                    "best_acc": best_acc,
                    "best_epoch": best_epoch,
                    "best2_acc": best2_acc,
                    "best2_epoch": best2_epoch,
                    "epochs_no_improve": epochs_no_improve
                }, f"{out_dir}/checkpoints/last.pth")
                
                # save final epoch checkpoint
                torch.save({
                    "epoch": epoch,
                    "model_state": model.state_dict(),
                    "optim_state": optimizer.state_dict(),
                    "scheduler_state": scheduler.state_dict(),
                    "best_acc": best_acc,
                    "best_epoch": best_epoch,
                    "best2_acc": best2_acc,
                    "best2_epoch": best2_epoch,
                    "epochs_no_improve": epochs_no_improve,
                    "train_acc": train_acc,
                    "train_loss": train_loss,
                    "val_acc": val_acc,
                    "val_loss": val_loss,
                    "early_stopped": True
                }, f"{out_dir}/epoch_checkpoints/epoch_{epoch+1}.pth")
                print(f"✓ Saved final epoch checkpoint (early stopped): epoch_{epoch+1}.pth")
                break

        # save last checkpoint (progress checkpoint) after updating best/patience counters
        torch.save({
            "epoch": epoch,
            "model_state": model.state_dict(),
            "optim_state": optimizer.state_dict(),
            "scheduler_state": scheduler.state_dict(),
            "best_acc": best_acc,
            "best_epoch": best_epoch,
            "best2_acc": best2_acc,
            "best2_epoch": best2_epoch,
            "epochs_no_improve": epochs_no_improve
        }, f"{out_dir}/checkpoints/last.pth")
        
        # save epoch checkpoint for each epoch
        torch.save({
            "epoch": epoch,
            "model_state": model.state_dict(),
            "optim_state": optimizer.state_dict(),
            "scheduler_state": scheduler.state_dict(),
            "best_acc": best_acc,
            "best_epoch": best_epoch,
            "best2_acc": best2_acc,
            "best2_epoch": best2_epoch,
            "epochs_no_improve": epochs_no_improve,
            "train_acc": train_acc,
            "train_loss": train_loss,
            "val_acc": val_acc,
            "val_loss": val_loss
        }, f"{out_dir}/epoch_checkpoints/epoch_{epoch+1}.pth")
        print(f"✓ Saved epoch checkpoint: epoch_{epoch+1}.pth")
    
    # Cleanup report images sau khi training xong (nếu chưa cleanup giữa chừng)
    if cleanup_report and not report_cleaned_up:
        print("\n" + "=" * 60)
        print("CLEANUP REPORT IMAGES")
        print("=" * 60)
        try:
            from cleanup_report_after_training import cleanup_report_images
            moved_count = cleanup_report_images(data_dir)
            if moved_count > 0:
                print(f"✓ Training complete! {moved_count} report images moved to training data.")
                print("  These images will now be part of normal training in future runs.")
            else:
                print("✓ No report images to cleanup.")
        except Exception as e:
            print(f"⚠️  Cleanup failed: {e}")
            print("  You can manually run: python src/cleanup_report_after_training.py")
    elif report_cleaned_up:
        print("\n✓ Report images already cleaned up during training.")
    
    print("\n✓ Training finished!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="./data")
    parser.add_argument("--out_dir", type=str, default="./outputs")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--patience", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--weight_decay", type=float, default=1e-3)
    parser.add_argument("--dropout_rate", type=float, default=0.2)
    parser.add_argument("--resume", type=str, default=None)
    parser.add_argument("--resume_from", type=str, choices=["last","best","none"], default="last")
    parser.add_argument("--no_cleanup_report", action="store_true", help="Don't move report images to train after training")
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
        resume_from=args.resume_from,
        cleanup_report=not args.no_cleanup_report,
    )
