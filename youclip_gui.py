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


class WinampStyle:
    """Winamp-inspired color scheme and styling constants"""
    # Colors - Classic Winamp palette
    BG_PRIMARY = "#2c2c2c"      # Dark gray background
    BG_SECONDARY = "#1a1a1a"    # Darker panels
    BG_ACCENT = "#3a3a3a"       # Raised elements
    BG_SUNKEN = "#0f0f0f"       # Sunken elements
    
    # Winamp classic green LCD colors
    TEXT_PRIMARY = "#00ff00"     # Bright green
    TEXT_SECONDARY = "#00aa00"   # Dimmer green
    TEXT_LCD = "#00ff41"         # LCD green
    TEXT_SUCCESS = "#00ff00"     # Success green
    TEXT_ERROR = "#ff0000"       # Error red
    TEXT_WARNING = "#ffff00"     # Warning yellow
    
    # Accent colors
    ACCENT_COLOR = "#ff6600"     # Winamp orange
    ACCENT_HOVER = "#ff8833"     # Lighter orange
    BUTTON_ACTIVE = "#4a90e2"    # Active button blue
    
    # Border colors - More Winamp-like metallic theme
    BORDER_LIGHT = "#888888"     # Light border (metallic)
    BORDER_DARK = "#000000"      # Dark border
    BORDER_ACCENT = "#aaaaaa"    # Accent border (chrome-like)
    BORDER_CHROME_LIGHT = "#cccccc"  # Chrome highlight
    BORDER_CHROME_DARK = "#333333"   # Chrome shadow
    
    # Fonts - More retro/digital style with better readability
    FONT_MAIN = ("Courier New", 12)
    FONT_HEADING = ("Arial", 14, "bold")
    FONT_SMALL = ("Courier New", 10)
    FONT_LCD = ("Courier New", 12, "bold")  # For LCD-style displays
    FONT_TITLE = ("Arial", 20, "bold")  # For main title
    FONT_BUTTON = ("Arial", 11, "bold")  # For buttons


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
        """Configure the main window - Winamp style"""
        self.root.title("YouClip v2.1 - [Stopped] - Winamp")
        self.root.geometry("850x750")
        self.root.minsize(750, 650)
        
        # Configure window background with Winamp colors
        self.root.configure(bg=WinampStyle.BG_PRIMARY)
        
        # Try to make the window look more retro
        try:
            # Remove window decorations for more authentic look (optional)
            # self.root.overrideredirect(True)  # Uncomment for borderless
            pass
        except:
            pass
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (850 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"850x750+{x}+{y}")
        
        # Set window icon (if available)
        try:
            # You can add a Winamp-style icon file here
            pass
        except:
            pass
    
    def create_widgets(self):
        """Create and layout all GUI widgets - Winamp style"""
        # Main container with Winamp-style border effect
        main_frame = tk.Frame(
            self.root, 
            bg=WinampStyle.BG_ACCENT,
            relief="raised",
            bd=2
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Main title bar - Winamp style with metallic appearance
        title_bar = tk.Frame(
            main_frame, 
            bg=WinampStyle.BORDER_ACCENT, 
            relief="raised", 
            bd=4,
            highlightbackground=WinampStyle.BORDER_CHROME_LIGHT,
            highlightcolor=WinampStyle.BORDER_CHROME_DARK,
            highlightthickness=1
        )
        title_bar.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 0), padx=10)
        
        # Title - Winamp style with ASCII art feel
        title_label = tk.Label(
            title_bar, 
            text="░░░ YouClip v2.1 ░░░", 
            font=WinampStyle.FONT_TITLE,
            foreground=WinampStyle.ACCENT_COLOR,
            background=WinampStyle.BORDER_ACCENT
        )
        title_label.grid(row=0, column=0, pady=8)
        
        # Subtitle with retro feel
        subtitle_label = tk.Label(
            main_frame,
            text="♫ ♪ ♫ YouTube Video Clip Downloader ♫ ♪ ♫",
            font=WinampStyle.FONT_MAIN,
            foreground=WinampStyle.TEXT_LCD,
            background=WinampStyle.BG_ACCENT
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(8, 15), padx=10, sticky="ew")
        
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
        """Create URL input section - Winamp style"""
        # Section frame with Winamp styling
        url_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY, relief="groove", bd=2)
        url_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(5, 10), padx=10)
        url_frame.columnconfigure(1, weight=1)
        
        # Section title
        title_label = tk.Label(
            url_frame, 
            text="=== YOUTUBE VIDEO URL ===", 
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.ACCENT_COLOR,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(8, 5))
        
        # URL entry
        tk.Label(
            url_frame, 
            text="URL:", 
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        ).grid(row=1, column=0, sticky="w", padx=(15, 10), pady=8)
        
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            url_frame, 
            textvariable=self.url_var, 
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=2,
            insertbackground=WinampStyle.TEXT_LCD
        )
        self.url_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=8)
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        
        # Validate and preview buttons
        button_frame = tk.Frame(url_frame, bg=WinampStyle.BG_SECONDARY)
        button_frame.grid(row=1, column=2, sticky="e", padx=(0, 10))
        
        self.validate_btn = tk.Button(
            button_frame, 
            text="VALIDATE", 
            command=self.validate_url,
            width=10,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BG_ACCENT,
            fg=WinampStyle.TEXT_PRIMARY,
            relief="raised",
            bd=2,
            activebackground=WinampStyle.ACCENT_HOVER,
            activeforeground=WinampStyle.TEXT_LCD
        )
        self.validate_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.preview_btn = tk.Button(
            button_frame, 
            text="PREVIEW", 
            command=self.preview_video,
            width=10,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BG_ACCENT,
            fg=WinampStyle.TEXT_PRIMARY,
            relief="raised",
            bd=2,
            state="disabled",
            activebackground=WinampStyle.ACCENT_HOVER,
            activeforeground=WinampStyle.TEXT_LCD
        )
        self.preview_btn.grid(row=0, column=1)
        
        # URL status with LCD-style display
        self.url_status_var = tk.StringVar()
        self.url_status_label = tk.Label(
            url_frame, 
            textvariable=self.url_status_var,
            font=WinampStyle.FONT_LCD,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=1,
            anchor="w"
        )
        self.url_status_label.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(5, 8), padx=10)
    
    def create_video_info_section(self, parent, row):
        """Create video information display section - Winamp style"""
        self.info_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY, relief="groove", bd=2)
        self.info_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(5, 10), padx=10)
        self.info_frame.columnconfigure(1, weight=1)
        
        # Section title
        title_label = tk.Label(
            self.info_frame, 
            text="=== VIDEO INFORMATION ===", 
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.ACCENT_COLOR,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(8, 5))
        
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
            # Label
            tk.Label(
                self.info_frame, 
                text=label_text, 
                font=WinampStyle.FONT_MAIN,
                fg=WinampStyle.TEXT_PRIMARY,
                bg=WinampStyle.BG_SECONDARY
            ).grid(row=i+1, column=0, sticky="w", padx=(10, 10), pady=2)
            
            # Value with LCD-style display
            tk.Label(
                self.info_frame, 
                textvariable=var, 
                font=WinampStyle.FONT_LCD,
                fg=WinampStyle.TEXT_LCD,
                bg=WinampStyle.BG_SUNKEN,
                relief="sunken",
                bd=1,
                anchor="w"
            ).grid(row=i+1, column=1, sticky="ew", pady=2, padx=(0, 10))
    
    def create_time_section(self, parent, row):
        """Create time range input section - Winamp style"""
        time_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY, relief="groove", bd=2)
        time_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(5, 10), padx=10)
        time_frame.columnconfigure(1, weight=1)
        time_frame.columnconfigure(3, weight=1)
        
        # Section title
        title_label = tk.Label(
            time_frame, 
            text="=== TIME RANGE ===", 
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.ACCENT_COLOR,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(8, 10))
        
        # Start time
        tk.Label(
            time_frame, 
            text="START:", 
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        ).grid(row=1, column=0, sticky="w", padx=(10, 10))
        
        self.start_time_var = tk.StringVar()
        self.start_entry = tk.Entry(
            time_frame, 
            textvariable=self.start_time_var, 
            width=15,
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=2,
            insertbackground=WinampStyle.TEXT_LCD
        )
        self.start_entry.grid(row=1, column=1, sticky="w", padx=(0, 20))
        self.start_entry.bind('<KeyRelease>', self.on_time_change)
        
        # End time
        tk.Label(
            time_frame, 
            text="END:", 
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        ).grid(row=1, column=2, sticky="w", padx=(0, 10))
        
        self.end_time_var = tk.StringVar()
        self.end_entry = tk.Entry(
            time_frame, 
            textvariable=self.end_time_var, 
            width=15,
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=2,
            insertbackground=WinampStyle.TEXT_LCD
        )
        self.end_entry.grid(row=1, column=3, sticky="w", padx=(0, 10))
        self.end_entry.bind('<KeyRelease>', self.on_time_change)
        
        # Time format help
        time_help = tk.Label(
            time_frame, 
            text="[ Formats: HH:MM:SS, MM:SS, or seconds (e.g., 90, 1:30, 0:01:30) ]",
            font=WinampStyle.FONT_SMALL,
            fg=WinampStyle.TEXT_SECONDARY,
            bg=WinampStyle.BG_SECONDARY
        )
        time_help.grid(row=2, column=0, columnspan=4, sticky="w", pady=(5, 0), padx=10)
        
        # Time validation status with LCD display
        self.time_status_var = tk.StringVar()
        self.time_status_label = tk.Label(
            time_frame,
            textvariable=self.time_status_var,
            font=WinampStyle.FONT_LCD,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=1,
            anchor="w"
        )
        self.time_status_label.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(5, 8), padx=10)
    
    def create_output_section(self, parent, row):
        """Create output options section - Winamp style"""
        output_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY, relief="groove", bd=2)
        output_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(5, 10), padx=10)
        output_frame.columnconfigure(1, weight=1)
        
        # Section title
        title_label = tk.Label(
            output_frame, 
            text="=== OUTPUT OPTIONS ===", 
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.ACCENT_COLOR,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(8, 10))
        
        # Output type
        tk.Label(
            output_frame, 
            text="TYPE:", 
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        ).grid(row=1, column=0, sticky="w", padx=(10, 10))
        
        self.output_type_var = tk.StringVar(value="video")
        type_frame = tk.Frame(output_frame, bg=WinampStyle.BG_SECONDARY)
        type_frame.grid(row=1, column=1, sticky="w", pady=(0, 10), padx=(0, 10))
        
        tk.Radiobutton(
            type_frame, 
            text="Video (MP4)", 
            variable=self.output_type_var, 
            value="video",
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SECONDARY,
            fg=WinampStyle.TEXT_PRIMARY,
            selectcolor=WinampStyle.BG_ACCENT,
            activebackground=WinampStyle.BG_ACCENT,
            activeforeground=WinampStyle.TEXT_LCD
        ).grid(row=0, column=0, padx=(0, 20))
        
        tk.Radiobutton(
            type_frame, 
            text="Audio Only (MP3)", 
            variable=self.output_type_var, 
            value="audio",
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SECONDARY,
            fg=WinampStyle.TEXT_PRIMARY,
            selectcolor=WinampStyle.BG_ACCENT,
            activebackground=WinampStyle.BG_ACCENT,
            activeforeground=WinampStyle.TEXT_LCD
        ).grid(row=0, column=1)
        
        # Output filename
        tk.Label(
            output_frame, 
            text="FILENAME:", 
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        ).grid(row=2, column=0, sticky="w", padx=(10, 10))
        
        filename_frame = tk.Frame(output_frame, bg=WinampStyle.BG_SECONDARY)
        filename_frame.grid(row=2, column=1, columnspan=2, sticky="ew", padx=(0, 10))
        filename_frame.columnconfigure(0, weight=1)
        
        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(
            filename_frame, 
            textvariable=self.filename_var,
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=2,
            insertbackground=WinampStyle.TEXT_LCD
        )
        self.filename_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.browse_btn = tk.Button(
            filename_frame, 
            text="BROWSE...", 
            command=self.browse_output_file,
            width=12,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BG_ACCENT,
            fg=WinampStyle.TEXT_PRIMARY,
            relief="raised",
            bd=2,
            activebackground=WinampStyle.ACCENT_HOVER,
            activeforeground=WinampStyle.TEXT_LCD
        )
        self.browse_btn.grid(row=0, column=1)
        
        # Auto-generate checkbox
        self.auto_filename_var = tk.BooleanVar(value=True)
        auto_check = tk.Checkbutton(
            output_frame,
            text="[ AUTO-GENERATE FILENAME FROM VIDEO TITLE ]",
            variable=self.auto_filename_var,
            command=self.on_auto_filename_change,
            font=WinampStyle.FONT_SMALL,
            bg=WinampStyle.BG_SECONDARY,
            fg=WinampStyle.TEXT_SECONDARY,
            selectcolor=WinampStyle.BG_ACCENT,
            activebackground=WinampStyle.BG_SECONDARY,
            activeforeground=WinampStyle.TEXT_LCD
        )
        auto_check.grid(row=3, column=1, sticky="w", pady=(5, 8), padx=(0, 10))
    
    def create_action_buttons(self, parent, row):
        """Create main action buttons - Winamp style"""
        button_frame = tk.Frame(parent, bg=WinampStyle.BG_ACCENT)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(15, 15), padx=20, sticky="ew")
        
        # Center the buttons
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(4, weight=1)
        
        # Download button - main action
        self.download_btn = tk.Button(
            button_frame,
            text=">>> DOWNLOAD CLIP <<<",
            command=self.start_download,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.ACCENT_COLOR,
            fg=WinampStyle.BG_PRIMARY,
            relief="raised",
            bd=3,
            width=20,
            activebackground=WinampStyle.ACCENT_HOVER,
            activeforeground=WinampStyle.BG_PRIMARY
        )
        self.download_btn.grid(row=0, column=1, padx=10, pady=8)
        
        # Cancel button
        self.cancel_btn = tk.Button(
            button_frame,
            text="CANCEL",
            command=self.cancel_download,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.TEXT_ERROR,
            fg=WinampStyle.BG_PRIMARY,
            relief="raised",
            bd=2,
            width=12,
            state="disabled",
            activebackground="#ff3333",
            activeforeground=WinampStyle.BG_PRIMARY
        )
        self.cancel_btn.grid(row=0, column=2, padx=10, pady=8)
        
        # Clear button
        self.clear_btn = tk.Button(
            button_frame,
            text="CLEAR ALL",
            command=self.clear_all,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BG_ACCENT,
            fg=WinampStyle.TEXT_PRIMARY,
            relief="raised",
            bd=2,
            width=12,
            activebackground=WinampStyle.ACCENT_HOVER,
            activeforeground=WinampStyle.TEXT_LCD
        )
        self.clear_btn.grid(row=0, column=3, padx=10, pady=8)
    
    def create_progress_section(self, parent, row):
        """Create progress tracking section - Winamp style"""
        self.progress_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY, relief="groove", bd=2)
        self.progress_frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(5, 10), padx=10)
        self.progress_frame.columnconfigure(0, weight=1)
        
        # Section title
        title_label = tk.Label(
            self.progress_frame, 
            text="=== PROGRESS ===", 
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.ACCENT_COLOR,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, pady=(8, 5))
        
        # Initially hidden
        self.progress_frame.grid_remove()
        
        # Progress bar - Winamp style (using a frame as a fake progress bar)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Frame(
            self.progress_frame,
            bg=WinampStyle.BG_SUNKEN,
            relief="sunken",
            bd=2,
            height=20
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 5), padx=10)
        
        # Progress status with LCD display
        self.progress_status_var = tk.StringVar()
        self.progress_status_label = tk.Label(
            self.progress_frame,
            textvariable=self.progress_status_var,
            font=WinampStyle.FONT_LCD,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=1,
            anchor="w"
        )
        self.progress_status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 8))
    
    def create_status_section(self, parent, row):
        """Create status/log section - Winamp style"""
        status_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY, relief="groove", bd=2)
        status_frame.grid(row=row, column=0, columnspan=3, sticky="nsew", pady=(5, 10), padx=10)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        # Section title
        title_label = tk.Label(
            status_frame, 
            text="=== STATUS LOG ===", 
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.ACCENT_COLOR,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, pady=(8, 5))
        
        # Configure main frame to expand this section
        parent.rowconfigure(row, weight=1)
        
        # Status text area with Winamp styling
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=8,
            wrap=tk.WORD,
            font=WinampStyle.FONT_SMALL,
            bg=WinampStyle.BG_SUNKEN,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=2,
            insertbackground=WinampStyle.TEXT_LCD,
            selectbackground=WinampStyle.BG_ACCENT,
            selectforeground=WinampStyle.TEXT_LCD,
            state=tk.DISABLED
        )
        self.status_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 8))
        
        # Add initial message
        self.log_message(">>> YouClip GUI ready! Enter a YouTube URL to begin. <<<", "info")
    
    def setup_styles(self):
        """Configure custom Winamp-inspired styles"""
        style = ttk.Style()
        
        # Set the theme to something darker
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configure Winamp-style button
        style.configure(
            "Winamp.TButton",
            font=WinampStyle.FONT_MAIN,
            background=WinampStyle.BG_ACCENT,
            foreground=WinampStyle.TEXT_PRIMARY,
            borderwidth=2,
            relief="raised",
            focuscolor="none"
        )
        
        style.map(
            "Winamp.TButton",
            background=[
                ("active", WinampStyle.ACCENT_HOVER),
                ("pressed", WinampStyle.BG_SUNKEN)
            ],
            foreground=[
                ("active", WinampStyle.TEXT_LCD),
                ("pressed", WinampStyle.TEXT_LCD)
            ],
            relief=[
                ("pressed", "sunken"),
                ("active", "raised")
            ]
        )
        
        # Configure Winamp-style frame
        style.configure(
            "Winamp.TLabelFrame",
            background=WinampStyle.BG_SECONDARY,
            foreground=WinampStyle.TEXT_PRIMARY,
            borderwidth=2,
            relief="groove"
        )
        
        style.configure(
            "Winamp.TLabelFrame.Label",
            background=WinampStyle.BG_SECONDARY,
            foreground=WinampStyle.ACCENT_COLOR,
            font=WinampStyle.FONT_HEADING
        )
        
        # Configure Winamp-style entry
        style.configure(
            "Winamp.TEntry",
            fieldbackground=WinampStyle.BG_SUNKEN,
            foreground=WinampStyle.TEXT_LCD,
            borderwidth=2,
            relief="sunken",
            insertcolor=WinampStyle.TEXT_LCD
        )
        
        # Configure Winamp-style label
        style.configure(
            "Winamp.TLabel",
            background=WinampStyle.BG_SECONDARY,
            foreground=WinampStyle.TEXT_PRIMARY,
            font=WinampStyle.FONT_MAIN
        )
        
        # Configure LCD-style label for status displays
        style.configure(
            "LCD.TLabel",
            background=WinampStyle.BG_SUNKEN,
            foreground=WinampStyle.TEXT_LCD,
            font=WinampStyle.FONT_LCD,
            relief="sunken",
            borderwidth=1
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
        
        self.log_message(f"Download complete: {result_path}", "success")
    
    def cancel_download(self):
        """Cancel the current download"""
        # Note: This is a simplified cancel - in a production app you'd need 
        # more sophisticated thread management
        self.hide_progress()
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        
        self.log_message("Download cancelled by user", "warning")
    
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
        
        self.log_message("All fields cleared", "info")
    
    def show_progress(self, message):
        """Show progress section with message - Winamp style"""
        self.progress_frame.grid()
        # Create animated progress effect by changing the background color
        self._animate_progress()
        self.progress_status_var.set(message)
    
    def hide_progress(self):
        """Hide progress section - Winamp style"""
        # Stop any ongoing animation
        if hasattr(self, '_progress_animation'):
            self.root.after_cancel(self._progress_animation)
        # Reset progress bar color
        self.progress_bar.configure(bg=WinampStyle.BG_SUNKEN)
        self.progress_frame.grid_remove()
    
    def _animate_progress(self):
        """Create a simple animation effect for the progress bar"""
        try:
            # Alternate between two colors to simulate activity
            current_color = self.progress_bar.cget('bg')
            if current_color == WinampStyle.BG_SUNKEN:
                new_color = WinampStyle.ACCENT_COLOR
            else:
                new_color = WinampStyle.BG_SUNKEN
            
            self.progress_bar.configure(bg=new_color)
            
            # Schedule next animation frame
            self._progress_animation = self.root.after(500, self._animate_progress)
        except:
            # In case the widget is destroyed, silently ignore
            pass
    
    def update_progress_status(self, message):
        """Update progress status message"""
        self.progress_status_var.set(message)
    
    def handle_error(self, error_message):
        """Handle and display errors"""
        self.hide_progress()
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        
        messagebox.showerror("Error", error_message)
        self.log_message(error_message, "error")
    
    def log_message(self, message, level="info"):
        """Add message to status log - Winamp style"""
        self.status_text.configure(state=tk.NORMAL)
        
        # Add timestamp with Winamp-style formatting
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Format message based on level with Winamp-style indicators
        if level == "success":
            formatted_msg = f"[{timestamp}] ▬▬ {message}\n"
            color_tag = "success"
        elif level == "error":
            formatted_msg = f"[{timestamp}] ░░ ERROR: {message}\n"
            color_tag = "error"
        elif level == "warning":
            formatted_msg = f"[{timestamp}] ▓▓ WARNING: {message}\n"
            color_tag = "warning"
        else:
            formatted_msg = f"[{timestamp}] ▬▬ {message}\n"
            color_tag = "info"
        
        # Configure color tags for different message types
        self.status_text.tag_configure("success", foreground=WinampStyle.TEXT_SUCCESS)
        self.status_text.tag_configure("error", foreground=WinampStyle.TEXT_ERROR)
        self.status_text.tag_configure("warning", foreground=WinampStyle.TEXT_WARNING)
        self.status_text.tag_configure("info", foreground=WinampStyle.TEXT_LCD)
        
        # Insert with appropriate color tag
        start_idx = self.status_text.index(tk.END)
        self.status_text.insert(tk.END, formatted_msg)
        end_idx = self.status_text.index(tk.END)
        self.status_text.tag_add(color_tag, start_idx, end_idx)
        
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
        
        self.log_message("All dependencies available", "success")
        
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