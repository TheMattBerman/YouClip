"""
Input validation utilities for YouClip
Validates YouTube URLs and other user inputs
"""

import re
import os
from urllib.parse import urlparse, parse_qs
from typing import Optional


class Validators:
    """Handles various input validations"""
    
    # YouTube URL patterns
    YOUTUBE_PATTERNS = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',
    ]
    
    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        """
        Check if URL is a valid YouTube URL
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid YouTube URL, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        url = url.strip()
        
        for pattern in Validators.YOUTUBE_PATTERNS:
            if re.match(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract YouTube video ID from URL
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID if found, None otherwise
        """
        if not Validators.is_valid_youtube_url(url):
            return None
        
        for pattern in Validators.YOUTUBE_PATTERNS:
            match = re.match(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """
        Check if filename is valid for the current OS
        
        Args:
            filename: Filename to validate
            
        Returns:
            True if valid filename, False otherwise
        """
        if not filename or not isinstance(filename, str):
            return False
        
        filename = filename.strip()
        
        # Check for empty or whitespace-only names
        if not filename or filename.isspace():
            return False
        
        # Check for invalid characters (Windows is most restrictive)
        invalid_chars = r'[<>:"/\\|?*]'
        if re.search(invalid_chars, filename):
            return False
        
        # Check for reserved names (Windows)
        reserved_names = [
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        ]
        
        name_without_ext = os.path.splitext(filename)[0].upper()
        if name_without_ext in reserved_names:
            return False
        
        # Check length (most filesystems support up to 255 characters)
        if len(filename.encode('utf-8')) > 255:
            return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing/replacing invalid characters
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        if not filename:
            return "untitled"
        
        # Replace invalid characters with underscores
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove leading/trailing whitespace and dots
        filename = filename.strip(' .')
        
        # Ensure it's not empty after sanitization
        if not filename:
            filename = "untitled"
        
        # Truncate if too long (leave room for extension)
        max_length = 200
        if len(filename.encode('utf-8')) > max_length:
            filename = filename[:max_length].strip()
        
        return filename
    
    @staticmethod
    def is_valid_directory(directory: str) -> bool:
        """
        Check if directory path is valid and writable
        
        Args:
            directory: Directory path to validate
            
        Returns:
            True if valid and writable directory, False otherwise
        """
        if not directory or not isinstance(directory, str):
            return False
        
        try:
            # Check if directory exists
            if not os.path.exists(directory):
                return False
            
            # Check if it's actually a directory
            if not os.path.isdir(directory):
                return False
            
            # Check if writable
            if not os.access(directory, os.W_OK):
                return False
            
            return True
        
        except (OSError, ValueError):
            return False 