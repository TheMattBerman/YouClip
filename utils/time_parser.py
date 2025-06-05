"""
Time parsing utilities for YouClip
Handles various time formats and validates time ranges
"""

import re
from typing import Union, Tuple


class TimeParser:
    """Handles parsing and validation of time formats"""
    
    @staticmethod
    def parse_time(time_str: str) -> float:
        """
        Parse time string to seconds
        Supports formats: HH:MM:SS, MM:SS, SS, or pure seconds
        
        Args:
            time_str: Time string to parse
            
        Returns:
            Time in seconds as float
            
        Raises:
            ValueError: If time format is invalid
        """
        if not time_str:
            raise ValueError("Time string cannot be empty")
        
        time_str = time_str.strip()
        
        # Try to parse as pure seconds first
        try:
            return float(time_str)
        except ValueError:
            pass
        
        # Parse HH:MM:SS or MM:SS format
        time_pattern = r'^(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)$'
        match = re.match(time_pattern, time_str)
        
        if not match:
            raise ValueError(f"Invalid time format: {time_str}. Use HH:MM:SS, MM:SS, or seconds")
        
        hours, minutes, seconds = match.groups()
        
        # Convert to seconds
        total_seconds = 0.0
        
        if hours:
            total_seconds += int(hours) * 3600
        
        total_seconds += int(minutes) * 60
        total_seconds += float(seconds)
        
        if total_seconds < 0:
            raise ValueError("Time cannot be negative")
        
        return total_seconds
    
    @staticmethod
    def validate_time_range(start_time: float, end_time: float, video_duration: float = None) -> Tuple[float, float]:
        """
        Validate start and end times
        
        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            video_duration: Video duration in seconds (optional)
            
        Returns:
            Tuple of validated (start_time, end_time)
            
        Raises:
            ValueError: If time range is invalid
        """
        if start_time < 0:
            raise ValueError("Start time cannot be negative")
        
        if end_time <= start_time:
            raise ValueError("End time must be greater than start time")
        
        if video_duration is not None:
            if start_time >= video_duration:
                raise ValueError(f"Start time ({start_time}s) exceeds video duration ({video_duration}s)")
            
            if end_time > video_duration:
                print(f"Warning: End time ({end_time}s) exceeds video duration ({video_duration}s). Clipping to video end.")
                end_time = video_duration
        
        return start_time, end_time
    
    @staticmethod
    def seconds_to_timestamp(seconds: float) -> str:
        """
        Convert seconds to HH:MM:SS format
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Time string in HH:MM:SS format
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
        else:
            return f"{minutes:02d}:{secs:06.3f}" 