import torch
import unittest
from privacy.differential_privacy import add_gaussian_noise, clip_gradient_norm
from models.model import get_model

class TestPrivacy(unittest.TestCase):
    """
    Test Differential Privacy functionality.
    """
    def test_noise_addition(self):
        params = {"weight": torch.ones(5, 5), "bias": torch.zeros(5)}
        noised_params = add_gaussian_noise(params, noise_multiplier=1.0, l2_norm_clip=1.0)
        
        # Verify noise is added
        self.assertFalse(torch.equal(params["weight"], noised_params["weight"]))
        self.assertFalse(torch.equal(params["bias"], noised_params["bias"]))
        
    def test_gradient_clipping(self):
        model = get_model(input_dim=10)
        # Create large gradient
        for param in model.parameters():
            param.grad = torch.ones_like(param) * 100.0
            
        clip_gradient_norm(model, l2_norm_clip=1.0)
        
        # Verify norm is clipped
        total_norm = torch.norm(torch.stack([torch.norm(p.grad.detach(), 2) for p in model.parameters()]), 2)
        self.assertLessEqual(total_norm.item(), 1.0 + 1e-5)

if __name__ == "__main__":
    unittest.main()
