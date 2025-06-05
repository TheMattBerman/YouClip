#!/usr/bin/env python3
"""
YouClip GUI Launcher
Simple launcher for the YouClip GUI with error handling
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available"""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter (usually comes with Python)")
    
    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp")
    
    return missing

def main():
    """Main launcher function"""
    # Check if we're in the right directory
    if not Path("youclip_gui.py").exists():
        print("❌ Error: youclip_gui.py not found in current directory")
        print("Please run this launcher from the YouClip project directory")
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print("❌ Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nPlease install missing dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check ffmpeg
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Warning: ffmpeg not found")
        print("YouClip GUI will start but downloads will fail without ffmpeg")
        print("Install ffmpeg: https://ffmpeg.org/download.html")
        
        response = input("\nContinue anyway? (y/N): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    # Launch GUI
    print("🚀 Launching YouClip GUI...")
    try:
        from youclip_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 