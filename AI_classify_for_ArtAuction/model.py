import torch.nn as nn
from torchvision.models import convnext_tiny, ConvNeXt_Tiny_Weights


def get_model(
    model_name: str = "convnext_tiny",
    num_classes: int = 27,
    pretrained: bool = True,
    dropout_rate: float = 0.2,
) -> nn.Module:
    if model_name != "convnext_tiny":
        raise ValueError(f"Model {model_name} is not supported in this reference implementation.")

    weights = ConvNeXt_Tiny_Weights.DEFAULT if pretrained else None
    model = convnext_tiny(weights=weights)
    in_features = model.classifier[2].in_features

    # Custom classifier head cho style classification
    model.classifier = nn.Sequential(
        nn.AdaptiveAvgPool2d((1, 1)),
        nn.Flatten(),
        nn.Dropout(dropout_rate),
        nn.Linear(in_features, in_features // 2),
        nn.ReLU(inplace=True),
        nn.Dropout(dropout_rate * 0.3),
        nn.Linear(in_features // 2, num_classes),
    )

    return model
