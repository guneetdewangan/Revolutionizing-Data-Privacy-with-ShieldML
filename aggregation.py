import torch
from privacy.secure_aggregation import SecureAggregator
from utils.logger import logger

class FedAvgAggregator:
    """
    Standard Federated Averaging implementation.
    """
    def __init__(self, num_clients):
        self.num_clients = num_clients
        self.secure_aggregator = SecureAggregator(num_clients)
        
    def aggregate_updates(self, client_updates, use_secure_agg=True):
        """
        Aggregate local updates from clients using FedAvg.
        """
        if use_secure_agg:
            logger.info("Using Secure Aggregation for model update.")
            return self.secure_aggregator.secure_sum(client_updates)
            
        # Standard average if not secure
        aggregated_update = {}
        for update in client_updates:
            for name, param in update.items():
                if name not in aggregated_update:
                    aggregated_update[name] = param.clone()
                else:
                    aggregated_update[name] += param
                    
        num_clients = len(client_updates)
        for name in aggregated_update:
            aggregated_update[name] /= num_clients
            
        return aggregated_update

def update_global_model(global_model, aggregated_update):
    """
    Apply aggregated update to the global model parameters.
    """
    global_model.load_state_dict(aggregated_update)
    return global_model

if __name__ == "__main__":
    from models.model import get_model
    model = get_model()
    aggregator = FedAvgAggregator(5)
    
    # Simulate updates
    updates = [model.state_dict() for _ in range(5)]
    new_weights = aggregator.aggregate_updates(updates)
    update_global_model(model, new_weights)
    print("Global model updated.")
