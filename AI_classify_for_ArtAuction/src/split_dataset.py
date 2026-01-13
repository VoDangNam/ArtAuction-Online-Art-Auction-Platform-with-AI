#!/usr/bin/env python3
"""
split_dataset.py
- Input: data_raw/ (contains either "AI" and "Human" folders, or many folders named AI_* and Human_*)
- Output: data/train/AI/... , data/train/Human/... , data/val/AI/... , data/val/Human/...
- Preserves subfolder structure under each AI/Human root.
- Usage:
  python src/split_dataset.py --raw_dir ./data_raw --out_dir ./data --train_ratio 0.8 --move False
"""

import argparse
from pathlib import Path
import random
import shutil
from tqdm import tqdm

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}

def find_class_roots(raw_dir: Path):
    """
    Return two lists: ai_roots, human_roots (paths)
    Accept either:
      - raw_dir/AI/..., raw_dir/Human/...
      - raw_dir/AI_*..., raw_dir/Human_*...
    """
    ai_roots = []
    human_roots = []
    for p in raw_dir.iterdir():
        if not p.is_dir():
            continue
        n = p.name.lower()
        if n == "ai" or n.startswith("ai_"):
            ai_roots.append(p)
        elif n == "human" or n.startswith("human_"):
            human_roots.append(p)
    return ai_roots, human_roots

def gather_images(root: Path):
    """Return list of Path to image files under root (recursive)."""
    files = []
    for f in root.rglob("*"):
        if f.is_file() and f.suffix.lower() in IMG_EXTS:
            files.append(f)
    return files

def safe_copy(src: Path, dst: Path, move=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        # avoid overwrite by adding suffix
        base = dst.stem
        suf = dst.suffix
        i = 1
        while True:
            new_name = f"{base}_{i}{suf}"
            new_path = dst.parent / new_name
            if not new_path.exists():
                dst = new_path
                break
            i += 1
    if move:
        shutil.move(str(src), str(dst))
    else:
        shutil.copy2(str(src), str(dst))

def split_and_copy(files, out_dir: Path, split_name: str, cls_name: str, preserve_subdir_from: Path, move=False):
    """
    files: list of Paths (absolute). preserve_subdir_from: when copying preserve relative path relative to this
    e.g., if src = preserve_subdir_from / "AI_SD_baroque" / "img1.jpg"
    we copy to out_dir/split_name/cls_name/AI_SD_baroque/img1.jpg
    """
    for f in tqdm(files, desc=f"Copying {cls_name} {split_name}"):
        # compute relative part under preserve_subdir_from, then under cls_name
        try:
            rel = f.relative_to(preserve_subdir_from)
        except Exception:
            # fallback to filename only
            rel = f.name
        dst = out_dir / split_name / cls_name / rel
        safe_copy(f, dst, move=move)

def split_dataset(raw_dir: str, out_dir: str, train_ratio: float = 0.8, seed: int = 42, move: bool = False):
    raw = Path(raw_dir).expanduser().resolve()
    out = Path(out_dir).expanduser().resolve()
    assert raw.exists(), f"Raw dir not found: {raw}"

    out_train_ai = out / "train" / "AI"
    out_train_hu = out / "train" / "Human"
    out_val_ai = out / "val" / "AI"
    out_val_hu = out / "val" / "Human"
    # create base dirs
    (out / "train" / "AI").mkdir(parents=True, exist_ok=True)
    (out / "train" / "Human").mkdir(parents=True, exist_ok=True)
    (out / "val" / "AI").mkdir(parents=True, exist_ok=True)
    (out / "val" / "Human").mkdir(parents=True, exist_ok=True)

    ai_roots, human_roots = find_class_roots(raw)
    if not ai_roots and not human_roots:
        raise RuntimeError("No AI/Human folders found. Expected folder names 'AI' or 'AI_*', 'Human' or 'Human_*' inside raw_dir.")

    print("AI roots:", ai_roots)
    print("Human roots:", human_roots)

    random.seed(seed)

    # gather files from all ai_roots, keep track of original root for preserving subdirs
    all_ai = []
    for r in ai_roots:
        files = gather_images(r)
        all_ai.extend([(f, r) for f in files])

    all_human = []
    for r in human_roots:
        files = gather_images(r)
        all_human.extend([(f, r) for f in files])

    print(f"Found {len(all_ai)} AI images and {len(all_human)} Human images (total).")

    def do_split(list_of_pairs, cls_name):
        # list_of_pairs: [(Path file, Path preserve_root), ...]
        random.shuffle(list_of_pairs)
        n = len(list_of_pairs)
        n_train = int(n * train_ratio)
        train_pairs = list_of_pairs[:n_train]
        val_pairs = list_of_pairs[n_train:]
        # copy train
        for f, root in tqdm(train_pairs, desc=f"Copy train {cls_name}"):
            # relative path under preserve root
            rel = f.relative_to(root)
            dst = out / "train" / cls_name / root.name / rel
            safe_copy(f, dst, move=move)
        # copy val
        for f, root in tqdm(val_pairs, desc=f"Copy val {cls_name}"):
            rel = f.relative_to(root)
            dst = out / "val" / cls_name / root.name / rel
            safe_copy(f, dst, move=move)

    do_split(all_ai, "AI")
    do_split(all_human, "Human")

    print("Split done.")
    print("Train folder:", out / "train")
    print("Val folder:", out / "val")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--raw_dir", type=str, default="./data_raw", help="Input raw folder")
    p.add_argument("--out_dir", type=str, default="./data", help="Output data folder (train/val)")
    p.add_argument("--train_ratio", type=float, default=0.8, help="Train ratio (0..1)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--move", action="store_true", help="Move files instead of copying (saves disk)")
    args = p.parse_args()
    split_dataset(args.raw_dir, args.out_dir, args.train_ratio, args.seed, move=args.move)
