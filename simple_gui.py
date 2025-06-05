#!/usr/bin/env python3
"""
Simple YouClip GUI - Simplified version to avoid crashes
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from utils.video_processor import VideoProcessor
from utils.time_parser import TimeParser
from utils.validators import Validators


class SimpleYouClipGUI:
    """Simplified GUI for YouClip that avoids potential crash issues"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.processor = VideoProcessor()
        self.current_video_info = None
        
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("YouClip - Simple GUI")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"700x600+{x}+{y}")
        
    def create_widgets(self):
        """Create and layout GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouClip - YouTube Video Clip Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL Section
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky="w", pady=5)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5, padx=(10, 0))
        
        # Preview button
        preview_btn = ttk.Button(main_frame, text="Preview Video Info", command=self.preview_video)
        preview_btn.grid(row=2, column=1, pady=10, sticky="w")
        
        # Time section
        time_frame = ttk.LabelFrame(main_frame, text="Time Range", padding="10")
        time_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        time_frame.columnconfigure(1, weight=1)
        time_frame.columnconfigure(3, weight=1)
        
        ttk.Label(time_frame, text="Start:").grid(row=0, column=0, sticky="w")
        self.start_var = tk.StringVar()
        ttk.Entry(time_frame, textvariable=self.start_var, width=15).grid(row=0, column=1, padx=(5, 10), sticky="w")
        
        ttk.Label(time_frame, text="End:").grid(row=0, column=2, sticky="w")
        self.end_var = tk.StringVar()
        ttk.Entry(time_frame, textvariable=self.end_var, width=15).grid(row=0, column=3, padx=(5, 0), sticky="w")
        
        ttk.Label(time_frame, text="Format: HH:MM:SS, MM:SS, or seconds", 
                 font=("Arial", 9)).grid(row=1, column=0, columnspan=4, pady=(5, 0))
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output Options", padding="10")
        output_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output file:").grid(row=0, column=0, sticky="w")
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        output_entry.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        
        browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2)
        
        # Audio only checkbox
        self.audio_only_var = tk.BooleanVar()
        audio_check = ttk.Checkbutton(output_frame, text="Audio only (MP3)", variable=self.audio_only_var)
        audio_check.grid(row=1, column=0, columnspan=3, sticky="w", pady=(10, 0))
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        download_btn = ttk.Button(button_frame, text="Download Clip", command=self.download_clip)
        download_btn.grid(row=0, column=0, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_btn.grid(row=0, column=1)
        
        # Status text
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure main frame row weights
        main_frame.rowconfigure(6, weight=1)
        
        self.log("YouClip Simple GUI started successfully!")
        
    def log(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def preview_video(self):
        """Preview video information"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        if not Validators.is_valid_youtube_url(url):
            messagebox.showerror("Error", "Invalid YouTube URL")
            return
        
        self.log("Fetching video information...")
        
        try:
            self.current_video_info = self.processor.get_video_info(url)
            info = self.current_video_info
            
            self.log(f"✅ Video: {info['title']}")
            self.log(f"Duration: {TimeParser.seconds_to_timestamp(info['duration']) if info['duration'] else 'Unknown'}")
            self.log(f"Uploader: {info['uploader']}")
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to fetch video info: {str(e)}")
    
    def browse_file(self):
        """Browse for output file"""
        audio_only = self.audio_only_var.get()
        
        if audio_only:
            filetypes = [("MP3 files", "*.mp3"), ("All files", "*.*")]
            default_ext = ".mp3"
        else:
            filetypes = [("MP4 files", "*.mp4"), ("All files", "*.*")]
            default_ext = ".mp4"
            
        filename = filedialog.asksaveasfilename(
            title="Save clip as...",
            filetypes=filetypes,
            defaultextension=default_ext
        )
        
        if filename:
            self.output_var.set(filename)
    
    def download_clip(self):
        """Download the video clip"""
        # Validate inputs
        url = self.url_var.get().strip()
        start_str = self.start_var.get().strip()
        end_str = self.end_var.get().strip()
        output_path = self.output_var.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        if not Validators.is_valid_youtube_url(url):
            messagebox.showerror("Error", "Invalid YouTube URL")
            return
            
        if not start_str or not end_str:
            messagebox.showerror("Error", "Please enter start and end times")
            return
            
        if not output_path:
            messagebox.showerror("Error", "Please specify output file")
            return
        
        # Parse times
        try:
            start_time = TimeParser.parse_time(start_str)
            end_time = TimeParser.parse_time(end_str)
            
            if start_time >= end_time:
                messagebox.showerror("Error", "End time must be greater than start time")
                return
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid time format: {str(e)}")
            return
        
        # Start download in thread
        self.log("Starting download...")
        
        def download_worker():
            try:
                def progress_callback(message):
                    self.root.after(0, lambda: self.log(f"📊 {message}"))
                
                result_path = self.processor.create_clip(
                    url, start_time, end_time, output_path, 
                    self.audio_only_var.get(), progress_callback
                )
                
                # Success
                self.root.after(0, lambda: self.download_complete(result_path))
                
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.download_error(error_msg))
        
        threading.Thread(target=download_worker, daemon=True).start()
    
    def download_complete(self, result_path):
        """Handle successful download"""
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            file_size_mb = file_size / (1024 * 1024)
            
            self.log(f"✅ Download complete!")
            self.log(f"File: {os.path.basename(result_path)}")
            self.log(f"Size: {file_size_mb:.2f} MB")
            self.log(f"Location: {os.path.dirname(result_path)}")
            
            result = messagebox.askquestion(
                "Download Complete",
                f"Clip created successfully!\n\nFile: {os.path.basename(result_path)}\nSize: {file_size_mb:.2f} MB\n\nOpen containing folder?",
                icon='question'
            )
            
            if result == 'yes':
                try:
                    if sys.platform == "darwin":  # macOS
                        subprocess.run(["open", "-R", result_path])
                    elif sys.platform == "win32":  # Windows
                        subprocess.run(["explorer", "/select,", result_path])
                    else:  # Linux
                        subprocess.run(["xdg-open", os.path.dirname(result_path)])
                except Exception as e:
                    self.log(f"Could not open folder: {e}")
        else:
            self.log("❌ Download failed - file not created")
    
    def download_error(self, error_message):
        """Handle download error"""
        self.log(f"❌ Download failed: {error_message}")
        messagebox.showerror("Download Failed", f"Error: {error_message}")
    
    def clear_all(self):
        """Clear all fields"""
        self.url_var.set("")
        self.start_var.set("")
        self.end_var.set("")
        self.output_var.set("")
        self.audio_only_var.set(False)
        self.current_video_info = None
        self.log("All fields cleared")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = SimpleYouClipGUI()
    app.run()


if __name__ == "__main__":
    main() 