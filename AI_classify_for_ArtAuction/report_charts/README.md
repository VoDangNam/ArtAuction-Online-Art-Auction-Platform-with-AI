# Report Charts - Visualization Gallery

Thư mục này chứa các biểu đồ visualization cho báo cáo AI vs Human Artwork Classification.

## 📊 Danh Sách Biểu Đồ

### 1. accuracy_progress.png
**Training and Validation Accuracy Progress**
- Training accuracy (màu xanh)
- Validation accuracy (màu đỏ)
- Shows improvement từ epoch 11 → 24
- Best validation: 99.48% (Epoch 18 & 20)

### 2. loss_progress.png
**Training and Validation Loss Progress**
- Training loss (màu xanh)
- Validation loss (màu đỏ)
- Shows convergence
- Final loss rất thấp (< 0.01)

### 3. overfitting_analysis.png
**Overfitting Analysis: Train-Validation Gap**
- Gap = Train Acc - Val Acc
- Gap < 1% → Healthy model
- Spike ở epoch 16 (sau đó recover)

### 4. performance_summary.png
**Model Performance Summary**
- 4 metrics: Best Train/Val, Final Train/Val
- Bar chart dễ nhìn
- Shows consistency

### 5. learning_rate_schedule.png
**Learning Rate Schedule (ReduceLROnPlateau)**
- Learning rate decay over epochs
- 1e-4 → 3e-5 (epoch 17)
- Log scale cho dễ nhìn

### 6. dataset_distribution.png
**Dataset Distribution**
- Training: AI (57,910) vs Human (62,911)
- Validation: AI (17,468) vs Human (18,243)
- Total: 156,532 images

### 7. model_architecture.png
**ConvNeXt-Tiny Architecture Diagram**
- Input → Stem → Stages 1-4 → Classifier → Output
- Shows channels và blocks ở mỗi stage
- 28M parameters total

## 🔄 Regenerate Charts

Nếu cần tạo lại biểu đồ:

```bash
python generate_report_visualizations.py
```

Script sẽ:
1. Đọc metrics từ `outputs/epoch_checkpoints/`
2. Generate 7 charts
3. Save vào folder `report_charts/`

## 📐 Thông Số Kỹ Thuật

**Format:** PNG  
**Resolution:** 300 DPI  
**Size:** 
- Regular charts: 12×6 inches
- Bar charts: 10×6 inches
- Architecture: 14×10 inches

**Color Scheme:**
- Training: Blue
- Validation: Red
- Neutral: Purple/Green
- Bars: Colorful (distinctive)

## 💡 Cách Sử Dụng

### Trong Báo Cáo Markdown
```markdown
![Accuracy Progress](report_charts/accuracy_progress.png)
```

### Trong PowerPoint/Slides
1. Insert → Pictures
2. Select chart từ `report_charts/`
3. Resize as needed

### Trong LaTeX
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{report_charts/accuracy_progress.png}
\caption{Training and Validation Accuracy Progress}
\end{figure}
```

## 📊 Data Source

All charts generated from:
- **Training logs:** `outputs/epoch_checkpoints/epoch_*.pth`
- **Metrics tracked:** train_acc, val_acc, train_loss, val_loss
- **Epochs:** 11-24 (best at 18 & 20)

## 🎯 Insights Summary

**Key Takeaways:**
- ✅ Validation accuracy: 99.48% (Epoch 18 & 20)
- ✅ No overfitting (gap < 1%)
- ✅ Learning rate decay effective
- ✅ Balanced dataset
- ✅ Model converged well

---

**Generated:** 13/11/2024  
**Script:** generate_report_visualizations.py  
**Project:** AI vs Human Artwork Classification







