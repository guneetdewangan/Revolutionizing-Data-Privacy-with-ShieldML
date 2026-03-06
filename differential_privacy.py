import torch
import numpy as np
from utils.config import DP_NOISE_MULTIPLIER, DP_L2_NORM_CLIP

def add_gaussian_noise(parameters, noise_multiplier=DP_NOISE_MULTIPLIER, l2_norm_clip=DP_L2_NORM_CLIP):
    """
    Apply Gaussian noise to model parameters or gradients for Differential Privacy.
    noise = noise_multiplier * l2_norm_clip * standard_gaussian
    """
    noised_params = {}
    
    # Noise standard deviation
    std_dev = noise_multiplier * l2_norm_clip
    
    for name, param in parameters.items():
        noise = torch.randn(param.size()) * std_dev
        noised_params[name] = param + noise
        
    return noised_params

def clip_gradient_norm(model, l2_norm_clip=DP_L2_NORM_CLIP):
    """
    Clip model gradient norms for Differential Privacy.
    Protects against outlier influence.
    """
    torch.nn.utils.clip_grad_norm_(model.parameters(), l2_norm_clip)

def dp_noise_for_update(model_update, noise_multiplier=DP_NOISE_MULTIPLIER, l2_norm_clip=DP_L2_NORM_CLIP):
    """
    Apply DP noise to model weights/gradients before sending to server.
    """
    return add_gaussian_noise(model_update, noise_multiplier, l2_norm_clip)

if __name__ == "__main__":
    import torch.nn as nn
    model = nn.Linear(10, 1)
    params = {name: param.data for name, param in model.named_parameters()}
    
    noised_params = add_gaussian_noise(params)
    print("Noise applied.")
    for name in noised_params:
        diff = torch.norm(params[name] - noised_params[name])
        print(f"Difference in {name}: {diff.item():.4f}")
