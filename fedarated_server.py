import torch
import torch.nn as nn
from models.model import get_model
from client.client_train import FederatedClient
from server.aggregation import FedAvgAggregator, update_global_model
from data.dataset_loader import get_client_datasets
from utils.config import TRAINING_ROUNDS, NUM_CLIENTS, USE_SECURE_AGGREGATION
from utils.logger import logger

class FederatedServer:
    """
    Central Server orchestrating federated learning.
    """
    def __init__(self, num_clients=NUM_CLIENTS):
        self.global_model = get_model()
        self.num_clients = num_clients
        self.clients = [FederatedClient(client_id=i) for i in range(num_clients)]
        self.aggregator = FedAvgAggregator(num_clients)
        
        # Load global test data
        _, (X_test, y_test) = get_client_datasets()
        self.X_test = torch.tensor(X_test, dtype=torch.float32)
        self.y_test = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)
        
        # Performance history
        self.history = {
            "rounds": [],
            "accuracy": [],
            "loss": [],
            "privacy_noise": []
        }
        
    def evaluate(self):
        """
        Evaluate logic to assess the performance of the current global model.
        """
        self.global_model.eval()
        with torch.no_grad():
            output = self.global_model(self.X_test)
            preds = (output > 0.5).float()
            accuracy = (preds == self.y_test).float().mean()
            loss_fn = nn.BCELoss()
            loss = loss_fn(output, self.y_test).item()
            
        return accuracy.item(), loss

    def run_training_rounds(self, use_dp=True):
        """
        Federated Learning training: Model initialization -> Local training -> Global model update.
        """
        logger.info(f"Starting {TRAINING_ROUNDS} Federated Learning rounds.")
        
        for r in range(TRAINING_ROUNDS):
            logger.info(f"Round {r+1}/{TRAINING_ROUNDS}: Selecting {self.num_clients} clients.")
            
            # (In reality, only a subset of clients might be selected per round)
            client_updates = []
            for i, client in enumerate(self.clients):
                client.download_global_model(self.global_model.state_dict())
                update = client.train_locally(use_dp=use_dp)
                client_updates.append(update)
                
            # Aggregate updates securely
            aggregated_update = self.aggregator.aggregate_updates(client_updates, use_secure_agg=USE_SECURE_AGGREGATION)
            
            # Update global model
            update_global_model(self.global_model, aggregated_update)
            
            # Evaluate global model
            acc, loss = self.evaluate()
            self.history["rounds"].append(r+1)
            self.history["accuracy"].append(acc)
            self.history["loss"].append(loss)
            self.history["privacy_noise"].append(0.5 if use_dp else 0.0) # Placeholder for noise scale visualization
            
            logger.info(f"End of Round {r+1}: Accuracy={acc:.4f}, Loss={loss:.4f}")
            
        logger.info("Federated Training complete.")
        return self.history

if __name__ == "__main__":
    server = FederatedServer()
    history = server.run_training_rounds(use_dp=True)
    print("Training history recorded.")
