import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    """
    Focal Loss giúp model học kỹ hơn từ những ảnh bị dán nhãn sai.
    
    Focal Loss = -alpha * (1 - p_t)^gamma * log(p_t)
    
    Trong đó:
    - p_t: Probability của nhãn đúng
    - alpha: Weight cho từng class (thường cao hơn cho class ít sample hơn)
    - gamma: Focusing parameter (gamma > 0 tăng trọng số cho hard samples)
    
    Khi model dự đoán sai (p_t nhỏ), (1-p_t)^gamma sẽ tăng loss để model học mạnh hơn.
    """
    def __init__(self, alpha=None, gamma=2.0, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
    
    def forward(self, inputs, targets):
        # Compute cross entropy
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', weight=self.alpha)
        
        # Get probability of correct class
        p_t = torch.exp(-ce_loss)
        
        # Compute focal loss
        focal_loss = (1 - p_t) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss



