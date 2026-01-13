"""
Script để verify class mapping giữa train và report folder
Đảm bảo ảnh report được map đúng nhãn
"""
from pathlib import Path
from torchvision import datasets

def verify_class_mapping(data_dir="./data"):
    """Verify class mapping giữa train và report"""
    
    print("=" * 60)
    print("VERIFYING CLASS MAPPING")
    print("=" * 60)
    
    # Load train dataset
    train_ds = datasets.ImageFolder(root=f"{data_dir}/train")
    print(f"\n✓ Train dataset:")
    print(f"  Classes: {train_ds.classes}")
    print(f"  Class to idx: {train_ds.class_to_idx}")
    
    # Load report dataset (nếu có)
    report_path = Path(data_dir) / "report"
    if report_path.exists():
        report_ds = datasets.ImageFolder(root=str(report_path))
        print(f"\n✓ Report dataset:")
        print(f"  Classes: {report_ds.classes}")
        print(f"  Class to idx: {report_ds.class_to_idx}")
        
        # Verify mapping
        print(f"\n✓ Class mapping verification:")
        train_mapping = train_ds.class_to_idx
        report_mapping = report_ds.class_to_idx
        
        all_match = True
        for cls_name in train_ds.classes:
            if cls_name in report_mapping:
                if train_mapping[cls_name] != report_mapping[cls_name]:
                    print(f"  ❌ MISMATCH: {cls_name}")
                    print(f"     Train: {cls_name} -> {train_mapping[cls_name]}")
                    print(f"     Report: {cls_name} -> {report_mapping[cls_name]}")
                    all_match = False
                else:
                    print(f"  ✓ {cls_name}: Train={train_mapping[cls_name]}, Report={report_mapping[cls_name]}")
        
        if all_match:
            print(f"\n✓ All class mappings match correctly!")
        
        # Count images
        print(f"\n📊 Image counts in report:")
        for cls_name in report_ds.classes:
            cls_path = report_path / cls_name
            if cls_path.exists():
                images = list(cls_path.glob("*"))
                print(f"  {cls_name}: {len(images)} images")
        
    else:
        print(f"\n⚠️  No report folder found at {report_path}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "./data"
    verify_class_mapping(data_dir)



