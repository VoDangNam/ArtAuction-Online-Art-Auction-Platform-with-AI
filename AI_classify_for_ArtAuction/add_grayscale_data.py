#!/usr/bin/env python3
"""
add_grayscale_data.py
- Convert existing color images to grayscale and add to dataset
- Maintains train/val split structure
- Adds 10-15% grayscale images to each class
"""

import os
import random
from pathlib import Path
from PIL import Image
from tqdm import tqdm

def convert_to_grayscale(img_path, output_path):
    """Convert color image to grayscale (3-channel RGB)"""
    try:
        img = Image.open(img_path).convert("RGB")
        # Convert to grayscale then back to RGB (3 channels)
        img_gray = img.convert("L").convert("RGB")
        img_gray.save(output_path, "JPEG", quality=95)
        return True
    except Exception as e:
        print(f"Error converting {img_path}: {e}")
        return False

def add_grayscale_to_dataset(data_dir="./data", target_ratio=0.12):
    """
    Add grayscale images to dataset
    - data_dir: path to data directory
    - target_ratio: ratio of grayscale images to add (0.12 = 12%)
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"Data directory not found: {data_dir}")
        return
    
    # Process both train and val
    for split in ["train", "val"]:
        split_path = data_path / split
        if not split_path.exists():
            print(f"Split directory not found: {split_path}")
            continue
            
        print(f"\nProcessing {split} split...")
        
        # Process each class (AI, Human)
        for class_name in ["AI", "Human"]:
            class_path = split_path / class_name
            if not class_path.exists():
                print(f"Class directory not found: {class_path}")
                continue
                
            print(f"  Processing {class_name} class...")
            
            # Get all image files recursively (handle nested structure)
            image_files = []
            for ext in ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp", "*.tiff"]:
                image_files.extend(class_path.rglob(ext))
            
            if not image_files:
                print(f"    No images found in {class_path}")
                continue
                
            # Calculate how many to convert
            num_images = len(image_files)
            num_to_convert = int(num_images * target_ratio)
            
            print(f"    Found {num_images} images, will convert {num_to_convert} to grayscale")
            
            # Randomly select images to convert
            selected_files = random.sample(image_files, min(num_to_convert, num_images))
            
            # Convert selected images
            converted_count = 0
            for img_file in tqdm(selected_files, desc=f"    Converting {class_name}"):
                # Create new filename with _gray suffix
                stem = img_file.stem
                suffix = img_file.suffix
                new_filename = f"{stem}_gray{suffix}"
                output_path = img_file.parent / new_filename
                
                # Skip if already exists
                if output_path.exists():
                    continue
                    
                if convert_to_grayscale(img_file, output_path):
                    converted_count += 1
            
            print(f"    Converted {converted_count} images to grayscale")
    
    print("\n✅ Grayscale data addition completed!")
    print(f"Added approximately {target_ratio*100:.1f}% grayscale images to each class")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Add grayscale images to dataset")
    parser.add_argument("--data_dir", type=str, default="./data", help="Path to data directory")
    parser.add_argument("--ratio", type=float, default=0.12, help="Ratio of grayscale images to add (0.12 = 12%)")
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(42)
    
    add_grayscale_to_dataset(args.data_dir, args.ratio)
