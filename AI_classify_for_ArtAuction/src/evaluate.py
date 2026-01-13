import argparse
import torch
import torch.nn as nn
from dataset import get_dataloaders
from model import get_model
from tqdm import tqdm

def load_checkpoint_safely(model: torch.nn.Module, checkpoint_path: str, device: torch.device) -> None:
    ckpt = torch.load(checkpoint_path, map_location=device)
    state = ckpt.get("model_state", ckpt)
    try:
        model.load_state_dict(state, strict=True)
        print("[OK] Loaded full model state successfully")
        return
    except RuntimeError as e:
        print("[WARNING] Full load failed due to:", str(e).splitlines()[0])
        print("-> Attempting backbone-only load (excluding classifier)")
        backbone_state = {k: v for k, v in state.items() if not k.startswith("classifier")}
        missing, unexpected = model.load_state_dict(backbone_state, strict=False)
        if missing:
            print("Missing keys after backbone load:", [k for k in missing if not k.startswith("classifier")][:6], "...")
        if unexpected:
            print("Unexpected keys ignored:", unexpected[:6], "...")
        print("[OK] Backbone loaded; classifier will use current architecture")

def evaluate(model_path: str = "./outputs/checkpoints/best_model.pth", data_dir: str = "./data", split: str = "val", batch_size: int = 32, img_size: int = 224, val_center_crop: bool = True):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    _, val_loader, classes = get_dataloaders(data_dir, img_size=img_size, batch_size=batch_size, val_center_crop=val_center_crop)
    model = get_model("convnext_tiny", num_classes=len(classes)).to(device)

    print(f"Loading checkpoint: {model_path}")
    load_checkpoint_safely(model, model_path, device)
    model.eval()

    criterion = nn.CrossEntropyLoss()
    val_loss, correct, total = 0.0, 0, 0

    with torch.no_grad():
        for x, y in tqdm(val_loader, desc="Evaluating"):
            x, y = x.to(device), y.to(device)
            out = model(x)
            loss = criterion(out, y)
            val_loss += loss.item() * x.size(0)
            _, pred = out.max(1)
            correct += pred.eq(y).sum().item()
            total += y.size(0)

    acc = correct / total if total > 0 else 0.0
    avg_loss = val_loss / total if total > 0 else 0.0
    print(f"Accuracy on {split} set: {acc*100:.2f}%")
    print(f"Average loss: {avg_loss:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="./data")
    parser.add_argument("--checkpoint", type=str, default="./outputs/checkpoints/best_model.pth")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--img_size", type=int, default=224)
    parser.add_argument("--val_center_crop", action="store_true")
    args = parser.parse_args()
    evaluate(model_path=args.checkpoint, data_dir=args.data_dir, batch_size=args.batch_size, img_size=args.img_size, val_center_crop=args.val_center_crop)
