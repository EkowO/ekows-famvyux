#!/usr/bin/env python3
"""
Comprehensive MovieHub Server Diagnostic and Startup Script
Diagnoses issues and starts the server with proper error handling
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_status(message, status="INFO"):
    """Print a formatted status message"""
    emoji = {"INFO": "ℹ️", "ERROR": "❌", "SUCCESS": "✅", "WARNING": "⚠️"}
    print(f"{emoji.get(status, 'ℹ️')} {message}")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_status(f"Python {version.major}.{version.minor} detected. Python 3.8+ required.", "ERROR")
        return False
    print_status(f"Python {version.major}.{version.minor}.{version.micro} - OK", "SUCCESS")
    return True

def check_working_directory():
    """Check if we're in the correct working directory"""
    current_dir = Path.cwd()
    main_py = current_dir / "main.py"
    app_dir = current_dir / "app"
    
    if not main_py.exists():
        print_status("main.py not found in current directory", "ERROR")
        return False
    
    if not app_dir.exists():
        print_status("app/ directory not found", "ERROR")
        return False
    
    print_status(f"Working directory: {current_dir}", "SUCCESS")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "fastapi", "uvicorn", "jinja2", "python-multipart", 
        "itsdangerous", "python-jose", "authlib", "httpx"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_status(f"{package} - OK", "SUCCESS")
        except ImportError:
            missing_packages.append(package)
            print_status(f"{package} - MISSING", "ERROR")
    
    if missing_packages:
        print_status(f"Missing packages: {', '.join(missing_packages)}", "ERROR")
        print_status("Run: pip install -r requirements.txt", "INFO")
        return False
    
    return True

def check_data_files():
    """Check if required data files exist"""
    base_dir = Path.cwd()
    data_files = [
        "data/get movies/all_10000_movies.json",
        "data/get movies/movie_likes.json",
        "data/get movies/watch_later.json",
        "data/get movies/users.json",
        "data/get movies/comments.json"
    ]
    
    missing_files = []
    
    for file_path in data_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
            print_status(f"{file_path} - MISSING", "ERROR")
        else:
            print_status(f"{file_path} - OK", "SUCCESS")
    
    if missing_files:
        print_status("Some data files are missing. Creating empty files...", "WARNING")
        create_missing_data_files(missing_files)
    
    return True

def create_missing_data_files(missing_files):
    """Create missing data files with default content"""
    base_dir = Path.cwd()
    
    default_content = {
        "movie_likes.json": {},
        "watch_later.json": {},
        "users.json": {},
        "comments.json": {},
        "all_10000_movies.json": []
    }
    
    for file_path in missing_files:
        full_path = base_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_name = full_path.name
        content = default_content.get(file_name, {})
        
        try:
            with open(full_path, 'w') as f:
                json.dump(content, f, indent=2)
            print_status(f"Created {file_path}", "SUCCESS")
        except Exception as e:
            print_status(f"Failed to create {file_path}: {e}", "ERROR")

def test_imports():
    """Test if the app imports correctly"""
    try:
        sys.path.insert(0, str(Path.cwd()))
        from app.config import BASE_DIR, MOVIES_FILE, LIKES_FILE
        print_status("App config import - OK", "SUCCESS")
        
        from app.routes_movies import router
        print_status("Movies router import - OK", "SUCCESS")
        
        from app.routes_auth import router as auth_router
        print_status("Auth router import - OK", "SUCCESS")
        
        return True
    except Exception as e:
        print_status(f"Import error: {e}", "ERROR")
        return False

def install_dependencies():
    """Install missing dependencies"""
    print_status("Installing dependencies...", "INFO")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_status("Dependencies installed successfully", "SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install dependencies: {e}", "ERROR")
        return False

def start_server():
    """Start the FastAPI server"""
    print_status("Starting MovieHub server...", "INFO")
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        print_status(f"Failed to start server: {e}", "ERROR")
        return False

def main():
    """Main diagnostic and startup function"""
    print("=" * 60)
    print("🎬 MovieHub Server Diagnostic & Startup")
    print("=" * 60)
    
    # Step 1: Check Python version
    print_status("Checking Python version...", "INFO")
    if not check_python_version():
        return False
    
    # Step 2: Check working directory
    print_status("Checking working directory...", "INFO")
    if not check_working_directory():
        print_status("Please navigate to the ekows-famvyux directory", "ERROR")
        return False
    
    # Step 3: Check dependencies
    print_status("Checking dependencies...", "INFO")
    if not check_dependencies():
        response = input("Install missing dependencies? (y/n): ").lower().strip()
        if response == 'y':
            if not install_dependencies():
                return False
        else:
            return False
    
    # Step 4: Check data files
    print_status("Checking data files...", "INFO")
    check_data_files()
    
    # Step 5: Test imports
    print_status("Testing imports...", "INFO")
    if not test_imports():
        return False
    
    # Step 6: Start server
    print("=" * 60)
    print_status("All checks passed! Starting server...", "SUCCESS")
    print_status("Server will be available at: http://localhost:8000", "INFO")
    print_status("Press Ctrl+C to stop the server", "INFO")
    print("=" * 60)
    
    start_server()

if __name__ == "__main__":
    main()
