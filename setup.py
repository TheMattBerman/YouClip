#!/usr/bin/env python3
"""
YouClip Setup Script
Automates installation and testing of YouClip
"""

import subprocess
import sys
import os
from pathlib import Path


def print_step(message):
    """Print a step message"""
    print(f"\n🔧 {message}")


def print_success(message):
    """Print success message"""
    print(f"✅ {message}")


def print_error(message):
    """Print error message"""
    print(f"❌ {message}")


def run_command(cmd, description):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print_success(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print_step("Checking Python version...")
    
    if sys.version_info < (3, 7):
        print_error("Python 3.7 or higher is required")
        return False
    
    print_success(f"Python {sys.version.split()[0]} is compatible")
    return True


def check_ffmpeg():
    """Check if ffmpeg is installed"""
    print_step("Checking ffmpeg installation...")
    
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print_success("ffmpeg is installed and available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("ffmpeg is not installed or not in PATH")
        print("\n📋 FFmpeg Installation Instructions:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print_step("Installing Python dependencies...")
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Dependency installation"
    )


def run_tests():
    """Run the test suite"""
    print_step("Running test suite...")
    
    return run_command(
        f"{sys.executable} test_youclip.py",
        "Test suite"
    )


def make_executable():
    """Make scripts executable on Unix systems"""
    if os.name != 'nt':  # Not Windows
        print_step("Making scripts executable...")
        
        scripts = ['youclip.py', 'youclip_gui.py', 'launch_gui.py', 'examples/batch_example.sh']
        for script in scripts:
            if Path(script).exists():
                os.chmod(script, 0o755)
        
        print_success("Scripts made executable")


def main():
    """Main setup function"""
    print("YouClip Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    ffmpeg_available = check_ffmpeg()
    
    # Install dependencies
    if not install_dependencies():
        print_error("Failed to install dependencies")
        sys.exit(1)
    
    # Make scripts executable
    make_executable()
    
    # Run tests
    if not run_tests():
        print_error("Tests failed")
        sys.exit(1)
    
    # Final status
    print("\n" + "=" * 50)
    print("🎉 YouClip Setup Complete!")
    
    if ffmpeg_available:
        print("\n✅ YouClip is ready to use!")
        print("\nQuick start:")
        print("  python3 youclip.py  # Interactive mode")
        print("  python3 youclip.py --help  # See all options")
    else:
        print("\n⚠️  YouClip is installed but ffmpeg is missing.")
        print("Please install ffmpeg before using YouClip.")
    
    print("\n📚 See README.md for detailed usage instructions.")


if __name__ == '__main__':
    main() 