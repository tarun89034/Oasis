"""
Script to run the Oasis API
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def run_api():
    """Run the FastAPI server"""
    try:
        # Check if we're running with gunicorn
        if os.getenv('USE_GUNICORN', 'False').lower() == 'true':
            print("Starting Oasis API server with Gunicorn...")
            subprocess.run(["gunicorn", "-c", "gunicorn.conf.py", "api.main:app"])
        else:
            # Change to the api directory
            os.chdir("api")
            print("Starting Oasis API server...")
            print("Access the API documentation at: http://localhost:8000/docs")
            subprocess.run(["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\nShutting down API server...")
    except Exception as e:
        print(f"Error running API server: {e}")

if __name__ == "__main__":
    # Install dependencies if needed
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        install_dependencies()
    
    # Run the API
    run_api()