import os
import io
from flask import Flask, request, jsonify
from PIL import Image
import torch
import torch.nn as nn
from torchvision.models import convnext_tiny
import torchvision.transforms as T
from pathlib import Path
from typing import Optional, Dict, Any

app = Flask(__name__)

# Enable CORS manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Configuration
# MODEL_PATH = "./outputs/checkpoints/best_model3.pth"
MODEL_PATH = "./outputs/epoch_checkpoints/epoch_36.pth"
MODEL_NAME = "convnext_tiny"
IMG_SIZE = 224
THRESHOLD_DEFAULT = 0.75

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_model(model_name="convnext_tiny", num_classes=2, pretrained=True, dropout_rate=0.2):
    """Load ConvNeXt Tiny model with same architecture as training"""
    if model_name == "convnext_tiny":
        weights = None if not pretrained else "DEFAULT"
        model = convnext_tiny(weights=weights)
        in_features = model.classifier[2].in_features
        
        # Same classifier architecture as training
        model.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(dropout_rate),
            nn.Linear(in_features, in_features // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate * 0.3),
            nn.Linear(in_features // 2, num_classes)
        )
    else:
        raise ValueError(f"Model {model_name} not supported")
    return model

# Load model once on startup
model = None
best_acc = 0.0
best_epoch = -1

try:
    print("Loading model:", MODEL_NAME, "from", MODEL_PATH, "device:", device)
    model = get_model(MODEL_NAME, num_classes=2, pretrained=False, dropout_rate=0.2)
    model.to(device)
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    ckpt = torch.load(MODEL_PATH, map_location=device)
    if isinstance(ckpt, dict) and "model_state" in ckpt:
        model.load_state_dict(ckpt["model_state"])
        best_acc = ckpt.get("best_acc", 0.0)
        best_epoch = ckpt.get("best_epoch", -1)
    else:
        model.load_state_dict(ckpt)
        best_acc = 0.0
        best_epoch = -1

    model.eval()
    print(f"Model loaded! Best accuracy: {best_acc*100:.2f}%")
except Exception as e:
    print(f"WARNING: could not load model at startup: {e}")
    model = None
    best_acc = 0.0
    best_epoch = -1

# Image transform (same preprocessing as training)
transform = T.Compose([
    T.Resize(int(IMG_SIZE * 1.14)),
    T.CenterCrop(IMG_SIZE),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def allowed_file(filename: str):
    _, ext = os.path.splitext(filename.lower())
    return ext in {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}

@app.route('/')
def index():
    return jsonify({
        "api_name": "AI vs Human Artwork Classifier API",
        "version": "1.0.0",
        "status": "running",
        "model_info": {
            "name": MODEL_NAME,
            "accuracy": f"{best_acc*100:.2f}%",
            "epoch": best_epoch
        },
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST with file)"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "device": str(device),
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"success": False, "message": "Model not loaded on server"}), 503

    if 'image' not in request.files:
        return jsonify({"success": False, "message": "No image part in the request"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "File type not allowed"}), 400

    try:
        img = Image.open(io.BytesIO(file.read())).convert("RGB")
    except Exception as e:
        return jsonify({"success": False, "message": f"Cannot open image: {str(e)}"}), 400

    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        if device.type == "cuda":
            with torch.amp.autocast("cuda"):
                out = model(x)
        else:
            out = model(x)
        probs = torch.softmax(out, dim=1).cpu().numpy()[0]
    
    # Dataset classes: ["AI", "Human"] (alphabetical order)
    # probs[0] = AI, probs[1] = Human
    p_ai = float(probs[0])
    p_human = float(probs[1])
    
    assigned = "Unknown"
    confidence = max(p_ai * 100, p_human * 100)
    
    if p_ai >= THRESHOLD_DEFAULT:
        assigned = "AI"
    elif p_human >= THRESHOLD_DEFAULT:
        assigned = "Human"

    return jsonify({
        "success": True,
        "prediction": assigned,
        "result": assigned,
        "human_probability": round(p_human * 100, 2),
        "ai_probability": round(p_ai * 100, 2),
        "confidence": round(confidence, 2),
        "model_info": {
            "accuracy": f"{best_acc*100:.2f}%",
            "epoch": best_epoch
        }
    })


@app.route('/report', methods=['POST'])
def report():
    """Save incorrectly labeled images to report folder for retraining"""
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No image in request"}), 400
        
        if 'correct_label' not in request.form:
            return jsonify({"success": False, "message": "No correct_label in request"}), 400
        
        file = request.files['image']
        correct_label = request.form['correct_label']
        
        # Validate label
        if correct_label not in ['AI', 'Human']:
            return jsonify({"success": False, "message": "Invalid label. Must be 'AI' or 'Human'"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "File type not allowed"}), 400
        
        # Get metadata about the mistake (nếu có)
        wrong_prediction = request.form.get('wrong_prediction', 'Unknown')
        wrong_probability = request.form.get('wrong_probability', '0')
        correct_probability = request.form.get('correct_probability', '0')
        confidence_delta = request.form.get('confidence_delta', '0')
        
        # Create report directory if not exists
        report_dir = f"./data/report/{correct_label}"
        os.makedirs(report_dir, exist_ok=True)
        
        # Save image with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = os.path.splitext(file.filename)[1]
        save_path = os.path.join(report_dir, f"report_{timestamp}{ext}")
        
        # Read and save image
        img_data = file.read()
        with open(save_path, 'wb') as f:
            f.write(img_data)
        
        # Save metadata file (JSON)
        import json
        metadata = {
            "correct_label": correct_label,
            "wrong_prediction": wrong_prediction,
            "wrong_probability": float(wrong_probability),
            "correct_probability": float(correct_probability),
            "confidence_delta": float(confidence_delta),
            "timestamp": timestamp,
            "error_severity": "high" if float(confidence_delta) > 0.5 else "medium" if float(confidence_delta) > 0.2 else "low"
        }
        
        metadata_path = save_path + ".json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return jsonify({
            "success": True,
            "message": f"Image saved to report/{correct_label} folder",
            "path": save_path,
            "metadata": metadata
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask API...")
    print(f"Model: {MODEL_NAME}")
    print(f"Accuracy: {best_acc*100:.2f}%")
    print(f"API will run on: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
