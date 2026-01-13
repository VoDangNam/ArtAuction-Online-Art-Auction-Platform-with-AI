from torchvision import datasets, transforms
import torch
import os
from torch.utils.data import ConcatDataset, WeightedRandomSampler

def get_dataloaders(data_dir, img_size=224, batch_size=32, num_workers=4, val_center_crop=True, use_report_data=True, report_weight=3.0):
    train_tf = transforms.Compose([
        transforms.Resize((img_size + 8, img_size + 8)),  # Resize nhỏ hơn
        transforms.RandomCrop((img_size, img_size), padding=4, padding_mode='reflect'),
        transforms.RandomHorizontalFlip(p=0.5),
        # Bỏ RandomVerticalFlip - không phù hợp artwork
        transforms.RandomRotation(degrees=3),  # Giảm mạnh từ 10 xuống 3
        transforms.ColorJitter(brightness=0.05, contrast=0.05, saturation=0.02, hue=0.01),  # Giảm rất mạnh
        transforms.RandomApply([transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 0.5))], p=0.02),  # Giảm mạnh
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])

    if val_center_crop:
        # Giống pipeline infer 224-center-crop (khi img_size=224)
        val_tf = transforms.Compose([
            transforms.Resize(int(img_size * 1.14)),
            transforms.CenterCrop(img_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])
    else:
        val_tf = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])

    train_ds = datasets.ImageFolder(root=f"{data_dir}/train", transform=train_tf)
    report_ds = None
    
    # Merge report data if exists
    if use_report_data and os.path.exists(f"{data_dir}/report"):
        report_ds = datasets.ImageFolder(root=f"{data_dir}/report", transform=train_tf)
        # Duplicate report images để xuất hiện nhiều lần hơn
        # Thay vì dùng weighted sampler phức tạp, duplicate trực tiếp trong dataset
        duplicated_report = ConcatDataset([report_ds] * int(report_weight))  # Duplicate report_weight lần
        train_ds = ConcatDataset([train_ds, duplicated_report])
        
        # Report images đã duplicate trong dataset
        # Không cần tính indices nữa vì shuffle sẽ xử lý
        train_size = len(train_ds.datasets[0])
        print(f"  Original train size: {train_size}")
        
        print(f"✓ Merged {len(report_ds)} report images (duplicated {int(report_weight)}x) into training dataset")
        print(f"  Total training images: {len(train_ds)}")
        print(f"  Report images will appear {int(report_weight)}x per epoch (for better learning)")
    
    val_ds = datasets.ImageFolder(root=f"{data_dir}/val", transform=val_tf)
    
    # Không cần weighted sampler nữa vì đã duplicate trực tiếp trong dataset
    # Simple shuffle đảm bảo tất cả ảnh được duyệt qua
    sampler = None
    
    if use_report_data and report_ds is not None:
        # Log severity từ metadata (để info, không dùng cho training)
        import json
        from pathlib import Path
        
        high_severity_count = 0
        if report_ds is not None and len(report_ds.imgs) > 0:
            for img_path, label in report_ds.imgs:
                try:
                    metadata_path = Path(img_path).with_suffix(Path(img_path).suffix + ".json")
                    if metadata_path.exists():
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        if metadata.get('error_severity') == 'high':
                            high_severity_count += 1
                            print(f"  ⚠️  High severity: {metadata['wrong_prediction']} → {metadata['correct_label']} (delta={metadata['confidence_delta']:.3f})")
                except:
                    pass
        
        if high_severity_count > 0:
            print(f"  Found {high_severity_count} high-severity mistakes (will be duplicated {int(report_weight)}x for intensive learning)")
    
    train_loader = torch.utils.data.DataLoader(
        train_ds, 
        batch_size=batch_size, 
        shuffle=(sampler is None),  # Nếu có sampler thì không shuffle
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=True,
        prefetch_factor=2
    )
    val_loader = torch.utils.data.DataLoader(
        val_ds, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=True,
        prefetch_factor=2
    )

    # Get classes - nếu là ConcatDataset thì lấy từ dataset đầu tiên
    if hasattr(train_ds, 'classes'):
        classes = train_ds.classes
    else:
        # ConcatDataset case - lấy từ dataset đầu tiên
        classes = train_ds.datasets[0].classes
    
    return train_loader, val_loader, classes
