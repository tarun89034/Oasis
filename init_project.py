"""
Initialization script for Oasis
Sets up the entire project environment
"""
import subprocess
import sys
import os

def install_python_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Python dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python dependencies: {e}")
        return False
    return True

def install_node_dependencies():
    """Install Node.js dependencies for frontend"""
    print("Installing Node.js dependencies...")
    try:
        os.chdir("frontend")
        subprocess.check_call(["npm", "install"])
        os.chdir("..")
        print("Node.js dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Node.js dependencies: {e}")
        return False
    except FileNotFoundError:
        print("npm not found. Please install Node.js first.")
        return False
    return True

def create_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Created data directory")

def initialize_database():
    """Initialize the database"""
    print("Initializing database...")
    try:
        os.chdir("data")
        # Import and run the data handler to initialize database
        sys.path.append("..")
        from data.data_handler import DataHandler
        handler = DataHandler()
        print("Database initialized successfully!")
        os.chdir("..")
    except Exception as e:
        print(f"Error initializing database: {e}")
        os.chdir("..")
        return False
    return True

def main():
    """Main initialization function"""
    print("Initializing Oasis Project...")
    print("=" * 40)
    
    # Create data directory
    create_data_directory()
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("Failed to install Python dependencies. Exiting.")
        return
    
    # Initialize database
    if not initialize_database():
        print("Failed to initialize database. Exiting.")
        return
    
    # Install Node.js dependencies
    if not install_node_dependencies():
        print("Failed to install Node.js dependencies. You can install them later manually.")
    
    print("\nProject initialization completed!")
    print("\nTo run the application:")
    print("1. Start the backend API: python run_api.py")
    print("2. In another terminal, start the frontend: cd frontend && npm start")
    print("3. Open your browser to http://localhost:3000")

if __name__ == "__main__":
    main()