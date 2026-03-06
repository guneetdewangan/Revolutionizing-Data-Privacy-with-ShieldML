import torch
import torch.nn as nn
import torch.optim as optim
from models.model import get_model
from client.local_dataset_loader import get_client_dataloader
from privacy.differential_privacy import add_gaussian_noise, clip_gradient_norm
from utils.config import LOCAL_EPOCHS, LEARNING_RATE, DP_NOISE_MULTIPLIER, DP_L2_NORM_CLIP
from utils.logger import logger

class FederatedClient:
    """
    Simulated Federated Learning client.
    """
    def __init__(self, client_id):
        self.client_id = client_id
        self.local_model = get_model()
        self.dataloader = get_client_dataloader(client_id)
        self.criterion = nn.BCELoss()
        self.optimizer = optim.SGD(self.local_model.parameters(), lr=LEARNING_RATE)
        
    def download_global_model(self, global_model_state_dict):
        """
        Download the global model state dictionary.
        """
        logger.info(f"Client {self.client_id} downloading global model weights.")
        self.local_model.load_state_dict(global_model_state_dict)
        
    def train_locally(self, use_dp=True):
        """
        Local model training on the client's dataset.
        If use_dp=True, Differential Privacy is applied during/after training.
        """
        logger.info(f"Client {self.client_id} starting local training for {LOCAL_EPOCHS} epochs.")
        
        self.local_model.train()
        for epoch in range(LOCAL_EPOCHS):
            epoch_loss = 0.0
            for X, y in self.dataloader:
                self.optimizer.zero_grad()
                output = self.local_model(X)
                loss = self.criterion(output, y)
                loss.backward()
                
                # Apply DP: Gradient Clipping
                if use_dp:
                    clip_gradient_norm(self.local_model, DP_L2_NORM_CLIP)
                
                self.optimizer.step()
                epoch_loss += loss.item()
                
            avg_loss = epoch_loss / len(self.dataloader)
            logger.info(f"Client {self.client_id} - Epoch {epoch+1}/{LOCAL_EPOCHS}, Loss: {avg_loss:.4f}")
            
        # Apply DP: Add noise to final weights
        local_update = self.local_model.state_dict()
        if use_dp:
            logger.info(f"Client {self.client_id} applying DP noise to local update.")
            local_update = add_gaussian_noise(local_update, DP_NOISE_MULTIPLIER, DP_L2_NORM_CLIP)
            
        return local_update

if __name__ == "__main__":
    from models.model import get_model
    global_model = get_model()
    
    client = FederatedClient(client_id=0)
    client.download_global_model(global_model.state_dict())
    update = client.train_locally(use_dp=True)
    print(f"Client update generated (with noise).")
