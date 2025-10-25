"""
Setup script for Oasis
Installs dependencies and initializes the project
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies from requirements.txt"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def create_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Created data directory")

def initialize_project():
    """Initialize the project"""
    print("Initializing Oasis project...")
    
    # Create data directory
    create_data_directory()
    
    # Install dependencies
    install_dependencies()
    
    print("Project initialized successfully!")
    print("\nTo run the API server:")
    print("  python run_api.py")
    print("\nTo test the LSTM model:")
    print("  python models/test_lstm.py")
    print("\nTo update market data:")
    print("  python data/data_handler.py")
    print("\nTo run the scheduler:")
    print("  python data/scheduler.py")

if __name__ == "__main__":
    initialize_project()