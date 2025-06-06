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
    """YouClip-inspired color scheme and styling constants - Dark Gunmetal Chrome Theme"""
    
    # Core Dark Winamp Colors - Dark Gunmetal/Charcoal Metallic Palette
    BG_PRIMARY = "#3a3a3a"          # Dark gunmetal background (was light chrome)
    BG_SECONDARY = "#2d2d2d"        # Darker gunmetal panels  
    BG_ACCENT = "#505050"           # Medium gunmetal raised elements
    BG_SUNKEN = "#1a1a1a"           # Very dark gunmetal sunken elements
    BG_DARK = "#404040"             # Dark gunmetal for deep areas
    
    # Classic Winamp LCD/Display Colors - Keep authentic bright green
    BG_LCD = "#000000"              # Black LCD background
    TEXT_LCD = "#00ff41"            # Classic bright Winamp green
    TEXT_LCD_DIM = "#00cc33"        # Dimmed LCD text
    TEXT_LCD_GLOW = "#66ff66"       # LCD glow effect
    
    # Dark Metal/Chrome gradient colors for authentic 3D effect on dark theme
    CHROME_LIGHT = "#6a6a6a"        # Brightest chrome highlight (darker than white)
    CHROME_MID_LIGHT = "#555555"    # Light chrome (dark theme)
    CHROME_MID = "#3a3a3a"          # Base dark chrome
    CHROME_MID_DARK = "#2d2d2d"     # Mid chrome shadow
    CHROME_DARK = "#202020"         # Deep chrome shadow
    CHROME_DARKEST = "#151515"      # Darkest chrome
    
    # Dark theme button colors - High contrast on dark backgrounds
    BUTTON_FACE = "#4a4a4a"         # Dark button face
    BUTTON_LIGHT = "#6a6a6a"        # Button highlight (light on dark)
    BUTTON_SHADOW = "#2a2a2a"       # Button shadow
    BUTTON_DARK_SHADOW = "#1a1a1a"  # Button dark shadow
    BUTTON_PRESSED = "#353535"      # Pressed button
    BUTTON_TEXT = "#ffffff"         # White text on dark buttons for contrast
    BUTTON_TEXT_DARK = "#000000"    # Black text for light button backgrounds
    
    # YouClip Orange accent - Keep the classic Winamp color
    ACCENT_ORANGE = "#ff6600"       # Classic Winamp orange
    ACCENT_ORANGE_LIGHT = "#ff8833" # Light orange
    ACCENT_ORANGE_DARK = "#cc4400"  # Dark orange
    
    # Special Winamp gradient colors for authentic look
    WINAMP_BLUE = "#2d4f8e"         # Classic Winamp blue
    WINAMP_BLUE_LIGHT = "#4a6bb5"   # Light Winamp blue
    WINAMP_BLUE_DARK = "#1a3366"    # Dark Winamp blue
    
    # Text colors for dark theme - High contrast
    TEXT_PRIMARY = "#ffffff"        # White text on dark backgrounds
    TEXT_SECONDARY = "#cccccc"      # Light gray text
    TEXT_WHITE = "#ffffff"          # White text for dark areas
    TEXT_ERROR = "#ff4444"          # Bright red for errors
    TEXT_SUCCESS = "#44ff44"        # Bright green for success
    TEXT_WARNING = "#ffaa44"        # Bright orange for warnings
    
    # Window frame colors for authentic 3D effect on dark theme
    FRAME_LIGHT = "#6a6a6a"         # Top/left highlight (lighter on dark)
    FRAME_SHADOW = "#2a2a2a"        # Bottom/right shadow
    FRAME_DARK_SHADOW = "#1a1a1a"   # Deep shadow
    
    # Classic Winamp progress bar colors
    PROGRESS_BG = "#000000"         # Black progress background
    PROGRESS_FILL = "#ffaa00"       # Classic orange/yellow progress fill
    PROGRESS_HIGHLIGHT = "#ffcc33"  # Bright progress highlight
    
    # Fonts - Larger, more readable bitmap-style fonts
    FONT_SYSTEM = ("MS Sans Serif", 10, "bold")          # Larger system font
    FONT_MAIN = ("MS Sans Serif", 10, "bold")            # Larger main interface font
    FONT_HEADING = ("MS Sans Serif", 11, "bold")         # Larger section headings
    FONT_LCD = ("Fixedsys", 11, "bold")                  # Larger LCD displays
    FONT_TITLE = ("MS Sans Serif", 12, "bold")           # Larger main title
    FONT_BUTTON = ("MS Sans Serif", 10, "bold")          # Larger button text
    FONT_SMALL = ("MS Sans Serif", 9, "bold")            # Larger small text
    FONT_MONO = ("Courier New", 10, "bold")              # Larger monospace
    
    # Spacing and sizing - slightly more spacious for readability
    PADDING_SMALL = 3
    PADDING_MEDIUM = 5
    PADDING_LARGE = 10
    BORDER_WIDTH = 1
    BUTTON_HEIGHT = 26              # Slightly taller buttons for larger text
    
    @staticmethod
    def create_3d_border_style(widget, style="raised"):
        """Create authentic 3D border effect like classic Windows/YouClip"""
        if style == "raised":
            widget.configure(
                highlightbackground=WinampStyle.FRAME_LIGHT,
                highlightcolor=WinampStyle.FRAME_LIGHT,
                highlightthickness=1,
                relief="raised",
                bd=2
            )
        elif style == "sunken":
            widget.configure(
                highlightbackground=WinampStyle.FRAME_SHADOW,
                highlightcolor=WinampStyle.FRAME_SHADOW,
                highlightthickness=1,
                relief="sunken",
                bd=2
            )
        elif style == "chrome":
            widget.configure(
                highlightbackground=WinampStyle.CHROME_LIGHT,
                highlightcolor=WinampStyle.CHROME_LIGHT,
                highlightthickness=1,
                relief="raised",
                bd=3
            )
    
    @staticmethod
    def create_lcd_display_style(widget):
        """Create authentic LCD display styling"""
        widget.configure(
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD,
            font=WinampStyle.FONT_LCD,
            relief="sunken",
            bd=2,
            highlightbackground=WinampStyle.CHROME_DARK,
            highlightthickness=1
        )


class YouTubeClipGUI:
    """Main GUI application for YouClip"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.processor = VideoProcessor()
        self.current_video_info = None
        self.download_thread = None
        
        # Add scrolling text variables for authentic YouClip feel
        self.title_text = ""
        self.title_scroll_pos = 0
        self.title_scroll_active = False
        
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        
        # Setup keyboard shortcuts after widgets are created
        self.setup_keyboard_shortcuts()
        
        # Start the title scrolling animation
        self.animate_title_scroll()
        
    def setup_window(self):
        """Configure the main window - Authentic Winamp style with Windows 98 chrome"""
        self.root.title("YouClip v2.1 - [Stopped] - YouClip")
        self.root.geometry("580x480")  # More compact like original Winamp
        self.root.minsize(550, 450)
        self.root.resizable(True, True)
        
        # Configure window background with authentic chrome colors
        self.root.configure(bg=WinampStyle.BG_PRIMARY)
        
        # Try to set classic Windows styling
        try:
            # Make it look like a classic Windows application
            self.root.attributes('-toolwindow', False)
        except:
            pass
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (580 // 2)
        y = (self.root.winfo_screenheight() // 2) - (480 // 2)
        self.root.geometry(f"580x480+{x}+{y}")
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_keyboard_shortcuts(self):
        """Setup classic YouClip-style keyboard shortcuts"""
        # Classic YouClip shortcuts
        self.root.bind('<Control-l>', lambda e: self.url_entry.focus_set() if hasattr(self, 'url_entry') else None)  # Focus URL
        self.root.bind('<Control-Return>', lambda e: self.start_download())  # Download
        self.root.bind('<Escape>', lambda e: self.cancel_download())         # Stop
        self.root.bind('<Control-c>', lambda e: self.clear_all())           # Clear
        self.root.bind('<F1>', lambda e: self.show_about())                 # About
        
        # Make Enter in URL field trigger preview
        if hasattr(self, 'url_entry') and hasattr(self, 'preview_btn'):
            self.url_entry.bind('<Return>', lambda e: self.preview_video() if self.preview_btn['state'] == 'normal' else None)
    
    def create_widgets(self):
        """Create and layout all GUI widgets - Authentic YouClip style"""
        # Main container with authentic Windows 98 chrome 3D border
        main_frame = tk.Frame(
            self.root, 
            bg=WinampStyle.BG_PRIMARY,
            relief="raised",
            bd=2
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Create authentic YouClip-style title bar
        self.create_title_bar(main_frame, row=0)
        
        # Create main LCD display area (like YouClip's main display)
        self.create_main_display(main_frame, row=1)
        
        # Create control panels section
        self.create_control_panels(main_frame, row=2)
        
        # Create bottom status/log area
        self.create_bottom_panel(main_frame, row=3)
    
    def create_title_bar(self, parent, row):
        """Create authentic YouClip-style title bar"""
        title_frame = tk.Frame(
            parent,
            bg=WinampStyle.BG_PRIMARY,
            relief="flat",
            bd=0
        )
        title_frame.grid(row=row, column=0, sticky="ew", pady=(0, 2))
        title_frame.columnconfigure(1, weight=1)
        
        # Left side - YouClip logo area with Winamp blue gradient
        logo_frame = tk.Frame(
            title_frame,
            bg=WinampStyle.WINAMP_BLUE,
            relief="raised",
            bd=1
        )
        logo_frame.grid(row=0, column=0, sticky="w", padx=(2, 4))
        
        # YouClip logo text - Larger and more prominent
        logo_label = tk.Label(
            logo_frame,
            text="YOUCLIP",
            font=("Arial", 11, "bold"),
            fg=WinampStyle.TEXT_WHITE,
            bg=WinampStyle.WINAMP_BLUE
        )
        logo_label.pack(padx=6, pady=2)
        
        # Center - main title
        title_label = tk.Label(
            title_frame,
            text="YouClip v2.1 - YouTube Video Clip Downloader",
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_PRIMARY
        )
        title_label.grid(row=0, column=1, sticky="w", padx=4)
        
        # Right side - minimize/close buttons (aesthetic only)
        buttons_frame = tk.Frame(
            title_frame,
            bg=WinampStyle.BG_PRIMARY,
            relief="flat"
        )
        buttons_frame.grid(row=0, column=2, sticky="e", padx=2)
        
        # Minimize button - Authentic Winamp style
        min_btn = tk.Button(
            buttons_frame,
            text="_",
            font=("Arial", 8, "bold"),
            width=2,
            height=1,
            bg=WinampStyle.BUTTON_FACE,
            fg=WinampStyle.BUTTON_TEXT,
            relief="raised",
            bd=1,
            command=self.minimize_window,
            highlightbackground=WinampStyle.BUTTON_LIGHT,
            highlightcolor=WinampStyle.BUTTON_LIGHT
        )
        min_btn.pack(side="left", padx=1)
        
        # Close button - Authentic Winamp style
        close_btn = tk.Button(
            buttons_frame,
            text="X",
            font=("Arial", 8, "bold"),
            width=2,
            height=1,
            bg=WinampStyle.BUTTON_FACE,
            fg=WinampStyle.BUTTON_TEXT,
            relief="raised",
            bd=1,
            command=self.root.quit,
            highlightbackground=WinampStyle.BUTTON_LIGHT,
            highlightcolor=WinampStyle.BUTTON_LIGHT
        )
        close_btn.pack(side="left")
    
    def create_main_display(self, parent, row):
        """Create main LCD display area like YouClip's main window"""
        display_frame = tk.Frame(
            parent,
            bg=WinampStyle.BG_SECONDARY,
            relief="sunken",
            bd=2
        )
        display_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=2)
        display_frame.columnconfigure(0, weight=1)
        
        # Main LCD display with enhanced Winamp styling
        lcd_frame = tk.Frame(
            display_frame,
            bg=WinampStyle.BG_LCD,
            relief="sunken",
            bd=2
        )
        lcd_frame.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        lcd_frame.columnconfigure(0, weight=1)
        
        # Create URL input section within LCD
        self.create_url_section(lcd_frame, row=0)
        
        # Create video info display
        self.create_video_info_section(lcd_frame, row=1)
    
    def create_control_panels(self, parent, row):
        """Create control panels section"""
        controls_frame = tk.Frame(
            parent,
            bg=WinampStyle.BG_PRIMARY,
            relief="flat"
        )
        controls_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=2)
        controls_frame.columnconfigure(0, weight=1)
        controls_frame.columnconfigure(1, weight=1)
        
        # Left panel - Time controls
        left_panel = tk.Frame(
            controls_frame,
            bg=WinampStyle.BG_SECONDARY,
            relief="sunken",
            bd=2
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        
        self.create_time_section(left_panel, row=0)
        
        # Right panel - Output controls
        right_panel = tk.Frame(
            controls_frame,
            bg=WinampStyle.BG_SECONDARY,
            relief="sunken",
            bd=2
        )
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(1, 0))
        
        self.create_output_section(right_panel, row=0)
        
        # Action buttons below panels
        self.create_action_buttons(controls_frame, row=1)
        
        # Progress section
        self.create_progress_section(controls_frame, row=2)
    
    def create_bottom_panel(self, parent, row):
        """Create bottom status panel"""
        self.create_status_section(parent, row)
    
    def minimize_window(self):
        """Minimize window"""
        self.root.iconify()
    
    def create_url_section(self, parent, row):
        """Create URL input section - Authentic LCD style"""
        # URL input area within LCD display
        url_frame = tk.Frame(
            parent,
            bg=WinampStyle.BG_LCD,
            relief="flat"
        )
        url_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=4)
        url_frame.columnconfigure(1, weight=1)
        
        # URL label in LCD style
        url_label = tk.Label(
            url_frame,
            text="URL:",
            font=WinampStyle.FONT_LCD,
            fg=WinampStyle.TEXT_LCD,
            bg=WinampStyle.BG_LCD
        )
        url_label.grid(row=0, column=0, sticky="w", padx=(2, 4), pady=2)
        
        # URL entry with authentic LCD styling
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            url_frame,
            textvariable=self.url_var,
            font=WinampStyle.FONT_LCD,
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=1,
            insertbackground=WinampStyle.TEXT_LCD,
            highlightthickness=0
        )
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(0, 2), pady=2)
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        
        # Preview button (compact, like YouClip buttons) - Authentic Winamp styling
        self.preview_btn = tk.Button(
            url_frame,
            text="►",
            command=self.preview_video,
            width=3,
            height=1,
            font=("Arial", 12, "bold"),
            bg=WinampStyle.BUTTON_FACE,
            fg=WinampStyle.BUTTON_TEXT,
            relief="raised",
            bd=2,
            state="disabled",
            activebackground=WinampStyle.ACCENT_ORANGE,
            activeforeground=WinampStyle.TEXT_WHITE,
            cursor="hand2",
            highlightbackground=WinampStyle.BUTTON_LIGHT,
            highlightcolor=WinampStyle.BUTTON_LIGHT,
            disabledforeground=WinampStyle.BUTTON_SHADOW
        )
        self.preview_btn.grid(row=0, column=2, sticky="e", padx=2)
        
        # Add authentic Winamp hover effects for preview button
        def on_preview_enter(e):
            if self.preview_btn['state'] == 'normal':
                self.preview_btn.configure(bg=WinampStyle.ACCENT_ORANGE, fg=WinampStyle.TEXT_WHITE)
        
        def on_preview_leave(e):
            if self.preview_btn['state'] == 'normal':
                self.preview_btn.configure(bg=WinampStyle.BUTTON_FACE, fg=WinampStyle.BUTTON_TEXT)
        
        self.preview_btn.bind("<Enter>", on_preview_enter)
        self.preview_btn.bind("<Leave>", on_preview_leave)
        
        # URL status display in enhanced LCD style
        self.url_status_var = tk.StringVar()
        self.url_status_label = tk.Label(
            url_frame,
            textvariable=self.url_status_var,
            font=WinampStyle.FONT_SMALL,
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD_DIM,
            anchor="w",
            justify="left"
        )
        self.url_status_label.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(2, 0))
    
    def create_video_info_section(self, parent, row):
        """Create video information display section - LCD style"""
        self.info_frame = tk.Frame(
            parent,
            bg=WinampStyle.BG_LCD,
            relief="flat"
        )
        self.info_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=4)
        self.info_frame.columnconfigure(0, weight=1)
        
        # Initially hidden
        self.info_frame.grid_remove()
        
        # Video info variables
        self.title_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.uploader_var = tk.StringVar()
        
        # Create scrolling text display area for video title (like Winamp's main display)
        self.title_display = tk.Label(
            self.info_frame,
            textvariable=self.title_var,
            font=WinampStyle.FONT_LCD,
            fg=WinampStyle.TEXT_LCD,
            bg=WinampStyle.BG_LCD,
            anchor="w",
            justify="left"
        )
        self.title_display.grid(row=0, column=0, sticky="ew", pady=2)
        
        # Duration and uploader info in smaller text
        info_frame = tk.Frame(self.info_frame, bg=WinampStyle.BG_LCD)
        info_frame.grid(row=1, column=0, sticky="ew")
        info_frame.columnconfigure(1, weight=1)
        
        # Duration
        duration_label = tk.Label(
            info_frame,
            textvariable=self.duration_var,
            font=WinampStyle.FONT_SMALL,
            fg=WinampStyle.TEXT_LCD_DIM,
            bg=WinampStyle.BG_LCD,
            anchor="w"
        )
        duration_label.grid(row=0, column=0, sticky="w")
        
        # Uploader
        uploader_label = tk.Label(
            info_frame,
            textvariable=self.uploader_var,
            font=WinampStyle.FONT_SMALL,
            fg=WinampStyle.TEXT_LCD_DIM,
            bg=WinampStyle.BG_LCD,
            anchor="e"
        )
        uploader_label.grid(row=0, column=1, sticky="e")
    
    def create_time_section(self, parent, row):
        """Create time range input section - Authentic panel style"""
        parent.columnconfigure(0, weight=1)
        
        # Panel title
        title_label = tk.Label(
            parent,
            text="Time Range",
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(4, 2), padx=4)
        
        # Time inputs frame
        time_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY)
        time_frame.grid(row=1, column=0, sticky="ew", padx=4, pady=2)
        time_frame.columnconfigure(1, weight=1)
        time_frame.columnconfigure(3, weight=1)
        
        # Start time
        tk.Label(
            time_frame,
            text="START",
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        ).grid(row=0, column=0, sticky="w", padx=(2, 4))
        
        self.start_time_var = tk.StringVar()
        self.start_entry = tk.Entry(
            time_frame,
            textvariable=self.start_time_var,
            width=10,
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=1,
            insertbackground=WinampStyle.TEXT_LCD
        )
        self.start_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.start_entry.bind('<KeyRelease>', self.on_time_change)
        
        # End time
        tk.Label(
            time_frame,
            text="END",
            font=WinampStyle.FONT_MAIN,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        ).grid(row=0, column=2, sticky="w", padx=(0, 4))
        
        self.end_time_var = tk.StringVar()
        self.end_entry = tk.Entry(
            time_frame,
            textvariable=self.end_time_var,
            width=10,
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=1,
            insertbackground=WinampStyle.TEXT_LCD
        )
        self.end_entry.grid(row=0, column=3, sticky="ew", padx=(0, 2))
        self.end_entry.bind('<KeyRelease>', self.on_time_change)
        
        # Time format help
        time_help = tk.Label(
            parent,
            text="Format: MM:SS or HH:MM:SS",
            font=WinampStyle.FONT_SMALL,
            fg=WinampStyle.TEXT_SECONDARY,
            bg=WinampStyle.BG_SECONDARY
        )
        time_help.grid(row=2, column=0, sticky="w", pady=(2, 2), padx=4)
        
        # Time validation status
        self.time_status_var = tk.StringVar()
        self.time_status_label = tk.Label(
            parent,
            textvariable=self.time_status_var,
            font=WinampStyle.FONT_SMALL,
            bg=WinampStyle.BG_SECONDARY,
            fg=WinampStyle.TEXT_SUCCESS,
            anchor="w"
        )
        self.time_status_label.grid(row=3, column=0, sticky="ew", pady=(2, 4), padx=4)
    
    def create_output_section(self, parent, row):
        """Create output options section - Authentic panel style"""
        parent.columnconfigure(0, weight=1)
        
        # Panel title
        title_label = tk.Label(
            parent,
            text="Output Options",
            font=WinampStyle.FONT_HEADING,
            fg=WinampStyle.TEXT_PRIMARY,
            bg=WinampStyle.BG_SECONDARY
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(4, 2), padx=4)
        
        # Output type selection
        type_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY)
        type_frame.grid(row=1, column=0, sticky="ew", padx=4, pady=2)
        
        self.output_type_var = tk.StringVar(value="video")
        
        tk.Radiobutton(
            type_frame,
            text="MP4 Video",
            variable=self.output_type_var,
            value="video",
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SECONDARY,
            fg=WinampStyle.TEXT_PRIMARY,
            selectcolor=WinampStyle.BG_ACCENT
        ).pack(side="left", padx=(2, 10))
        
        tk.Radiobutton(
            type_frame,
            text="MP3 Audio",
            variable=self.output_type_var,
            value="audio",
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_SECONDARY,
            fg=WinampStyle.TEXT_PRIMARY,
            selectcolor=WinampStyle.BG_ACCENT
        ).pack(side="left")
        
        # Filename input
        filename_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY)
        filename_frame.grid(row=2, column=0, sticky="ew", padx=4, pady=2)
        filename_frame.columnconfigure(0, weight=1)
        
        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(
            filename_frame,
            textvariable=self.filename_var,
            font=WinampStyle.FONT_MAIN,
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD,
            relief="sunken",
            bd=1,
            insertbackground=WinampStyle.TEXT_LCD
        )
        self.filename_entry.grid(row=0, column=0, sticky="ew", padx=(2, 4))
        
        self.browse_btn = tk.Button(
            filename_frame,
            text="...",
            command=self.browse_output_file,
            width=3,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BUTTON_FACE,
            fg=WinampStyle.BUTTON_TEXT,
            relief="raised",
            bd=2,
            activebackground=WinampStyle.ACCENT_ORANGE,
            activeforeground=WinampStyle.TEXT_WHITE,
            cursor="hand2",
            highlightbackground=WinampStyle.BUTTON_LIGHT,
            highlightcolor=WinampStyle.BUTTON_LIGHT
        )
        self.browse_btn.grid(row=0, column=1, padx=2)
        
        # Add authentic Winamp hover effects for browse button
        self.browse_btn.bind("<Enter>", lambda e: self.browse_btn.configure(bg=WinampStyle.ACCENT_ORANGE, fg=WinampStyle.TEXT_WHITE))
        self.browse_btn.bind("<Leave>", lambda e: self.browse_btn.configure(bg=WinampStyle.BUTTON_FACE, fg=WinampStyle.BUTTON_TEXT))
        
        # Auto-generate checkbox
        self.auto_filename_var = tk.BooleanVar(value=True)
        auto_check = tk.Checkbutton(
            parent,
            text="Auto-generate from title",
            variable=self.auto_filename_var,
            command=self.on_auto_filename_change,
            font=WinampStyle.FONT_SMALL,
            bg=WinampStyle.BG_SECONDARY,
            fg=WinampStyle.TEXT_SECONDARY,
            selectcolor=WinampStyle.BG_ACCENT
        )
        auto_check.grid(row=3, column=0, sticky="w", pady=(2, 4), padx=4)
    
    def create_action_buttons(self, parent, row):
        """Create main action buttons - Authentic YouClip style with enhanced polish"""
        button_frame = tk.Frame(parent, bg=WinampStyle.BG_PRIMARY)
        button_frame.grid(row=row, column=0, sticky="ew", pady=4, padx=2)
        
        # Create classic Winamp-style transport buttons with authentic metallic chrome styling
        transport_frame = tk.Frame(button_frame, bg=WinampStyle.BG_SECONDARY, relief="sunken", bd=2)
        transport_frame.pack(fill="x", padx=1, pady=1)
        
        # Center the buttons with chrome background
        button_container = tk.Frame(transport_frame, bg=WinampStyle.BG_SECONDARY)
        button_container.pack(expand=True, pady=2)
        
        # Download button (play button style) - Compact Winamp styling
        self.download_btn = tk.Button(
            button_container,
            text="DOWNLOAD",
            command=self.start_download,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BUTTON_FACE,
            fg=WinampStyle.BUTTON_TEXT_DARK,
            relief="raised",
            bd=2,
            width=14,
            height=2,
            activebackground=WinampStyle.ACCENT_ORANGE,
            activeforeground=WinampStyle.TEXT_WHITE,
            cursor="hand2"
        )
        self.download_btn.pack(side="left", padx=1)
        
        # Add authentic Winamp hover effects
        self.download_btn.bind("<Enter>", lambda e: self.download_btn.configure(bg=WinampStyle.ACCENT_ORANGE, fg=WinampStyle.TEXT_WHITE))
        self.download_btn.bind("<Leave>", lambda e: self.download_btn.configure(bg=WinampStyle.BUTTON_FACE, fg=WinampStyle.BUTTON_TEXT_DARK))
        
        # Cancel button (stop button style) - Compact Winamp styling
        self.cancel_btn = tk.Button(
            button_container,
            text="STOP",
            command=self.cancel_download,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BUTTON_FACE,
            fg=WinampStyle.BUTTON_TEXT,
            relief="raised",
            bd=2,
            width=10,
            height=2,
            state="disabled",
            activebackground=WinampStyle.TEXT_ERROR,
            activeforeground=WinampStyle.TEXT_WHITE,
            cursor="hand2",
            disabledforeground=WinampStyle.TEXT_SECONDARY
        )
        self.cancel_btn.pack(side="left", padx=1)
        
        # Clear button (reset button style) - Compact Winamp styling
        clear_btn = tk.Button(
            button_container,
            text="CLEAR",
            command=self.clear_all,
            font=WinampStyle.FONT_BUTTON,
            bg=WinampStyle.BUTTON_FACE,
            fg=WinampStyle.BUTTON_TEXT_DARK,
            relief="raised",
            bd=2,
            width=10,
            height=2,
            activebackground=WinampStyle.TEXT_WARNING,
            activeforeground=WinampStyle.TEXT_WHITE,
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=1)
        
        # Add authentic Winamp hover effects for clear button
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(bg=WinampStyle.TEXT_WARNING, fg=WinampStyle.TEXT_WHITE))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(bg=WinampStyle.BUTTON_FACE, fg=WinampStyle.BUTTON_TEXT_DARK))
    
    def create_progress_section(self, parent, row):
        """Create progress tracking section - Enhanced YouClip style"""
        self.progress_frame = tk.Frame(parent, bg=WinampStyle.BG_PRIMARY)
        self.progress_frame.grid(row=row, column=0, sticky="ew", pady=2, padx=2)
        self.progress_frame.columnconfigure(0, weight=1)
        
        # Initially hidden
        self.progress_frame.grid_remove()
        
        # Progress display area with enhanced styling
        progress_display = tk.Frame(
            self.progress_frame,
            bg=WinampStyle.BG_SECONDARY,
            relief="sunken",
            bd=2
        )
        progress_display.pack(fill="x", padx=2, pady=2)
        progress_display.columnconfigure(0, weight=1)
        
        # Progress bar - Classic Winamp orange/yellow seek bar style
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Frame(
            progress_display,
            bg=WinampStyle.PROGRESS_BG,
            relief="sunken",
            bd=1,
            height=12
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=2, padx=2)
        
        # Create the actual progress fill bar
        self.progress_fill = tk.Frame(
            self.progress_bar,
            bg=WinampStyle.PROGRESS_FILL,
            height=8
        )
        self.progress_fill.place(x=2, y=2, width=0, height=8)
        
        # Progress status with compact LCD display
        self.progress_status_var = tk.StringVar()
        self.progress_status_label = tk.Label(
            progress_display,
            textvariable=self.progress_status_var,
            font=WinampStyle.FONT_LCD,
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD,
            anchor="w",
            relief="flat",
            bd=0
        )
        self.progress_status_label.grid(row=1, column=0, sticky="ew", padx=2, pady=(1, 2))
    
    def create_status_section(self, parent, row):
        """Create status/log section - Enhanced YouClip style"""
        status_frame = tk.Frame(parent, bg=WinampStyle.BG_SECONDARY, relief="sunken", bd=2)
        status_frame.grid(row=row, column=0, sticky="nsew", pady=2, padx=2)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # Configure main frame to expand this section
        parent.rowconfigure(row, weight=1)
        
        # Status text area with compact Winamp styling
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=5,
            wrap=tk.WORD,
            font=WinampStyle.FONT_LCD,
            bg=WinampStyle.BG_LCD,
            fg=WinampStyle.TEXT_LCD,
            relief="flat",
            bd=0,
            insertbackground=WinampStyle.TEXT_LCD,
            selectbackground=WinampStyle.ACCENT_ORANGE,
            selectforeground=WinampStyle.BG_LCD,
            state=tk.DISABLED
        )
        self.status_text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        # Add initial message with authentic Winamp styling
        self.log_message("YouClip v2.1 Ready", "info")
        self.log_message("Enter YouTube URL to begin", "info")
    
    def setup_styles(self):
        """Configure custom dark Winamp-inspired styles"""
        style = ttk.Style()
        
        # Set the theme to something that works with dark colors
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configure dark Winamp-style button with high contrast
        style.configure(
            "Winamp.TButton",
            font=WinampStyle.FONT_BUTTON,
            background=WinampStyle.BUTTON_FACE,
            foreground=WinampStyle.BUTTON_TEXT,
            borderwidth=2,
            relief="raised",
            focuscolor="none"
        )
        
        style.map(
            "Winamp.TButton",
            background=[
                ("active", WinampStyle.ACCENT_ORANGE),
                ("pressed", WinampStyle.BUTTON_PRESSED)
            ],
            foreground=[
                ("active", WinampStyle.TEXT_WHITE),
                ("pressed", WinampStyle.TEXT_WHITE)
            ],
            relief=[
                ("pressed", "sunken"),
                ("active", "raised")
            ]
        )
        
        # Configure dark Winamp-style frame
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
            foreground=WinampStyle.ACCENT_ORANGE,
            font=WinampStyle.FONT_HEADING
        )
        
        # Configure dark Winamp-style entry with LCD colors
        style.configure(
            "Winamp.TEntry",
            fieldbackground=WinampStyle.BG_LCD,
            foreground=WinampStyle.TEXT_LCD,
            borderwidth=2,
            relief="sunken",
            insertcolor=WinampStyle.TEXT_LCD,
            font=WinampStyle.FONT_MAIN
        )
        
        # Configure dark Winamp-style label
        style.configure(
            "Winamp.TLabel",
            background=WinampStyle.BG_SECONDARY,
            foreground=WinampStyle.TEXT_PRIMARY,
            font=WinampStyle.FONT_MAIN
        )
        
        # Configure LCD-style label for status displays (keep green LCD theme)
        style.configure(
            "LCD.TLabel",
            background=WinampStyle.BG_LCD,
            foreground=WinampStyle.TEXT_LCD,
            font=WinampStyle.FONT_LCD,
            relief="sunken",
            borderwidth=2
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
            self.url_status_var.set("VALID URL")
            self.preview_btn.configure(state="normal")
        else:
            self.url_status_var.set("INVALID URL")
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
                self.time_status_var.set("ERROR: End > Start")
                return
            
            duration = end_time - start_time
            duration_str = TimeParser.seconds_to_timestamp(duration)
            self.time_status_var.set(f"DURATION: {duration_str}")
            
            # Update filename if auto-generate is enabled
            if self.auto_filename_var.get() and self.current_video_info:
                self.update_auto_filename()
            
        except ValueError as e:
            self.time_status_var.set(f"ERROR: {str(e)}")
    
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
        
        # Update info labels with scrolling title effect
        title = info.get('title', 'Unknown')
        self.title_text = title
        self.title_scroll_pos = 0
        self.title_scroll_active = len(title) > 40  # Start scrolling if title is long
        
        # Update window title like classic Winamp
        short_title = title[:50] + "..." if len(title) > 50 else title
        self.root.title(f"YouClip v2.1 - {short_title} - Winamp")
        
        duration = info.get('duration')
        if duration:
            duration_str = TimeParser.seconds_to_timestamp(duration)
            self.duration_var.set(f"Duration: {duration_str}")
        else:
            self.duration_var.set('Duration: Unknown')
        
        uploader = info.get('uploader', 'Unknown')
        if len(uploader) > 30:
            uploader = uploader[:27] + "..."
        self.uploader_var.set(f"By: {uploader}")
        
        # Show info frame
        self.info_frame.grid()
        
        # Update filename if auto-generate is enabled
        if self.auto_filename_var.get():
            self.update_auto_filename()
        
        # Hide progress
        self.hide_progress()
        
        self.log_message(f"Video info loaded: {title}", "success")
    
    def animate_title_scroll(self):
        """Animate scrolling title text like classic Winamp"""
        if self.title_scroll_active and self.title_text:
            display_width = 35  # Maximum characters to display
            
            if len(self.title_text) <= display_width:
                # Text fits, no scrolling needed
                display_text = self.title_text
            else:
                # Scroll the text
                extended_text = self.title_text + " *** "
                
                if self.title_scroll_pos >= len(extended_text):
                    self.title_scroll_pos = 0
                
                # Get the display portion
                display_text = extended_text[self.title_scroll_pos:self.title_scroll_pos + display_width]
                if len(display_text) < display_width:
                    display_text += extended_text[:display_width - len(display_text)]
                
                self.title_scroll_pos += 1
            
            # Update the display
            if hasattr(self, 'title_var'):
                self.title_var.set(display_text)
        
        # Schedule next animation frame
        self.root.after(200, self.animate_title_scroll)  # Update every 200ms
    
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
        if not self.validate_inputs():
            return
        
        # Update window title to show download in progress
        self.root.title("YouClip v2.1 - [Downloading...] - Winamp")
        
        # Show progress
        self.show_progress("Preparing download...")
        
        # Disable download button, enable cancel
        self.download_btn.configure(state="disabled", text="⧗ DOWNLOADING")
        self.cancel_btn.configure(state="normal")
        
        # Start download in separate thread
        self.download_thread = threading.Thread(target=self.download_worker, daemon=True)
        self.download_thread.start()
        
        self.log_message("Download started...", "info")
    
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
        """Handle download completion"""
        # Reset UI state
        self.download_btn.configure(state="normal", text="► DOWNLOAD")
        self.cancel_btn.configure(state="disabled")
        self.hide_progress()
        
        if result_path and os.path.exists(result_path):
            # Update window title to show completion
            self.root.title("YouClip v2.1 - [Complete] - Winamp")
            
            self.log_message(f"Download completed: {result_path}", "success")
            
            # Show completion dialog with option to open file location
            result = messagebox.askyesno(
                "Download Complete", 
                f"Clip saved successfully!\n\nFile: {os.path.basename(result_path)}\n\nWould you like to open the file location?",
                icon="question"
            )
            
            if result:
                self.open_file_location(result_path)
        else:
            self.root.title("YouClip v2.1 - [Error] - Winamp")
            self.log_message("Download failed!", "error")
            messagebox.showerror("Download Error", "Download failed. Check the status log for details.")
    
    def cancel_download(self):
        """Cancel the current download"""
        if self.download_thread and self.download_thread.is_alive():
            # Note: This is a graceful request to stop, actual stopping depends on the processor
            self.processor.stop_download()
            self.log_message("Download cancellation requested...", "warning")
            
            # Update window title
            self.root.title("YouClip v2.1 - [Stopped] - Winamp")
            
            # Reset UI state
            self.download_btn.configure(state="normal", text="► DOWNLOAD")
            self.cancel_btn.configure(state="disabled")
            self.hide_progress()
    
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
                new_color = WinampStyle.ACCENT_ORANGE
            else:
                new_color = WinampStyle.BG_SUNKEN
            
            self.progress_bar.configure(bg=new_color)
            
            # Schedule next animation frame
            self._progress_animation = self.root.after(500, self._animate_progress)
        except:
            # In case the widget is destroyed, silently ignore
            pass
    
    def update_progress_status(self, message):
        """Update progress status message and progress bar fill"""
        self.progress_status_var.set(message)
        
        # Update progress bar fill if message contains percentage
        if "%" in message:
            try:
                # Extract percentage from message
                import re
                match = re.search(r'(\d+(?:\.\d+)?)%', message)
                if match:
                    percentage = float(match.group(1))
                    # Update progress bar width
                    bar_width = self.progress_bar.winfo_width() - 4
                    if bar_width > 0:
                        fill_width = int((percentage / 100) * bar_width)
                        self.progress_fill.place_configure(width=fill_width)
            except:
                pass
    
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
    
    def show_about(self):
        """Show about dialog with retro styling"""
        about_text = """YouClip v2.1 - Winamp Edition
        
YouTube Video Clip Downloader
Designed with authentic early 2000s Winamp styling

Keyboard Shortcuts:
Ctrl+L    - Focus URL field
Ctrl+Enter - Start download
Escape    - Stop download
Ctrl+C    - Clear all
F1        - This help

Created with ♫ nostalgia ♫"""
        
        messagebox.showinfo("About YouClip", about_text)
    
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