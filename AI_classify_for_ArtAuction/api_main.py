import os
import io
from pathlib import Path
from typing import Optional, Dict, Any

from flask import Flask, request, jsonify
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as T
from torchvision.models import convnext_tiny

# ==============================
#         FLASK APP
# ==============================
app = Flask(__name__)

# Enable CORS manually
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


# ==============================
#         COMMON CONFIG
# ==============================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMG_SIZE = 224

def allowed_file(filename: str):
    _, ext = os.path.splitext(filename.lower())
    return ext in {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}


# ==============================
#   MODEL B: MULTI-CLASS (style)
# ==============================
# Bạn đang dùng get_model từ file model.py (ConvNeXt-tiny của bạn)
# -> đổi tên import để khỏi đụng get_model ở model binary.
from model import get_model as get_model_multiclass  # noqa: E402

CHECKPOINT_PATH_MULTI = "./outputs/classify_model/model_67acc.pth"
CLASSES_PATH_MULTI = "./outputs/classify_model/classes.txt"

def load_classes(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Không tìm thấy file classes: {path}. "
            f"Hãy tạo file classes.txt (mỗi dòng 1 class, đúng thứ tự label)."
        )
    with open(path, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f if line.strip()]
    return classes

classes_multi = []
model_multi = None
multi_error = None

# Transform giống file 1 (Resize 224x224)
transform_multi = T.Compose([
    T.Resize((IMG_SIZE, IMG_SIZE)),
    T.ToTensor(),
    T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

def load_model_multiclass():
    global classes_multi, model_multi, multi_error
    try:
        classes_multi = load_classes(CLASSES_PATH_MULTI)

        model = get_model_multiclass("convnext_tiny", num_classes=len(classes_multi), dropout_rate=0.0)
        ckpt = torch.load(CHECKPOINT_PATH_MULTI, map_location=device)

        state_dict = ckpt.get("model_state", ckpt)
        try:
            model.load_state_dict(state_dict, strict=True)
            print("[MULTI] [OK] Loaded full model weights.")
        except RuntimeError:
            print("[MULTI] [WARN] Architecture changed. Trying strict=False (ignore mismatch).")
            model.load_state_dict(state_dict, strict=False)

        model.to(device)
        model.eval()

        model_multi = model
        multi_error = None
    except Exception as e:
        model_multi = None
        multi_error = str(e)
        print(f"[MULTI] [ERROR] Could not load multi-class model: {multi_error}")

def tta_predict_multiclass(img_tensor: torch.Tensor, num_augments: int = 5):
    """
    img_tensor: shape (1, C, H, W)
    Trả về probs trung bình sau khi flip ngang nhiều lần.
    """
    if model_multi is None:
        raise RuntimeError("Multi-class model chưa load được.")

    with torch.no_grad():
        logits = model_multi(img_tensor)
        probs = F.softmax(logits, dim=1)

        for _ in range(num_augments - 1):
            flipped = torch.flip(img_tensor, dims=[3])  # flip ngang
            logits_flipped = model_multi(flipped)
            probs += F.softmax(logits_flipped, dim=1)

        probs /= num_augments

    return probs.squeeze(0)  # (num_classes,)


# ==============================
#   MODEL A: BINARY (AI vs Human)
# ==============================
MODEL_PATH_BIN = "./outputs/epoch_checkpoints/epoch_36.pth"
MODEL_NAME_BIN = "convnext_tiny"
THRESHOLD_DEFAULT = 0.75

model_bin = None
best_acc = 0.0
best_epoch = -1
bin_error = None

def build_model_binary(model_name="convnext_tiny", num_classes=2, pretrained=True, dropout_rate=0.2):
    """Load ConvNeXt Tiny model with same architecture as training (binary)"""
    if model_name == "convnext_tiny":
        weights = None if not pretrained else "DEFAULT"
        model = convnext_tiny(weights=weights)
        in_features = model.classifier[2].in_features

        model.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(dropout_rate),
            nn.Linear(in_features, in_features // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate * 0.3),
            nn.Linear(in_features // 2, num_classes),
        )
        return model
    raise ValueError(f"Model {model_name} not supported")

transform_bin = T.Compose([
    T.Resize(int(IMG_SIZE * 1.14)),
    T.CenterCrop(IMG_SIZE),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

def load_model_binary():
    global model_bin, best_acc, best_epoch, bin_error
    try:
        print("[BIN] Loading model:", MODEL_NAME_BIN, "from", MODEL_PATH_BIN, "device:", device)

        if not os.path.exists(MODEL_PATH_BIN):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH_BIN}")

        model = build_model_binary(MODEL_NAME_BIN, num_classes=2, pretrained=False, dropout_rate=0.2)
        model.to(device)

        ckpt = torch.load(MODEL_PATH_BIN, map_location=device)
        if isinstance(ckpt, dict) and "model_state" in ckpt:
            model.load_state_dict(ckpt["model_state"])
            best_acc = ckpt.get("best_acc", 0.0)
            best_epoch = ckpt.get("best_epoch", -1)
        else:
            model.load_state_dict(ckpt)
            best_acc = 0.0
            best_epoch = -1

        model.eval()
        model_bin = model
        bin_error = None
        print(f"[BIN] Model loaded! Best accuracy: {best_acc*100:.2f}%")
    except Exception as e:
        model_bin = None
        best_acc = 0.0
        best_epoch = -1
        bin_error = str(e)
        print(f"[BIN] WARNING: could not load model at startup: {bin_error}")

def autocast_if_cuda():
    # PyTorch >= 2: torch.amp.autocast("cuda")
    # PyTorch cũ: torch.cuda.amp.autocast()
    if device.type == "cuda":
        try:
            return torch.amp.autocast("cuda")
        except Exception:
            return torch.cuda.amp.autocast()
    # CPU: no autocast
    from contextlib import nullcontext
    return nullcontext()


# ==============================
#          LOAD BOTH
# ==============================
load_model_multiclass()
load_model_binary()


# ==============================
#            ROUTES
# ==============================
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "api_name": "ArtAuction - Multi Model API",
        "version": "1.0.0",
        "status": "running",
        "device": str(device),
        "models": {
            "binary_ai_vs_human": {
                "loaded": model_bin is not None,
                "model_name": MODEL_NAME_BIN,
                "accuracy": f"{best_acc*100:.2f}%",
                "epoch": best_epoch,
                "error": bin_error,
                "endpoint": "/predict (POST)"
            },
            "multiclass_style": {
                "loaded": model_multi is not None,
                "num_classes": len(classes_multi) if classes_multi else 0,
                "error": multi_error,
                "endpoint": "/classify (POST)"
            }
        },
        "endpoints": {
            "health": "/health",
            "predict_binary": "/predict (POST with image/file)",
            "classify_multiclass": "/classify (POST with file/image)",
            "report_binary": "/report (POST)"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "device": str(device),
        "binary_model_loaded": model_bin is not None,
        "binary_error": bin_error,
        "multiclass_model_loaded": model_multi is not None,
        "multiclass_error": multi_error,
        "num_classes_multiclass": len(classes_multi) if classes_multi else 0,
    })


# ------------------------------
#  MULTI-CLASS STYLE CLASSIFY
# ------------------------------
@app.route("/classify", methods=["POST"])
def classify_multiclass():
    """
    Nhận form-data:
      - file=@path/to/image.jpg (key: 'file')
    hoặc (cho tiện):
      - image=@path/to/image.jpg (key: 'image')
    Trả JSON: top1 + topk (5)
    """
    if model_multi is None:
        return jsonify({"error": f"Multi-class model chưa load được: {multi_error}"}), 503

    file = request.files.get("file") or request.files.get("image")
    if file is None:
        return jsonify({"error": "Thiếu file. Gửi form-data với key 'file' hoặc 'image'."}), 400

    if file.filename == "":
        return jsonify({"error": "Tên file rỗng."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed."}), 400

    try:
        img = Image.open(file.stream).convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Không đọc được ảnh: {str(e)}"}), 400

    img_tensor = transform_multi(img).unsqueeze(0).to(device)

    try:
        probs = tta_predict_multiclass(img_tensor, num_augments=5)
        top_k = min(5, len(classes_multi))
        top_probs, top_idxs = torch.topk(probs, k=top_k)

        topk_results = []
        for p, idx in zip(top_probs, top_idxs):
            idx = idx.item()
            topk_results.append({
                "index": idx,
                "label": classes_multi[idx],
                "probability": float(p.item())
            })

        return jsonify({
            "top1": topk_results[0],
            "topk": topk_results
        })
    except Exception as e:
        return jsonify({"error": f"Lỗi khi dự đoán multi-class: {str(e)}"}), 500


# ------------------------------
#  BINARY AI vs HUMAN PREDICT
# ------------------------------
@app.route("/predict", methods=["POST"])
def predict_binary():
    """
    Nhận form-data:
      - image=@... (key: 'image')  (chuẩn file 2)
    hoặc (cho tiện):
      - file=@...  (key: 'file')  (chuẩn file 1)
    """
    if model_bin is None:
        return jsonify({"success": False, "message": f"Model not loaded on server: {bin_error}"}), 503

    file = request.files.get("image") or request.files.get("file")
    if file is None:
        return jsonify({"success": False, "message": "No image part in the request (use key 'image' or 'file')"}), 400

    if file.filename == "":
        return jsonify({"success": False, "message": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed"}), 400

    try:
        img = Image.open(io.BytesIO(file.read())).convert("RGB")
    except Exception as e:
        return jsonify({"success": False, "message": f"Cannot open image: {str(e)}"}), 400

    x = transform_bin(img).unsqueeze(0).to(device)

    with torch.no_grad():
        with autocast_if_cuda():
            out = model_bin(x)
        probs = torch.softmax(out, dim=1).detach().float().cpu().numpy()[0]

    # Dataset classes: ["AI", "Human"] (alphabetical order)
    p_ai = float(probs[0])
    p_human = float(probs[1])

    assigned = "Unknown"
    confidence = max(p_ai * 100, p_human * 100)

    threshold = float(request.form.get("threshold", THRESHOLD_DEFAULT))
    if p_ai >= threshold:
        assigned = "AI"
    elif p_human >= threshold:
        assigned = "Human"

    return jsonify({
        "success": True,
        "prediction": assigned,
        "result": assigned,
        "human_probability": round(p_human * 100, 2),
        "ai_probability": round(p_ai * 100, 2),
        "confidence": round(confidence, 2),
        "threshold": threshold,
        "model_info": {
            "accuracy": f"{best_acc*100:.2f}%",
            "epoch": best_epoch
        }
    })


# ------------------------------
#  REPORT (BINARY) FOR RETRAIN
# ------------------------------
@app.route("/report", methods=["POST"])
def report():
    """Save incorrectly labeled images to report folder for retraining (binary)"""
    try:
        file = request.files.get("image") or request.files.get("file")
        if file is None:
            return jsonify({"success": False, "message": "No image in request (use key 'image' or 'file')"}), 400

        correct_label = request.form.get("correct_label")
        if not correct_label:
            return jsonify({"success": False, "message": "No correct_label in request"}), 400

        if correct_label not in ["AI", "Human"]:
            return jsonify({"success": False, "message": "Invalid label. Must be 'AI' or 'Human'"}), 400

        if file.filename == "":
            return jsonify({"success": False, "message": "No selected file"}), 400

        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "File type not allowed"}), 400

        wrong_prediction = request.form.get("wrong_prediction", "Unknown")
        wrong_probability = request.form.get("wrong_probability", "0")
        correct_probability = request.form.get("correct_probability", "0")
        confidence_delta = request.form.get("confidence_delta", "0")

        report_dir = f"./data/report/{correct_label}"
        os.makedirs(report_dir, exist_ok=True)

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = os.path.splitext(file.filename)[1] or ".jpg"
        save_path = os.path.join(report_dir, f"report_{timestamp}{ext}")

        img_data = file.read()
        with open(save_path, "wb") as f:
            f.write(img_data)

        import json
        cd = float(confidence_delta)
        metadata = {
            "correct_label": correct_label,
            "wrong_prediction": wrong_prediction,
            "wrong_probability": float(wrong_probability),
            "correct_probability": float(correct_probability),
            "confidence_delta": cd,
            "timestamp": timestamp,
            "error_severity": "high" if cd > 0.5 else "medium" if cd > 0.2 else "low"
        }

        metadata_path = save_path + ".json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return jsonify({
            "success": True,
            "message": f"Image saved to report/{correct_label} folder",
            "path": save_path,
            "metadata": metadata
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==============================
#            MAIN
# ==============================
if __name__ == "__main__":
    print("Starting Flask API...")
    print(f"Device: {device}")
    print(f"[BIN] Loaded: {model_bin is not None} | Acc: {best_acc*100:.2f}% | Epoch: {best_epoch} | Err: {bin_error}")
    print(f"[MULTI] Loaded: {model_multi is not None} | Classes: {len(classes_multi) if classes_multi else 0} | Err: {multi_error}")
    print("API will run on: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
