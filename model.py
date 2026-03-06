import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleMLModel(nn.Module):
    """
    Simple Logistic Regression model for binary classification.
    Can also be extended to a deeper neural network.
    """
    def __init__(self, input_dim=30, output_dim=1):
        super(SimpleMLModel, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)
    
    def forward(self, x):
        return torch.sigmoid(self.fc(x))

class SimpleNeuralNet(nn.Module):
    """
    Simple MLP model for binary classification.
    """
    def __init__(self, input_dim=30, hidden_dim=16, output_dim=1):
        super(SimpleNeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

def get_model(input_dim=30):
    return SimpleMLModel(input_dim)

if __name__ == "__main__":
    model = get_model()
    print(model)
    dummy_input = torch.randn(1, 30)
    output = model(dummy_input)
    print(f"Output shape: {output.shape}")
