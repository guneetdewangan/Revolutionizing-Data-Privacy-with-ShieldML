import argparse
from server.federated_server import FederatedServer
from utils.logger import logger
import matplotlib.pyplot as plt

def run_experiment(use_privacy=True):
    """
    Main experiment runner.
    """
    logger.info(f"--- Starting Experiment (Privacy={'Enabled' if use_privacy else 'Disabled'}) ---")
    
    server = FederatedServer()
    history = server.run_training_rounds(use_dp=use_privacy)
    
    # Simple plot
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history["rounds"], history["accuracy"], label=f"Privacy={use_privacy}", marker='o')
    plt.title("Accuracy vs Rounds")
    plt.ylabel("Accuracy")
    plt.xlabel("Round")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history["rounds"], history["loss"], label=f"Privacy={use_privacy}", marker='x', color='red')
    plt.title("Loss vs Rounds")
    plt.ylabel("Loss")
    plt.xlabel("Round")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"experiment_results_{'privacy' if use_privacy else 'no_privacy'}.png")
    logger.info(f"Experiment visualization saved as experiment_results_{'privacy' if use_privacy else 'no_privacy'}.png")
    
    return history

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Privacy-Preserving Federated ML Framework")
    parser.add_argument("--no-privacy", action="store_true", help="Run without Differential Privacy")
    args = parser.parse_args()
    
    run_experiment(use_privacy=not args.no_privacy)
