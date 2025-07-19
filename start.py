#!/usr/bin/env python3
"""
Startup script for the Ecommerce API
This script helps with local development and testing
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import pymongo
        import pydantic
        import requests
        print("SUCCESS: All dependencies are installed")
        return True
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if not env_file.exists():
        print("WARNING: .env file not found")
        print("Please create a .env file with your MongoDB connection string:")
        print("MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ecommerce_db?retryWrites=true&w=majority")
        return False
    else:
        print("SUCCESS: .env file found")
        return True

def start_server():
    """Start the FastAPI server"""
    print("Starting Ecommerce API server...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("Base URL: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped")

def run_tests():
    """Run the test script"""
    print("Running API tests...")
    try:
        subprocess.run([sys.executable, "test_api.py"])
    except Exception as e:
        print(f"ERROR: Error running tests: {e}")

def main():
    """Main function"""
    print("Ecommerce API - Development Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check environment file
    check_env_file()
    
    print("\nOptions:")
    print("1. Start server")
    print("2. Run tests")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        start_server()
    elif choice == "2":
        run_tests()
    elif choice == "3":
        print("Starting server in background...")
        # Start server in background
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
        # Wait a bit for server to start
        import time
        time.sleep(3)
        
        # Run tests
        run_tests()
        
        # Stop server
        server_process.terminate()
        print("SUCCESS: Server stopped")
    else:
        print("ERROR: Invalid choice")

if __name__ == "__main__":
    main() 