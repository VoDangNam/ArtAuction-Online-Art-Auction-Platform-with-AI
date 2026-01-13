# Hướng dẫn hoàn chỉnh - AI vs Human Artwork Classifier

## 📚 Mục lục

1. [Quick Start](#quick-start)
2. [Workflow chuẩn](#workflow-chuẩn)
3. [Report System - Chi tiết](#report-system---chi-tiết)
4. [Training Logic - Cách model học](#training-logic---cách-model-học)
5. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Cấu trúc folder
```
data/
├── train/
│   ├── AI/          # Ảnh AI artwork
│   └── Human/       # Ảnh Human artwork
├── val/
│   ├── AI/
│   └── Human/
└── report/          # Ảnh report tạm thời (sai nhãn)
    ├── AI/
    └── Human/
```

### 3 bước cơ bản

#### 1️⃣ Report ảnh sai
```bash
# Start API
python flask_api.py
```
- Mở frontend, upload ảnh
- Model predict sai → Click "Report as ..."
- Ảnh lưu vào `data/report/{correct_label}/`

#### 2️⃣ Verify mapping (quan trọng!)
```bash
python src/verify_class_mapping.py
```
**Output mong đợi:**
```
✓ Train: AI=0, Human=1
✓ Report: AI=0, Human=1
✓ All mappings match correctly!
```

#### 3️⃣ Train
```bash
cd src
python train.py --resume_from last
```
**Tự động:**
- ✅ Merge report vào training (weight=3x)
- ✅ Focal Loss để học kỹ hơn
- ✅ Auto-cleanup sau khi xong
- ✅ Move report → train (không duplicate)

---

## Workflow chuẩn

### Timeline đầy đủ

```
1. TEST MODEL
   └─> python flask_api.py
       └─> Model predict một số ảnh sai

2. REPORT ẢNH SAI
   └─> Click "Report as AI/Human" → Lưu vào data/report/
       ├─ Ảnh: data/report/AI/report_20251026_215530.jpg
       └─ Metadata: data/report/AI/report_20251026_215530.jpg.json

3. VERIFY MAPPING
   └─> python src/verify_class_mapping.py
       └─> Đảm bảo mapping đúng

4. TRAIN
   └─> python src/train.py --resume_from last
       ├─ Epoch 1: Học report images (weight=3x, Focal Loss)
       ├─ Epoch 2: TIẾP TỤC học report images
       ├─ ...
       └─ Epoch N: VẪN học report images
       
5. AUTO-CLEANUP
   └─> Sau khi train xong TẤT CẢ epochs
       ├─ Move data/report/AI/*   → data/train/AI/
       ├─ Move data/report/Human/* → data/train/Human/
       └─ Folder report trống (giữ structure)

6. RETEST & REPEAT
   └─> Test model mới → Report thêm → Train lại
```

---

## Report System - Chi tiết

### 1. Cách hoạt động

#### Report Endpoint
```python
# flask_api.py - Line 175-217
@app.route('/report', methods=['POST'])
def report():
    # Lưu ảnh vào data/report/{correct_label}/
    # Lưu metadata vào file .json
```

#### Merge vào Training
```python
# src/dataset.py - Line 38-53
if use_report_data and os.path.exists(f"{data_dir}/report"):
    report_ds = datasets.ImageFolder(root=f"{data_dir}/report")
    duplicated_report = ConcatDataset([report_ds] * 3)  # Duplicate 3x
    train_ds = ConcatDataset([train_ds, duplicated_report])
```

#### Cleanup sau Training
```python
# src/train.py - Line 323-338
# CHỈ SAU KHI TẤT CẢ EPOCHS XONG:
if cleanup_report:
    cleanup_report_images(data_dir)  # Move report → train
```

### 2. Tại sao ảnh report chưa bị xóa sau epoch 1?

**Câu hỏi:** Train xong epoch 1 nhưng ảnh report chưa xóa, logic này đúng không?

**Trả lời:** **ĐÚNG!** Ảnh report phải học qua **TẤT CẢ epochs!**

**Lý do:**
- Neural network cần **nhiều iterations** để học pattern
- Epoch 1: Model bị Focal Loss phạt mạnh
- Epoch 2-10: Tiếp tục phạt → Model dần học được
- Epoch 20+: Model CUỐI CÙNG nhớ được "Ảnh này = Human"

**Ví dụ:**
```
Ảnh: Oil painting (Human, nhưng model nghĩ là AI)

Epoch 1:  Focal Loss phạt mạnh → Update weights
Epoch 5:  VẪN PHẠT → Tiếp tục update
Epoch 10: Loss giảm → Model bắt đầu học được
Epoch 20: Model NHỚ "Oil = Human"

→ Không đủ 1 epoch để học!
```

**Nếu xóa sau mỗi epoch (KHÔNG ĐÚNG):**
```
Epoch 1: Học ảnh A
Epoch 2: Ảnh A mất → Model QUÊN
→ Model KHÔNG học được pattern!
```

### 3. Metadata & Error Severity

**Frontend gửi metadata về lỗi:**
```json
{
  "correct_label": "Human",
  "wrong_prediction": "AI",
  "wrong_probability": 0.85,
  "correct_probability": 0.15,
  "confidence_delta": 0.70,
  "timestamp": "20251026_215530",
  "error_severity": "high"
}
```

**Severity phân loại:**
- `high`: confidence_delta > 0.5 → weight = 6.0 (gấp 2)
- `medium`: confidence_delta > 0.2 → weight = 4.5 (gấp 1.5)  
- `low`: confidence_delta ≤ 0.2 → weight = 3.0 (base)

**Ví dụ Impact:**
```
Lỗi nhẹ (delta=0.30):
  weight = 3.0
  impact ≈ 1.26

Lỗi nghiêm trọng (delta=0.70):
  weight = 6.0
  impact ≈ 5.40
  → Cao gấp 4.3x!
```

---

## Training Logic - Cách model học

### 1. Weighted Sampling (gấp 3 lần)
```
Report images xuất hiện 3x nhiều hơn so với ảnh bình thường
→ Model thấy ảnh này thường xuyên hơn
```

### 2. Focal Loss (gấp 81-100 lần)
```
Ảnh dễ (p_t=0.9): Loss = 0.01 * log(0.9) ≈ 0.001
Ảnh khó (p_t=0.1): Loss = 0.81 * log(0.1) ≈ 1.87
→ Model bị "phạt" mạnh 1870x khi sai!
```

**Công thức:**
```
Focal Loss = (1 - p_t)^gamma * ce_loss

Với p_t = probability của nhãn đúng
     gamma = 2.0 (focusing parameter)
```

### 3. Model sẽ học gì từ ảnh khó?

**Khi loss cao → gradient cao → weights được update mạnh hơn**

**Cụ thể:**
1. **Features đặc trưng của class đúng**
   - Ví dụ: Model predict "AI" nhưng ảnh là "Human"
   - Model đang thấy: Đường nét AI, texture giả
   - Model CẦN HỌC: Brush strokes tự nhiên, imperfections
   - → Gradient "đẩy" detectors hướng tới brush strokes thật

2. **Unlearning features sai**
   - Ví dụ: Model nghĩ "smooth = AI" (sai!)
   - → Weights của neuron phát hiện "smooth" giảm mạnh

3. **Pattern recognition tốt hơn**
   - Model học: "Ảnh có X, Y, Z features KHÔNG BAO GIỜ là AI"

**Ví dụ với ConvNeXt:**
```python
# 50+ convolutional layers phát hiện: edges, textures, patterns
Ảnh report: Oil painting (Human, nhưng model nghĩ là AI)

Layer 1-10:   Phát hiện brush strokes
Layer 11-30:  Phát hiện texture của paint
Layer 31-50:  Phát hiện lighting, shadows tự nhiên

→ Gradient cao update TẤT CẢ các layers:
   - Tăng weights của detectors phát hiện "brush strokes thật"
   - Giảm weights của detectors phát hiện "smooth AI style"
   - Điều chỉnh classifier để phân biệt tốt hơn
```

### 4. Kết hợp Impact

```
Report images có impact 243-300x so với ảnh bình thường
→ Model học CỰC KỲ KỸ từ những ảnh bị dán sai
```

**Breakdown:**
- Weighted Sampling: 3x
- Focal Loss: 81-100x
- Tổng: 243-300x

---

## Troubleshooting

### Lỗi import
```bash
# Chạy từ thư mục project root
cd /path/to/project
python -m src.train
```

### Không thấy report images
- Check folder `data/report/AI/` và `data/report/Human/`
- Đảm bảo format ảnh đúng (jpg, png, etc.)

### Model không cải thiện
- Report đủ ảnh (ít nhất 10-20 ảnh mỗi class)
- Kiểm tra validation accuracy
- Thử tăng report_weight=5.0

### Verify mapping failed
```bash
# Re-run verification
python src/verify_class_mapping.py

# Output mong đợi:
✓ Train: AI=0, Human=1
✓ Report: AI=0, Human=1
✓ All mappings match correctly!
```

### Manual cleanup
```bash
# Cleanup thủ công nếu tự động fail
python src/cleanup_report_after_training.py

# Disable auto-cleanup
python src/train.py --no_cleanup_report
```

### Check progress
```bash
# Xem report images
ls data/report/AI/
ls data/report/Human/

# Xem training logs
tensorboard --logdir outputs/logs

# Xem epoch checkpoints
ls outputs/epoch_checkpoints/
```

---

## Tips & Best Practices

### ✅ Nên làm:
- Report những ảnh model **thực sự sai**
- Verify mapping trước khi train
- Retrain ngay khi có 5-10 ảnh report
- Test trên validation set
- **Để ảnh report học qua nhiều epochs** (cleanup tự động)

### ❌ Không nên:
- Report ảnh model đúng (gây confusion)
- Retrain quá nhiều với ít ảnh (overfitting)
- Ignore validation accuracy
- **Xóa ảnh report giữa chừng** (model sẽ quên)
- Skip cleanup (sẽ duplicate)

---

## Files trong project

### Core files:
- `src/train.py` - Training logic với Focal Loss
- `src/dataset.py` - Dataset với report merge
- `src/focal_loss.py` - Focal Loss implementation
- `src/model.py` - ConvNeXt architecture
- `flask_api.py` - API endpoint để report

### Utility files:
- `src/verify_class_mapping.py` - Verify AI/Human mapping
- `src/cleanup_report_after_training.py` - Auto-cleanup
- `src/evaluate.py` - Evaluate model
- `src/split_dataset.py` - Split train/val

### Documentation:
- `COMPLETE_GUIDE.md` - File này (hướng dẫn đầy đủ)
- `README.md` - Overview project

---

## Commands Reference

### Training
```bash
# Train từ đầu
python src/train.py --out_dir ./outputs

# Resume from last checkpoint
python src/train.py --resume_from last

# Resume from best
python src/train.py --resume_from best

# Custom parameters
python src/train.py --epochs 50 --batch_size 32 --lr 1e-4

# Disable auto-cleanup
python src/train.py --no_cleanup_report
```

### API & Testing
```bash
# Start API
python flask_api.py

# Verify mapping
python src/verify_class_mapping.py

# Cleanup manual
python src/cleanup_report_after_training.py
```

### Monitoring
```bash
# TensorBoard
tensorboard --logdir outputs/logs

# Check checkpoints
ls outputs/checkpoints/
ls outputs/epoch_checkpoints/
```

---

## Kết luận

**Workflow hoàn chỉnh:**
```
Report → Verify → Train → Cleanup → Repeat
```

**Key points:**
1. ✅ Ảnh report học qua TẤT CẢ epochs
2. ✅ Cleanup SAU KHI training xong
3. ✅ Auto-merge với weighted sampling
4. ✅ Focal Loss để học kỹ hơn
5. ✅ KHÔNG DUPLICATE!

**Chỉ cần:**
- Report ảnh sai
- Verify mapping
- Train → Auto-cleanup xong!
- Repeat

🎉 **Model sẽ cải thiện dần qua từng iteration!**



