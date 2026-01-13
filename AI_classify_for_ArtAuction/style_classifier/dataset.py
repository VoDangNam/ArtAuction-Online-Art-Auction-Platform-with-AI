from pathlib import Path
from typing import List, Tuple

import torch
from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, transforms


def _build_transforms(img_size: int, keep_center_crop: bool) -> Tuple[transforms.Compose, transforms.Compose]:
    train_tf = transforms.Compose([
        transforms.Resize((img_size + 8, img_size + 8)),
        transforms.RandomCrop((img_size, img_size), padding=4, padding_mode="reflect"),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=3),
        transforms.ColorJitter(brightness=0.05, contrast=0.05, saturation=0.02, hue=0.01),
        transforms.RandomApply(
            [transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 0.5))],
            p=0.02,
        ),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    if keep_center_crop:
        val_tf = transforms.Compose([
            transforms.Resize(int(img_size * 1.14)),
            transforms.CenterCrop(img_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
    else:
        val_tf = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    return train_tf, val_tf


def _maybe_log_class_distribution(dataset: datasets.ImageFolder, split_name: str) -> None:
    label_counts = {}
    for _, label_idx in dataset.samples:
        label_counts[label_idx] = label_counts.get(label_idx, 0) + 1

    mapped = sorted(((dataset.classes[idx], count) for idx, count in label_counts.items()), key=lambda x: x[0])
    print(f"[INFO] Class distribution for {split_name}:")
    for cls_name, count in mapped:
        print(f"  - {cls_name}: {count} images")


def get_dataloaders(
    data_dir: str,
    img_size: int = 224,
    batch_size: int = 32,
    num_workers: int = 4,
    val_center_crop: bool = True,
    balance_classes: bool = True,
) -> Tuple[DataLoader, DataLoader, List[str]]:
    """
    Build train/val dataloaders for the art style classifier.

    The folder structure is expected to be:
        data_dir/
            train/<style_name>/*.jpg
            val/<style_name>/*.jpg
    """
    root = Path(data_dir)
    train_dir = root / "train"
    val_dir = root / "val"

    if not train_dir.exists() or not val_dir.exists():
        raise FileNotFoundError(
            f"Expected 'train' and 'val' folders under {root}. Found train={train_dir.exists()}, val={val_dir.exists()}."
        )

    train_tf, val_tf = _build_transforms(img_size, val_center_crop)

    train_ds = datasets.ImageFolder(root=train_dir.as_posix(), transform=train_tf)
    val_ds = datasets.ImageFolder(root=val_dir.as_posix(), transform=val_tf)

    if not (10 <= len(train_ds.classes) <= 15):
        print(f"[WARN] Detected {len(train_ds.classes)} classes. Make sure this matches the labeled art styles (expected 10-15).")

    _maybe_log_class_distribution(train_ds, "train")
    _maybe_log_class_distribution(val_ds, "val")

    sampler = None
    if balance_classes:
        sample_targets = torch.tensor(train_ds.targets, dtype=torch.long)
        class_sample_counts = torch.bincount(sample_targets)
        if torch.all(class_sample_counts > 0):
            weights = (1.0 / class_sample_counts.float())
            sample_weights = weights[sample_targets]
            sampler = WeightedRandomSampler(sample_weights.double(), len(sample_weights), replacement=True)
            print("[INFO] Enabled WeightedRandomSampler for balanced mini-batches.")

    persistent_workers = num_workers > 0

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=(sampler is None),
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=persistent_workers,
        prefetch_factor=2,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=persistent_workers,
        prefetch_factor=2,
    )

    return train_loader, val_loader, train_ds.classes

