"""
Script to run the full Oasis application
Starts both the backend API and frontend development server
"""
import subprocess
import sys
import os
import threading

def run_backend():
    """Run the FastAPI backend server"""
    try:
        print("Starting Oasis Backend API...")
        print("API documentation available at: http://localhost:8000/docs")
        os.chdir("api")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\nStopping backend server...")
    except Exception as e:
        print(f"Error running backend server: {e}")

def run_frontend():
    """Run the React frontend development server"""
    try:
        print("Starting Oasis Frontend...")
        os.chdir("../frontend")
        # Check if node_modules exists, if not install dependencies
        if not os.path.exists("node_modules"):
            print("Installing frontend dependencies...")
            subprocess.run(["npm", "install"])
        print("Frontend available at: http://localhost:3000")
        subprocess.run(["npm", "start"])
    except KeyboardInterrupt:
        print("\nStopping frontend server...")
    except Exception as e:
        print(f"Error running frontend server: {e}")

def main():
    """Main function to run both servers"""
    print("Starting Oasis Full Application...")
    print("=" * 50)
    
    # Create threads for both servers
    backend_thread = threading.Thread(target=run_backend)
    # frontend_thread = threading.Thread(target=run_frontend)
    
    # Start both threads
    backend_thread.start()
    # frontend_thread.start()
    
    # Wait for threads to complete
    backend_thread.join()
    # frontend_thread.join()
    
    print("Both servers started. Press Ctrl+C to stop.")

if __name__ == "__main__":
    main()