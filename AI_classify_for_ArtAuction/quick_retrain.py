#!/usr/bin/env python
"""
Script to quickly retrain model on report data
This script:
1. Checks report data distribution
2. Trains model with balanced sampling
3. Reloads model in Flask API

Usage:
    python quick_retrain.py
    python quick_retrain.py --epochs 2 --lr 5e-4
"""

import subprocess
import sys
import os

def get_venv_python():
    """Get Python executable from venv if available"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(script_dir, "venv", "Scripts", "python.exe")
    
    if os.path.exists(venv_python):
        print(f"✓ Using venv Python: {venv_python}")
        return venv_python
    
    # Check if running inside venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"✓ Running inside virtual environment")
        return sys.executable
    
    # Fallback to system python
    print(f"⚠️  Warning: Not in virtual environment, using: {sys.executable}")
    return sys.executable

def main():
    # Step 1: Check if report data exists
    report_dir = "./data/report"
    if not os.path.exists(report_dir):
        print("❌ Error: Report directory not found")
        print("   Please report some images first through the web interface")
        return False
    
    # Count images
    from pathlib import Path
    ai_dir = Path(report_dir) / "AI"
    human_dir = Path(report_dir) / "Human"
    
    ai_count = len(list(ai_dir.glob("*.jpg"))) + len(list(ai_dir.glob("*.png"))) if ai_dir.exists() else 0
    human_count = len(list(human_dir.glob("*.jpg"))) + len(list(human_dir.glob("*.png"))) if human_dir.exists() else 0
    
    print("=" * 60)
    print("Report Data Summary:")
    print(f"  AI images: {ai_count}")
    print(f"  Human images: {human_count}")
    print(f"  Total: {ai_count + human_count}")
    print("=" * 60)
    
    if ai_count + human_count == 0:
        print("❌ Error: No images found in report directory")
        return False
    
    # Step 2: Run quick train
    print("\n🚀 Starting training on report data...")
    print("-" * 60)
    
    python_exe = get_venv_python()
    
    # Adjust epochs based on data imbalance
    if ai_count > human_count * 3 or human_count > ai_count * 3:
        epochs = "3"  # More epochs for imbalanced data
        print(f"⚠️  Imbalanced data detected, using {epochs} epochs")
    else:
        epochs = "2"
    
    cmd = [
        python_exe,
        "src/quick_train.py",
        "--epochs", epochs,
        "--lr", "1e-3",
        "--batch_size", "4"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n✓ Training completed!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training failed: {e}")
        return False
    
    # Step 3: Reload model in Flask API
    print("\n🔄 Reloading model in Flask API...")
    print("-" * 60)
    
    reload_cmd = [
        python_exe,
        "reload_model.py",
        "./outputs/checkpoints/best_model3_updated.pth"
    ]
    
    try:
        subprocess.run(reload_cmd, check=True, capture_output=False)
        print("\n✓ Model reloaded in Flask API!")
        print("\n✓ All done! Model is now updated and ready to use.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n⚠️  Model training succeeded but reload failed: {e}")
        print("   Please restart Flask API manually to load new model")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

