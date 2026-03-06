import torch
from torch.utils.data import DataLoader, TensorDataset
from data.dataset_loader import get_client_datasets

def get_client_dataloader(client_id, batch_size=32):
    """
    Get PyTorch DataLoader for a specific client.
    """
    client_data, _ = get_client_datasets()
    
    if client_id >= len(client_data):
        raise ValueError(f"Invalid client ID: {client_id}. Only {len(client_data)} clients available.")
        
    X_c, y_c = client_data[client_id]
    
    # Convert to tensors
    X_tensor = torch.tensor(X_c, dtype=torch.float32)
    y_tensor = torch.tensor(y_c, dtype=torch.float32).view(-1, 1)
    
    dataset = TensorDataset(X_tensor, y_tensor)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    return dataloader

if __name__ == "__main__":
    dataloader = get_client_dataloader(0, 16)
    print(f"Dataloader for client 0 created with batch size 16.")
    X, y = next(iter(dataloader))
    print(f"First batch shape: X: {X.shape}, y: {y.shape}")
