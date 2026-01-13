import os
import io

from flask import Flask, request, jsonify
from PIL import Image

import torch
import torch.nn.functional as F
from torchvision import transforms

from model import get_model  # dùng lại model ConvNeXt-tiny của bạn


# ==============================
#       CONFIG & LOADING
# ==============================
IMG_SIZE = 224  # nên để giống lúc training (args.img_size)
CHECKPOINT_PATH = "./outputs/classify_model/model_67acc.pth"
CLASSES_PATH = "./outputs/classify_model/classes.txt"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ----- Load class names -----
def load_classes(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Không tìm thấy file classes: {path}. "
            f"Hãy tạo file classes.txt (mỗi dòng 1 class, đúng thứ tự label)."
        )
    with open(path, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f if line.strip()]
    return classes


classes = load_classes(CLASSES_PATH)


# ----- Image transform giống lúc training (ImageNet norm) -----
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],   # chuẩn ImageNet
        std=[0.229, 0.224, 0.225],
    ),
])


# ----- Load model + checkpoint -----
def load_model():
    model = get_model("convnext_tiny", num_classes=len(classes), dropout_rate=0.0)
    ckpt = torch.load(CHECKPOINT_PATH, map_location=device)

    # training script của bạn dùng dạng dict với key 'model_state'
    state_dict = ckpt.get("model_state", ckpt)

    try:
        model.load_state_dict(state_dict, strict=True)
        print("[OK] Loaded full model weights.")
    except RuntimeError:
        print("[WARN] Architecture changed. Trying partial load (ignoring classifier mismatch).")
        # Bỏ qua các layer không khớp (thường là classifier)
        model.load_state_dict(state_dict, strict=False)

    model.to(device)
    model.eval()
    return model


model = load_model()


# ==============================
#        TTA PREDICT (nhẹ)
# ==============================
def tta_predict(img_tensor: torch.Tensor, num_augments: int = 5):
    """
    img_tensor: shape (1, C, H, W)
    Trả về probs trung bình sau khi flip ngang nhiều lần.
    """
    with torch.no_grad():
        # Original
        logits = model(img_tensor)
        probs = F.softmax(logits, dim=1)

        # Horizontal flip TTA
        for _ in range(num_augments - 1):
            flipped = torch.flip(img_tensor, dims=[3])  # flip theo chiều ngang
            logits_flipped = model(flipped)
            probs += F.softmax(logits_flipped, dim=1)

        probs /= num_augments

    return probs.squeeze(0)  # (num_classes,)


# ==============================
#         FLASK APP
# ==============================
app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "device": str(device),
        "num_classes": len(classes)
    })


@app.route("/classify", methods=["POST"])
def predict():
    """
    Nhận:
      - form-data: file=@path/to/image.jpg  (key: 'file')

    Trả:
      - JSON: top1 + topk (mặc định 5)
    """
    if "file" not in request.files:
        return jsonify({"error": "Thiếu file. Hãy gửi với key 'file' trong form-data."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Tên file rỗng."}), 400

    try:
        # Đọc ảnh bằng PIL và convert sang RGB
        img = Image.open(file.stream).convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Không đọc được ảnh: {str(e)}"}), 400

    # Transform -> tensor -> batch size 1
    img_tensor = transform(img).unsqueeze(0).to(device)

    # Dự đoán
    try:
        # Nếu không muốn TTA thì dùng đoạn này:
        # with torch.no_grad():
        #     logits = model(img_tensor)
        #     probs = F.softmax(logits, dim=1).squeeze(0)

        # Dùng TTA cho giống training script
        probs = tta_predict(img_tensor, num_augments=5)

        # Lấy top-k
        top_k = min(5, len(classes))
        top_probs, top_idxs = torch.topk(probs, k=top_k)

        topk_results = []
        for p, idx in zip(top_probs, top_idxs):
            idx = idx.item()
            topk_results.append({
                "index": idx,
                "label": classes[idx],
                "probability": float(p.item())
            })

        response = {
            "top1": topk_results[0],
            "topk": topk_results
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Lỗi khi dự đoán: {str(e)}"}), 500


if __name__ == "__main__":
    # Chạy server Flask
    # host="0.0.0.0" để có thể gọi từ máy khác trong LAN
    app.run(host="0.0.0.0", port=5000, debug=False)
