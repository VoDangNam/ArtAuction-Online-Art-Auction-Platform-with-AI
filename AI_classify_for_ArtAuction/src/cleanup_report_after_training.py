"""
Script để cleanup ảnh report sau khi training xong.
Sau khi train xong, ảnh report sẽ được move vào data/train/ để thành ảnh train chính thức.
Folder report sẽ được xóa để trống cho lần report tiếp theo.
"""
import os
import shutil
from pathlib import Path

def cleanup_report_images(data_dir="./data"):
    """Move report images vào train folder và xóa folder report"""
    data_path = Path(data_dir)
    report_dir = data_path / "report"
    train_dir = data_path / "train"
    
    if not report_dir.exists():
        print("No report folder found. Nothing to cleanup.")
        return 0
    
    moved_count = 0
    
    # Move từ report/AI/ sang train/AI/
    ai_report = report_dir / "AI"
    ai_train = train_dir / "AI"
    
    if ai_report.exists() and ai_train.exists():
        # Chỉ lấy image files, không lấy JSON files
        ai_files = [f for f in ai_report.glob("*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff']]
        print(f"Moving {len(ai_files)} AI report images to train/AI/...")
        for f in ai_files:
            dst = ai_train / f.name
            # Nếu file đã tồn tại, đổi tên
            if dst.exists():
                counter = 1
                name_parts = f.stem.rsplit('_', 1)
                new_name = f"{name_parts[0]}_r{counter}{f.suffix}"
                dst = ai_train / new_name
                while dst.exists():
                    counter += 1
                    new_name = f"{name_parts[0]}_r{counter}{f.suffix}"
                    dst = ai_train / new_name
            shutil.move(str(f), str(dst))
            moved_count += 1
        
        # Xóa tất cả JSON metadata files
        json_files = list(ai_report.glob("*.json"))
        for json_file in json_files:
            json_file.unlink()
        if json_files:
            print(f"  Deleted {len(json_files)} JSON metadata files from report/AI/")
    
    # Move từ report/Human/ sang train/Human/
    human_report = report_dir / "Human"
    human_train = train_dir / "Human"
    
    if human_report.exists() and human_train.exists():
        # Chỉ lấy image files, không lấy JSON files
        human_files = [f for f in human_report.glob("*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff']]
        print(f"Moving {len(human_files)} Human report images to train/Human/...")
        for f in human_files:
            dst = human_train / f.name
            # Nếu file đã tồn tại, đổi tên
            if dst.exists():
                counter = 1
                name_parts = f.stem.rsplit('_', 1)
                new_name = f"{name_parts[0]}_r{counter}{f.suffix}"
                dst = human_train / new_name
                while dst.exists():
                    counter += 1
                    new_name = f"{name_parts[0]}_r{counter}{f.suffix}"
                    dst = human_train / new_name
            shutil.move(str(f), str(dst))
            moved_count += 1
        
        # Xóa tất cả JSON metadata files
        json_files = list(human_report.glob("*.json"))
        for json_file in json_files:
            json_file.unlink()
        if json_files:
            print(f"  Deleted {len(json_files)} JSON metadata files from report/Human/")
    
    # Giữ lại folder structure (data/report/AI/ và data/report/Human/)
    # Chỉ cần đảm bảo các folder tồn tại cho lần report tiếp theo
    if report_dir.exists():
        # Giữ lại folder structure
        print("✓ Report folder structure kept for future reports")
        print(f"  Folder: {report_dir}")
        # Folder AI và Human đã trống (đã move hết ảnh)
        # Sẽ được tạo lại tự động khi có report mới
    
    print(f"✓ Moved {moved_count} report images to training data")
    return moved_count

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "./data"
    cleanup_report_images(data_dir)

