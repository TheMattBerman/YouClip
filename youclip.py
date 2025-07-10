#!/usr/bin/env python3
"""
YouClip - YouTube Video Clip Downloader
A tool to download specific segments from YouTube videos using ffmpeg
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

try:
    from colorama import init, Fore, Back, Style
    init()  # Initialize colorama for Windows compatibility
except ImportError:
    # Fallback if colorama is not available
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = RESET_ALL = ''

from utils.video_processor import VideoProcessor
from utils.time_parser import TimeParser
from utils.validators import Validators


class YouClipCLI:
    """Command-line interface for YouClip"""
    
    def __init__(self):
        self.processor = VideoProcessor()
        self.current_video_info = None
    
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Fore.CYAN}{'='*60}
{Style.BRIGHT}           YouClip - YouTube Video Clip Downloader
{Style.RESET_ALL}{Fore.CYAN}{'='*60}{Style.RESET_ALL}
{Fore.GREEN}Download specific segments from YouTube videos with ease!{Style.RESET_ALL}
"""
        print(banner)
    
    def print_error(self, message: str):
        """Print error message in red"""
        print(f"{Fore.RED}❌ Error: {message}{Style.RESET_ALL}")
    
    def print_success(self, message: str):
        """Print success message in green"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Print warning message in yellow"""
        print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message in blue"""
        print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")
    
    def get_youtube_url(self, url: Optional[str] = None) -> str:
        """
        Get and validate YouTube URL
        
        Args:
            url: Optional URL to validate
            
        Returns:
            Validated YouTube URL
        """
        if url:
            if Validators.is_valid_youtube_url(url):
                return url
            else:
                self.print_error("Invalid YouTube URL provided")
                sys.exit(1)
        
        while True:
            print(f"\n{Fore.YELLOW}Enter YouTube URL:{Style.RESET_ALL}")
            url = input("🔗 ").strip()
            
            if not url:
                self.print_error("URL cannot be empty")
                continue
            
            if Validators.is_valid_youtube_url(url):
                return url
            else:
                self.print_error("Invalid YouTube URL. Please try again.")
    
    def get_time_input(self, prompt: str, video_duration: Optional[float] = None) -> float:
        """
        Get and validate time input from user
        
        Args:
            prompt: Prompt message
            video_duration: Optional video duration for validation
            
        Returns:
            Time in seconds
        """
        while True:
            print(f"\n{Fore.YELLOW}{prompt}{Style.RESET_ALL}")
            if video_duration:
                duration_str = TimeParser.seconds_to_timestamp(video_duration)
                print(f"📺 Video duration: {duration_str}")
            print("⏱️  Formats: HH:MM:SS, MM:SS, or seconds (e.g., 120)")
            
            time_input = input("🕐 ").strip()
            
            if not time_input:
                self.print_error("Time cannot be empty")
                continue
            
            try:
                return TimeParser.parse_time(time_input)
            except ValueError as e:
                self.print_error(str(e))
    
    def get_output_filename(self, suggested_name: str) -> str:
        """
        Get output filename from user
        
        Args:
            suggested_name: Suggested filename based on video title
            
        Returns:
            Valid output filename
        """
        print(f"\n{Fore.YELLOW}Output filename:{Style.RESET_ALL}")
        print(f"💡 Suggested: {suggested_name}")
        print("📁 Press Enter to use suggested name, or type a custom name:")
        
        custom_name = input("📝 ").strip()
        
        if not custom_name:
            return suggested_name
        
        # Sanitize the custom filename
        sanitized = Validators.sanitize_filename(custom_name)
        
        if sanitized != custom_name:
            self.print_warning(f"Filename was sanitized to: {sanitized}")
        
        return sanitized
    
    def create_suggested_filename(self, title: str, start_time: float, end_time: float, audio_only: bool = False) -> str:
        """
        Create a suggested filename based on video title and time range
        
        Args:
            title: Video title
            start_time: Start time in seconds
            end_time: End time in seconds
            audio_only: Whether it's audio only
            
        Returns:
            Suggested filename
        """
        # Sanitize title
        clean_title = Validators.sanitize_filename(title)
        
        # Format time range
        start_str = TimeParser.seconds_to_timestamp(start_time).replace(':', '-')
        end_str = TimeParser.seconds_to_timestamp(end_time).replace(':', '-')
        
        # Choose extension
        ext = '.mp3' if audio_only else '.mp4'
        
        # Create filename
        filename = f"{clean_title}_clip_{start_str}_to_{end_str}{ext}"
        
        # Ensure filename isn't too long
        if len(filename) > 200:
            # Truncate title part
            title_part = clean_title[:100] + "..."
            filename = f"{title_part}_clip_{start_str}_to_{end_str}{ext}"
        
        return filename
    
    def _clean_url(self, url: str) -> str:
        """
        Clean URL by removing common prefixes that users might accidentally include
        
        Args:
            url: Original URL
            
        Returns:
            Cleaned URL
        """
        if not url:
            return url
            
        url = url.strip()
        
        # Remove common prefixes that users might accidentally include
        if url.startswith('@'):
            url = url[1:]
        if url.startswith('www.'):
            url = 'https://' + url
        elif not url.startswith(('http://', 'https://')):
            if 'youtube.com' in url or 'youtu.be' in url:
                url = 'https://' + url
        
        return url
    
    def progress_callback(self, message: str):
        """Progress callback for video processing"""
        print(f"\r{Fore.BLUE}🔄 {message}{Style.RESET_ALL}", end='', flush=True)
    
    def interactive_mode(self):
        """Run interactive mode"""
        self.print_banner()
        
        # Check dependencies
        success, message = VideoProcessor.check_dependencies()
        if not success:
            self.print_error(message)
            print(f"\n{Fore.YELLOW}Installation Instructions:{Style.RESET_ALL}")
            print("1. Install ffmpeg: https://ffmpeg.org/download.html")
            print("2. Install Python dependencies: pip install -r requirements.txt")
            sys.exit(1)
        
        self.print_success("All dependencies are available!")
        
        try:
            # Get YouTube URL
            url = self.get_youtube_url()
            
            # Get video information
            self.print_info("Retrieving video information...")
            self.processor.preview_video_info(url)
            self.current_video_info = self.processor.video_info
            
            # Ask for audio-only option
            print(f"\n{Fore.YELLOW}Download type:{Style.RESET_ALL}")
            print("1. Video clip (MP4)")
            print("2. Audio only (MP3)")
            
            while True:
                choice = input("Choose option (1 or 2): ").strip()
                if choice == '1':
                    audio_only = False
                    break
                elif choice == '2':
                    audio_only = True
                    break
                else:
                    self.print_error("Please enter 1 or 2")
            
            # Ask for quality preference (only for video)
            max_quality = "1440p"  # default
            if not audio_only:
                print(f"\n{Fore.YELLOW}Video quality:{Style.RESET_ALL}")
                print("1. 720p (HD)")
                print("2. 1080p (Full HD)")
                print("3. 1440p (2K) - Recommended")
                print("4. 2160p (4K)")
                print("5. Best available")
                
                quality_choices = {
                    '1': '720p',
                    '2': '1080p', 
                    '3': '1440p',
                    '4': '2160p',
                    '5': 'best'
                }
                
                while True:
                    choice = input("Choose quality (1-5, default is 3): ").strip()
                    if not choice:  # Default to 1440p
                        choice = '3'
                    if choice in quality_choices:
                        max_quality = quality_choices[choice]
                        break
                    else:
                        self.print_error("Please enter 1, 2, 3, 4, or 5")
            
            # Get time range
            duration = self.current_video_info.get('duration')
            start_time = self.get_time_input("Enter start time:", duration)
            end_time = self.get_time_input("Enter end time:", duration)
            
            # Validate time range
            try:
                start_time, end_time = TimeParser.validate_time_range(start_time, end_time, duration)
            except ValueError as e:
                self.print_error(str(e))
                return
            
            # Get output filename
            suggested_name = self.create_suggested_filename(
                self.current_video_info['title'], start_time, end_time, audio_only
            )
            output_filename = self.get_output_filename(suggested_name)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_filename) or '.'
            os.makedirs(output_dir, exist_ok=True)
            
            # Create the clip
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"Creating clip...")
            print(f"{'='*60}{Style.RESET_ALL}")
            
            result_path = self.processor.create_clip(
                url, start_time, end_time, output_filename, 
                audio_only, self.progress_callback, max_quality
            )
            
            print()  # New line after progress
            
            # Show results
            if os.path.exists(result_path):
                file_size = os.path.getsize(result_path)
                file_size_mb = file_size / (1024 * 1024)
                
                self.print_success("Clip created successfully!")
                print(f"📁 Location: {os.path.abspath(result_path)}")
                print(f"📊 Size: {file_size_mb:.2f} MB")
                print(f"⏱️  Duration: {TimeParser.seconds_to_timestamp(end_time - start_time)}")
            else:
                self.print_error("Clip file was not created")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
        except Exception as e:
            self.print_error(f"An unexpected error occurred: {str(e)}")
    
    def run_cli(self, args):
        """Run CLI with command-line arguments"""
        # Check dependencies
        success, message = VideoProcessor.check_dependencies()
        if not success:
            self.print_error(message)
            sys.exit(1)
        
        try:
            # Validate and clean inputs
            url = args.url
            if not Validators.is_valid_youtube_url(url):
                self.print_error("Invalid YouTube URL")
                sys.exit(1)
            
            # Clean the URL (remove @ prefix, add https if needed)
            url = self._clean_url(url)
            
            # Parse times
            start_time = TimeParser.parse_time(args.start)
            end_time = TimeParser.parse_time(args.end)
            
            # Get video info for validation
            if args.preview:
                self.processor.preview_video_info(url)
                return
            
            self.print_info("Retrieving video information...")
            video_info = self.processor.get_video_info(url)
            
            # Validate time range
            duration = video_info.get('duration')
            start_time, end_time = TimeParser.validate_time_range(start_time, end_time, duration)
            
            # Determine output filename
            if args.output:
                output_filename = args.output
            else:
                output_filename = self.create_suggested_filename(
                    video_info['title'], start_time, end_time, args.audio_only
                )
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_filename) or '.'
            os.makedirs(output_dir, exist_ok=True)
            
            # Create the clip
            self.print_info("Creating clip...")
            result_path = self.processor.create_clip(
                url, start_time, end_time, output_filename,
                args.audio_only, self.progress_callback, args.quality
            )
            
            print()  # New line after progress
            
            # Show results
            if os.path.exists(result_path):
                file_size = os.path.getsize(result_path)
                file_size_mb = file_size / (1024 * 1024)
                
                self.print_success("Clip created successfully!")
                print(f"📁 Location: {os.path.abspath(result_path)}")
                print(f"📊 Size: {file_size_mb:.2f} MB")
        
        except Exception as e:
            self.print_error(str(e))
            sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="YouClip - Download specific clips from YouTube videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python youclip.py
  
  # Command line mode
  python youclip.py "https://youtube.com/watch?v=VIDEO_ID" 30 90
  
  # With custom output and quality
  python youclip.py "https://youtube.com/watch?v=VIDEO_ID" 1:30 3:45 -o my_clip.mp4 --quality 2160p
  
  # Audio only
  python youclip.py "https://youtube.com/watch?v=VIDEO_ID" 0:30 2:00 --audio-only
  
  # Best available quality
  python youclip.py "https://youtube.com/watch?v=VIDEO_ID" 1:00 2:00 --quality best
  
  # Preview video info
  python youclip.py "https://youtube.com/watch?v=VIDEO_ID" --preview
  
Time formats: HH:MM:SS, MM:SS, or seconds (e.g., 30, 1:30, 0:01:30)
Quality options: 720p, 1080p, 1440p (default), 2160p, best
        """
    )
    
    parser.add_argument('url', nargs='?', help='YouTube video URL')
    parser.add_argument('start', nargs='?', help='Start time (HH:MM:SS, MM:SS, or seconds)')
    parser.add_argument('end', nargs='?', help='End time (HH:MM:SS, MM:SS, or seconds)')
    
    parser.add_argument('-o', '--output', help='Output filename')
    parser.add_argument('--audio-only', action='store_true', help='Extract audio only (MP3)')
    parser.add_argument('--quality', choices=['720p', '1080p', '1440p', '2160p', 'best'], 
                       default='1440p', help='Maximum video quality (default: 1440p)')
    parser.add_argument('--preview', action='store_true', help='Preview video information only')
    parser.add_argument('--version', action='version', version='YouClip 1.0.0')
    
    args = parser.parse_args()
    
    cli = YouClipCLI()
    
    # Check if we should run interactive mode
    if not args.url:
        cli.interactive_mode()
    elif args.preview:
        cli.run_cli(args)
    elif args.start and args.end:
        cli.run_cli(args)
    else:
        print("Error: Start and end times are required when providing URL")
        print("Use --help for usage information or run without arguments for interactive mode")
        sys.exit(1)


if __name__ == '__main__':
    main() 