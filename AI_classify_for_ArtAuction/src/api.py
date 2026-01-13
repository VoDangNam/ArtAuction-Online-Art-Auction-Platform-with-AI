# src/api.py
import os
import io
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from PIL import Image
import torch
import torchvision.transforms as T

# import your model builder (adjust if your model function name differs)
from model import get_model

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}

# Config via env vars (or set defaults)
MODEL_PATH = os.environ.get("MODEL_PATH", "./outputs/checkpoints/best_model.pth")
MODEL_NAME = os.environ.get("MODEL_NAME", "convnext_tiny")
IMG_SIZE = int(os.environ.get("IMG_SIZE", 224))
THRESHOLD_DEFAULT = float(os.environ.get("THRESHOLD", 0.75))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = FastAPI(title="AI-vs-Human Classifier API")

# Allow CORS from frontend(s) — adjust origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictOut(BaseModel):
    p_human: float
    p_ai: float
    assigned: str
    threshold: float

# Build and load model once on startup
def load_model():
    print("Loading model:", MODEL_NAME, "from", MODEL_PATH, "device:", device)
    model = get_model(MODEL_NAME, num_classes=2, pretrained=False)
    model.to(device)
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    ckpt = torch.load(MODEL_PATH, map_location=device)
    # ckpt could be either a dict with "model_state" or a state_dict directly
    loaded = False
    if isinstance(ckpt, dict):
        if "model_state" in ckpt:
            model.load_state_dict(ckpt["model_state"])
            loaded = True
        else:
            # try to load as if it's a state_dict
            try:
                model.load_state_dict(ckpt)
                loaded = True
            except Exception:
                # maybe the checkpoint saved under different keys
                for k in ["state_dict", "model"]:
                    if k in ckpt and isinstance(ckpt[k], dict):
                        model.load_state_dict(ckpt[k])
                        loaded = True
                        break
    if not loaded:
        raise RuntimeError("Failed to load model state from checkpoint.")
    model.eval()
    return model

model = None
try:
    model = load_model()
except Exception as e:
    print("WARNING: could not load model at startup:", e)
    model = None

# transform (same preprocessing as training)
transform = T.Compose([
    T.Resize(int(IMG_SIZE * 1.14)),
    T.CenterCrop(IMG_SIZE),
    T.ToTensor(),
    T.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225])
])

def allowed_file(filename: str):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXT

@app.get("/health")
async def health():
    return {"status": "ok", "device": str(device), "model_loaded": model is not None}

@app.post("/predict", response_model=PredictOut)
async def predict(file: UploadFile = File(...), threshold: Optional[float] = Query(None, ge=0.0, le=1.0)):
    """
    Upload an image file (form-data key 'file') and optionally pass threshold in query (0.0-1.0).
    Returns p_human, p_ai (floats 0..1) and assigned label (AI/Human/Unknown).
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded on server")

    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")

    data = await file.read()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        img = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot open image")

    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        # use autocast on CUDA if available for speed
        if device.type == "cuda":
            with torch.amp.autocast("cuda"):
                out = model(x)
        else:
            out = model(x)
        probs = torch.softmax(out, dim=1).cpu().numpy()[0]
    # Dataset classes: ["AI", "Human"] (alphabetical order)
    # Class 0 = "AI", Class 1 = "Human"
    p_ai = float(probs[0])      # probs[0] = AI
    p_human = float(probs[1])   # probs[1] = Human
    thr = threshold if threshold is not None else THRESHOLD_DEFAULT

    # percent formatting
    p_human_pct = round(p_human * 100.0, 2)
    p_ai_pct = round(p_ai * 100.0, 2)

    assigned = "Unknown"
    if p_ai >= thr:
        assigned = "AI"
    elif p_human >= thr:
        assigned = "Human"

    return {
        "p_human": p_human_pct,
        "p_ai": p_ai_pct,
        "assigned": assigned,
        "threshold": round(thr * 100.0, 2)
    }

# Optional: endpoint to reload model at runtime
@app.post("/reload_model")
async def reload_model(model_path: Optional[str] = None):
    global model, MODEL_PATH
    if model_path:
        MODEL_PATH = model_path
    try:
        model = load_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "reloaded", "model_path": MODEL_PATH}

if __name__ == "__main__":
    # Run with: MODEL_PATH=./outputs/checkpoints/best_model.pth MODEL_NAME=convnext_tiny python src/api.py
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
