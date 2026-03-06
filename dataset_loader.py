import numpy as np
from sklearn.model_selection import train_test_split
from data.preprocessing import load_and_preprocess_healthcare_data, partition_data_for_clients
from utils.config import NUM_CLIENTS

def get_client_datasets():
    """
    Get partitioned datasets for federated learning clients.
    """
    X, y = load_and_preprocess_healthcare_data()
    # Normalize features if needed
    
    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Partition train data for clients
    client_train_data = partition_data_for_clients(X_train, y_train, NUM_CLIENTS)
    
    return client_train_data, (X_test, y_test)

if __name__ == "__main__":
    client_data, test_data = get_client_datasets()
    print(f"Loaded datasets for {len(client_data)} clients.")
    print(f"Test data size: {len(test_data[0])}")
