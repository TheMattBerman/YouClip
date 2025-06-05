#!/usr/bin/env python3
"""
YouClip GUI - Graphical User Interface for YouTube Video Clip Downloader
A modern, user-friendly interface for extracting clips from YouTube videos
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from utils.video_processor import VideoProcessor
from utils.time_parser import TimeParser
from utils.validators import Validators


class ModernStyle:
    """Modern color scheme and styling constants"""
    # Colors
    BG_PRIMARY = "#f8f9fa"
    BG_SECONDARY = "#ffffff"
    BG_ACCENT = "#e9ecef"
    
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#6c757d"
    TEXT_SUCCESS = "#28a745"
    TEXT_ERROR = "#dc3545"
    TEXT_WARNING = "#ffc107"
    
    ACCENT_COLOR = "#007bff"
    ACCENT_HOVER = "#0056b3"
    
    # Fonts
    FONT_MAIN = ("Segoe UI", 10)
    FONT_HEADING = ("Segoe UI", 12, "bold")
    FONT_SMALL = ("Segoe UI", 8)


class YouTubeClipGUI:
    """Main GUI application for YouClip"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.processor = VideoProcessor()
        self.current_video_info = None
        self.download_thread = None
        
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("YouClip - YouTube Video Clip Downloader")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Configure window background
        self.root.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
        
        # Set window icon (if available)
        try:
            # You can add an icon file here
            pass
        except:
            pass
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="YouClip", 
            font=("Segoe UI", 24, "bold"),
            foreground=ModernStyle.ACCENT_COLOR
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Download specific clips from YouTube videos",
            font=ModernStyle.FONT_MAIN,
            foreground=ModernStyle.TEXT_SECONDARY
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # URL Section
        self.create_url_section(main_frame, row=2)
        
        # Video Info Section
        self.create_video_info_section(main_frame, row=3)
        
        # Time Range Section
        self.create_time_section(main_frame, row=4)
        
        # Output Options Section
        self.create_output_section(main_frame, row=5)
        
        # Action Buttons
        self.create_action_buttons(main_frame, row=6)
        
        # Progress Section
        self.create_progress_section(main_frame, row=7)
        
        # Status/Log Section
        self.create_status_section(main_frame, row=8)
    
    def create_url_section(self, parent, row):
        """Create URL input section"""
        # Section frame
        url_frame = ttk.LabelFrame(parent, text="YouTube Video URL", padding="10")
        url_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        url_frame.columnconfigure(1, weight=1)
        
        # URL entry
        ttk.Label(url_frame, text="URL:", font=ModernStyle.FONT_MAIN).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=ModernStyle.FONT_MAIN)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        
        # Validate and preview buttons
        button_frame = ttk.Frame(url_frame)
        button_frame.grid(row=0, column=2, sticky="e")
        
        self.validate_btn = ttk.Button(
            button_frame, 
            text="Validate", 
            command=self.validate_url,
            width=10
        )
        self.validate_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.preview_btn = ttk.Button(
            button_frame, 
            text="Preview", 
            command=self.preview_video,
            width=10,
            state="disabled"
        )
        self.preview_btn.grid(row=0, column=1)
        
        # URL status
        self.url_status_var = tk.StringVar()
        self.url_status_label = ttk.Label(
            url_frame, 
            textvariable=self.url_status_var,
            font=ModernStyle.FONT_SMALL
        )
        self.url_status_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))
    
    def create_video_info_section(self, parent, row):
        """Create video information display section"""
        self.info_frame = ttk.LabelFrame(parent, text="Video Information", padding="10")
        self.info_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        self.info_frame.columnconfigure(1, weight=1)
        
        # Initially hidden
        self.info_frame.grid_remove()
        
        # Video info labels
        self.title_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.uploader_var = tk.StringVar()
        
        info_labels = [
            ("Title:", self.title_var),
            ("Duration:", self.duration_var),
            ("Uploader:", self.uploader_var)
        ]
        
        for i, (label_text, var) in enumerate(info_labels):
            ttk.Label(self.info_frame, text=label_text, font=ModernStyle.FONT_MAIN).grid(
                row=i, column=0, sticky="w", padx=(0, 10), pady=2
            )
            ttk.Label(self.info_frame, textvariable=var, font=ModernStyle.FONT_MAIN).grid(
                row=i, column=1, sticky="w", pady=2
            )
    
    def create_time_section(self, parent, row):
        """Create time range input section"""
        time_frame = ttk.LabelFrame(parent, text="Time Range", padding="10")
        time_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        time_frame.columnconfigure(1, weight=1)
        time_frame.columnconfigure(3, weight=1)
        
        # Start time
        ttk.Label(time_frame, text="Start:", font=ModernStyle.FONT_MAIN).grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.start_time_var = tk.StringVar()
        self.start_entry = ttk.Entry(time_frame, textvariable=self.start_time_var, width=15)
        self.start_entry.grid(row=0, column=1, sticky="w", padx=(0, 20))
        self.start_entry.bind('<KeyRelease>', self.on_time_change)
        
        # End time
        ttk.Label(time_frame, text="End:", font=ModernStyle.FONT_MAIN).grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.end_time_var = tk.StringVar()
        self.end_entry = ttk.Entry(time_frame, textvariable=self.end_time_var, width=15)
        self.end_entry.grid(row=0, column=3, sticky="w")
        self.end_entry.bind('<KeyRelease>', self.on_time_change)
        
        # Time format help
        time_help = ttk.Label(
            time_frame, 
            text="Formats: HH:MM:SS, MM:SS, or seconds (e.g., 90, 1:30, 0:01:30)",
            font=ModernStyle.FONT_SMALL,
            foreground=ModernStyle.TEXT_SECONDARY
        )
        time_help.grid(row=1, column=0, columnspan=4, sticky="w", pady=(5, 0))
        
        # Time validation status
        self.time_status_var = tk.StringVar()
        self.time_status_label = ttk.Label(
            time_frame,
            textvariable=self.time_status_var,
            font=ModernStyle.FONT_SMALL
        )
        self.time_status_label.grid(row=2, column=0, columnspan=4, sticky="w", pady=(2, 0))
    
    def create_output_section(self, parent, row):
        """Create output options section"""
        output_frame = ttk.LabelFrame(parent, text="Output Options", padding="10")
        output_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        output_frame.columnconfigure(1, weight=1)
        
        # Output type
        ttk.Label(output_frame, text="Type:", font=ModernStyle.FONT_MAIN).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.output_type_var = tk.StringVar(value="video")
        type_frame = ttk.Frame(output_frame)
        type_frame.grid(row=0, column=1, sticky="w", pady=(0, 10))
        
        ttk.Radiobutton(
            type_frame, text="Video (MP4)", 
            variable=self.output_type_var, value="video"
        ).grid(row=0, column=0, padx=(0, 20))
        
        ttk.Radiobutton(
            type_frame, text="Audio Only (MP3)", 
            variable=self.output_type_var, value="audio"
        ).grid(row=0, column=1)
        
        # Output filename
        ttk.Label(output_frame, text="Filename:", font=ModernStyle.FONT_MAIN).grid(row=1, column=0, sticky="w", padx=(0, 10))
        
        filename_frame = ttk.Frame(output_frame)
        filename_frame.grid(row=1, column=1, columnspan=2, sticky="ew")
        filename_frame.columnconfigure(0, weight=1)
        
        self.filename_var = tk.StringVar()
        self.filename_entry = ttk.Entry(filename_frame, textvariable=self.filename_var)
        self.filename_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.browse_btn = ttk.Button(
            filename_frame, 
            text="Browse...", 
            command=self.browse_output_file,
            width=12
        )
        self.browse_btn.grid(row=0, column=1)
        
        # Auto-generate checkbox
        self.auto_filename_var = tk.BooleanVar(value=True)
        auto_check = ttk.Checkbutton(
            output_frame,
            text="Auto-generate filename from video title",
            variable=self.auto_filename_var,
            command=self.on_auto_filename_change
        )
        auto_check.grid(row=2, column=1, sticky="w", pady=(5, 0))
    
    def create_action_buttons(self, parent, row):
        """Create main action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(10, 15))
        
        # Download button
        self.download_btn = ttk.Button(
            button_frame,
            text="Download Clip",
            command=self.start_download,
            style="Accent.TButton"
        )
        self.download_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Cancel button
        self.cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_download,
            state="disabled"
        )
        self.cancel_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Clear button
        self.clear_btn = ttk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all
        )
        self.clear_btn.grid(row=0, column=2)
    
    def create_progress_section(self, parent, row):
        """Create progress tracking section"""
        self.progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        self.progress_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        self.progress_frame.columnconfigure(0, weight=1)
        
        # Initially hidden
        self.progress_frame.grid_remove()
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            mode='indeterminate'
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        # Progress status
        self.progress_status_var = tk.StringVar()
        self.progress_status_label = ttk.Label(
            self.progress_frame,
            textvariable=self.progress_status_var,
            font=ModernStyle.FONT_SMALL
        )
        self.progress_status_label.grid(row=1, column=0, sticky="w")
    
    def create_status_section(self, parent, row):
        """Create status/log section"""
        status_frame = ttk.LabelFrame(parent, text="Status Log", padding="10")
        status_frame.grid(row=row, column=0, columnspan=3, sticky="nsew", pady=(0, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # Configure main frame to expand this section
        parent.rowconfigure(row, weight=1)
        
        # Status text area
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=8,
            wrap=tk.WORD,
            font=ModernStyle.FONT_SMALL,
            state=tk.DISABLED
        )
        self.status_text.grid(row=0, column=0, sticky="nsew")
        
        # Add initial message
        self.log_message("YouClip GUI ready! Enter a YouTube URL to begin.", "info")
    
    def setup_styles(self):
        """Configure custom styles"""
        style = ttk.Style()
        
        # Configure accent button style
        style.configure(
            "Accent.TButton",
            font=ModernStyle.FONT_HEADING
        )
    
    def on_url_change(self, event=None):
        """Handle URL input changes"""
        url = self.url_var.get().strip()
        
        if not url:
            self.url_status_var.set("")
            self.preview_btn.configure(state="disabled")
            return
        
        # Validate URL
        if Validators.is_valid_youtube_url(url):
            self.url_status_var.set("✅ Valid YouTube URL")
            self.preview_btn.configure(state="normal")
        else:
            self.url_status_var.set("❌ Invalid YouTube URL")
            self.preview_btn.configure(state="disabled")
    
    def on_time_change(self, event=None):
        """Handle time input changes"""
        start_str = self.start_time_var.get().strip()
        end_str = self.end_time_var.get().strip()
        
        if not start_str or not end_str:
            self.time_status_var.set("")
            return
        
        try:
            start_time = TimeParser.parse_time(start_str)
            end_time = TimeParser.parse_time(end_str)
            
            if start_time >= end_time:
                self.time_status_var.set("❌ End time must be greater than start time")
                return
            
            duration = end_time - start_time
            duration_str = TimeParser.seconds_to_timestamp(duration)
            self.time_status_var.set(f"✅ Clip duration: {duration_str}")
            
            # Update filename if auto-generate is enabled
            if self.auto_filename_var.get() and self.current_video_info:
                self.update_auto_filename()
            
        except ValueError as e:
            self.time_status_var.set(f"❌ {str(e)}")
    
    def on_auto_filename_change(self):
        """Handle auto-filename checkbox change"""
        if self.auto_filename_var.get():
            self.filename_entry.configure(state="disabled")
            self.browse_btn.configure(state="disabled")
            if self.current_video_info:
                self.update_auto_filename()
        else:
            self.filename_entry.configure(state="normal")
            self.browse_btn.configure(state="normal")
    
    def validate_url(self):
        """Validate the entered URL"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL")
            return
        
        if Validators.is_valid_youtube_url(url):
            messagebox.showinfo("Success", "Valid YouTube URL!")
            self.log_message(f"✅ Valid URL: {url}", "success")
        else:
            messagebox.showerror("Error", "Invalid YouTube URL")
            self.log_message(f"❌ Invalid URL: {url}", "error")
    
    def preview_video(self):
        """Preview video information"""
        url = self.url_var.get().strip()
        
        if not Validators.is_valid_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL first")
            return
        
        # Show progress
        self.show_progress("Fetching video information...")
        
        # Run in thread to avoid blocking UI
        def fetch_info():
            try:
                self.current_video_info = self.processor.get_video_info(url)
                
                # Update UI in main thread
                self.root.after(0, self.display_video_info)
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_error(f"Failed to fetch video info: {str(e)}"))
        
        threading.Thread(target=fetch_info, daemon=True).start()
    
    def display_video_info(self):
        """Display video information in the UI"""
        if not self.current_video_info:
            return
        
        info = self.current_video_info
        
        # Update info labels
        self.title_var.set(info.get('title', 'Unknown'))
        
        duration = info.get('duration')
        if duration:
            duration_str = TimeParser.seconds_to_timestamp(duration)
            self.duration_var.set(duration_str)
        else:
            self.duration_var.set('Unknown')
        
        self.uploader_var.set(info.get('uploader', 'Unknown'))
        
        # Show info frame
        self.info_frame.grid()
        
        # Update filename if auto-generate is enabled
        if self.auto_filename_var.get():
            self.update_auto_filename()
        
        # Hide progress
        self.hide_progress()
        
        self.log_message(f"✅ Video info loaded: {info.get('title', 'Unknown')}", "success")
    
    def update_auto_filename(self):
        """Update filename based on video info and time range"""
        if not self.current_video_info:
            return
        
        start_str = self.start_time_var.get().strip()
        end_str = self.end_time_var.get().strip()
        
        if not start_str or not end_str:
            return
        
        try:
            start_time = TimeParser.parse_time(start_str)
            end_time = TimeParser.parse_time(end_str)
            audio_only = self.output_type_var.get() == "audio"
            
            # Create suggested filename
            title = self.current_video_info.get('title', 'Unknown')
            clean_title = Validators.sanitize_filename(title)
            
            start_timestamp = TimeParser.seconds_to_timestamp(start_time).replace(':', '-')
            end_timestamp = TimeParser.seconds_to_timestamp(end_time).replace(':', '-')
            
            ext = '.mp3' if audio_only else '.mp4'
            filename = f"{clean_title}_clip_{start_timestamp}_to_{end_timestamp}{ext}"
            
            # Truncate if too long
            if len(filename) > 200:
                title_part = clean_title[:100] + "..."
                filename = f"{title_part}_clip_{start_timestamp}_to_{end_timestamp}{ext}"
            
            self.filename_var.set(filename)
            
        except ValueError:
            pass  # Invalid time format, ignore
    
    def browse_output_file(self):
        """Browse for output file location"""
        audio_only = self.output_type_var.get() == "audio"
        
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
            self.filename_var.set(filename)
    
    def start_download(self):
        """Start the download process"""
        # Validate inputs
        if not self.validate_inputs():
            return
        
        # Disable download button and enable cancel
        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        
        # Show progress
        self.show_progress("Starting download...")
        
        # Start download thread
        self.download_thread = threading.Thread(target=self.download_worker, daemon=True)
        self.download_thread.start()
    
    def download_worker(self):
        """Worker thread for download process"""
        try:
            url = self.url_var.get().strip()
            start_str = self.start_time_var.get().strip()
            end_str = self.end_time_var.get().strip()
            output_path = self.filename_var.get().strip()
            audio_only = self.output_type_var.get() == "audio"
            
            # Parse times
            start_time = TimeParser.parse_time(start_str)
            end_time = TimeParser.parse_time(end_str)
            
            # Progress callback
            def progress_callback(message):
                self.root.after(0, lambda: self.update_progress_status(message))
            
            # Create clip
            result_path = self.processor.create_clip(
                url, start_time, end_time, output_path, audio_only, progress_callback
            )
            
            # Success
            self.root.after(0, lambda: self.download_complete(result_path))
            
        except Exception as e:
            self.root.after(0, lambda: self.handle_error(f"Download failed: {str(e)}"))
    
    def download_complete(self, result_path):
        """Handle successful download completion"""
        # Hide progress
        self.hide_progress()
        
        # Re-enable buttons
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        
        # Show success message
        file_size = os.path.getsize(result_path) if os.path.exists(result_path) else 0
        file_size_mb = file_size / (1024 * 1024)
        
        success_msg = f"✅ Clip created successfully!\n\nFile: {os.path.basename(result_path)}\nSize: {file_size_mb:.2f} MB\nLocation: {os.path.dirname(result_path)}"
        
        result = messagebox.askquestion(
            "Download Complete",
            f"{success_msg}\n\nWould you like to open the containing folder?",
            icon='question'
        )
        
        if result == 'yes':
            self.open_file_location(result_path)
        
        self.log_message(f"✅ Download complete: {result_path}", "success")
    
    def cancel_download(self):
        """Cancel the current download"""
        # Note: This is a simplified cancel - in a production app you'd need 
        # more sophisticated thread management
        self.hide_progress()
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        
        self.log_message("⚠️ Download cancelled by user", "warning")
    
    def validate_inputs(self):
        """Validate all user inputs before download"""
        # Check URL
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return False
        
        if not Validators.is_valid_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return False
        
        # Check times
        start_str = self.start_time_var.get().strip()
        end_str = self.end_time_var.get().strip()
        
        if not start_str or not end_str:
            messagebox.showerror("Error", "Please enter both start and end times")
            return False
        
        try:
            start_time = TimeParser.parse_time(start_str)
            end_time = TimeParser.parse_time(end_str)
            
            if start_time >= end_time:
                messagebox.showerror("Error", "End time must be greater than start time")
                return False
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid time format: {str(e)}")
            return False
        
        # Check filename
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showerror("Error", "Please specify an output filename")
            return False
        
        return True
    
    def clear_all(self):
        """Clear all inputs"""
        self.url_var.set("")
        self.start_time_var.set("")
        self.end_time_var.set("")
        self.filename_var.set("")
        self.url_status_var.set("")
        self.time_status_var.set("")
        
        # Hide info frame
        self.info_frame.grid_remove()
        self.current_video_info = None
        
        # Reset buttons
        self.preview_btn.configure(state="disabled")
        
        self.log_message("🔄 All fields cleared", "info")
    
    def show_progress(self, message):
        """Show progress section with message"""
        self.progress_frame.grid()
        self.progress_bar.start()
        self.progress_status_var.set(message)
    
    def hide_progress(self):
        """Hide progress section"""
        self.progress_bar.stop()
        self.progress_frame.grid_remove()
    
    def update_progress_status(self, message):
        """Update progress status message"""
        self.progress_status_var.set(message)
    
    def handle_error(self, error_message):
        """Handle and display errors"""
        self.hide_progress()
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        
        messagebox.showerror("Error", error_message)
        self.log_message(f"❌ {error_message}", "error")
    
    def log_message(self, message, level="info"):
        """Add message to status log"""
        self.status_text.configure(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, full_message)
        self.status_text.see(tk.END)
        self.status_text.configure(state=tk.DISABLED)
    
    def open_file_location(self, file_path):
        """Open file location in system file manager"""
        try:
            if sys.platform == "win32":
                os.startfile(os.path.dirname(file_path))
            elif sys.platform == "darwin":
                subprocess.run(["open", os.path.dirname(file_path)])
            else:
                subprocess.run(["xdg-open", os.path.dirname(file_path)])
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not open file location: {str(e)}")
    
    def run(self):
        """Start the GUI application"""
        # Check dependencies before starting
        success, message = VideoProcessor.check_dependencies()
        if not success:
            messagebox.showerror(
                "Missing Dependencies",
                f"{message}\n\nPlease install the required dependencies before using YouClip GUI."
            )
            return
        
        self.log_message("✅ All dependencies available", "success")
        
        # Start the main loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


def main():
    """Main entry point for GUI application"""
    try:
        app = YouTubeClipGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Failed to start YouClip GUI: {str(e)}")


if __name__ == '__main__':
    main() 