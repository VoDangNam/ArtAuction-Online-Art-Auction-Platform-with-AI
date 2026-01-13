import torch
import torch.nn as nn
from torchvision.models import convnext_tiny, ConvNeXt_Tiny_Weights

def get_model(model_name="convnext_tiny", num_classes=2, pretrained=True, dropout_rate=0.2):
    if model_name == "convnext_tiny":
        weights = ConvNeXt_Tiny_Weights.DEFAULT if pretrained else None
        model = convnext_tiny(weights=weights)
        in_features = model.classifier[2].in_features
        
        # Classifier tối ưu với dropout vừa phải
        model.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),  # Global average pooling
            nn.Flatten(),  # Flatten to 1D
            nn.Dropout(dropout_rate),  # Dropout vừa phải
            nn.Linear(in_features, in_features // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate * 0.3),  # Dropout nhẹ hơn cho layer cuối
            nn.Linear(in_features // 2, num_classes)
        )
    else:
        raise ValueError(f"Model {model_name} chưa hỗ trợ")
    return model
