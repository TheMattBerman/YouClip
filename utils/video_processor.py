"""
Video processing utilities for YouClip
Handles YouTube video info retrieval and ffmpeg operations
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, Optional, Tuple
from pathlib import Path

import yt_dlp
from tqdm import tqdm

from .validators import Validators
from .time_parser import TimeParser


class VideoProcessor:
    """Handles YouTube video processing and ffmpeg operations"""
    
    def __init__(self):
        self.temp_dir = None
        self.video_info = None
    
    def get_video_info(self, url: str) -> Dict:
        """
        Get video information from YouTube URL
        
        Args:
            url: YouTube URL
            
        Returns:
            Dictionary containing video metadata
            
        Raises:
            Exception: If unable to retrieve video info
        """
        if not Validators.is_valid_youtube_url(url):
            raise ValueError("Invalid YouTube URL provided")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                self.video_info = {
                    'id': info.get('id'),
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'upload_date': info.get('upload_date'),
                    'view_count': info.get('view_count'),
                    'description': info.get('description', ''),
                    'formats': info.get('formats', []),
                    'url': url
                }
                
                return self.video_info
                
        except Exception as e:
            raise Exception(f"Failed to retrieve video information: {str(e)}")
    
    def preview_video_info(self, url: str) -> None:
        """
        Display video information in a user-friendly format
        
        Args:
            url: YouTube URL
        """
        try:
            info = self.get_video_info(url)
            
            print(f"\n{'='*60}")
            print(f"VIDEO INFORMATION")
            print(f"{'='*60}")
            print(f"Title: {info['title']}")
            print(f"Uploader: {info['uploader']}")
            print(f"Duration: {TimeParser.seconds_to_timestamp(info['duration']) if info['duration'] else 'Unknown'}")
            print(f"Views: {info['view_count']:,}" if info['view_count'] else "Views: Unknown")
            
            if info['upload_date']:
                formatted_date = f"{info['upload_date'][:4]}-{info['upload_date'][4:6]}-{info['upload_date'][6:8]}"
                print(f"Upload Date: {formatted_date}")
            
            # Show available quality options
            video_formats = [f for f in info['formats'] if f.get('vcodec') != 'none']
            if video_formats:
                qualities = set()
                for fmt in video_formats:
                    if fmt.get('height'):
                        qualities.add(f"{fmt['height']}p")
                
                if qualities:
                    print(f"Available Qualities: {', '.join(sorted(qualities, key=lambda x: int(x[:-1]), reverse=True))}")
            
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"Error retrieving video info: {e}")
    
    def get_best_format(self, audio_only: bool = False, max_quality: str = "1440p") -> Optional[str]:
        """
        Get the best available format for the video
        
        Args:
            audio_only: If True, get best audio format
            max_quality: Maximum quality to download (1080p, 1440p, 2160p, or 'best')
            
        Returns:
            Format selector string for yt-dlp
        """
        if not self.video_info:
            return None
        
        if audio_only:
            # Try audio formats in order of preference, fallback to any available
            return 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best'
        else:
            # Map quality settings to height limits
            quality_map = {
                "720p": 720,
                "1080p": 1080, 
                "1440p": 1440,
                "2160p": 2160,
                "best": None
            }
            
            if max_quality == "best" or max_quality not in quality_map:
                # Download best available quality - use separate video+audio for highest quality
                return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best'
            else:
                max_height = quality_map[max_quality]
                # Use separate video+audio streams for high quality, with fallbacks
                return f'bestvideo[height<={max_height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}][ext=mp4]/best[height<={max_height}]/best[ext=mp4]/best'
    
    def create_clip(self, url: str, start_time: float, end_time: float, 
                   output_path: str, audio_only: bool = False, 
                   progress_callback: Optional[callable] = None,
                   max_quality: str = "1440p") -> str:
        """
        Create a clip from YouTube video
        
        Args:
            url: YouTube URL
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output file path
            audio_only: If True, extract audio only
            progress_callback: Optional callback for progress updates
            max_quality: Maximum video quality (720p, 1080p, 1440p, 2160p, or 'best')
            
        Returns:
            Path to the created clip file
            
        Raises:
            Exception: If clip creation fails
        """
        if not self.video_info:
            self.get_video_info(url)
        
        # Validate time range
        duration = self.video_info.get('duration')
        if duration:
            start_time, end_time = TimeParser.validate_time_range(start_time, end_time, duration)
        
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix='youclip_')
        
        try:
            # Step 1: Download the full video to temp directory
            temp_video_path = self._download_video(url, audio_only, progress_callback, max_quality)
            
            # Step 2: Extract clip using ffmpeg
            final_path = self._extract_clip_ffmpeg(temp_video_path, start_time, end_time, 
                                                 output_path, audio_only, progress_callback)
            
            return final_path
            
        finally:
            # Cleanup temporary files
            self._cleanup_temp_files()
    
    def _download_video(self, url: str, audio_only: bool = False, 
                       progress_callback: Optional[callable] = None,
                       max_quality: str = "1440p") -> str:
        """
        Download video to temporary directory
        
        Args:
            url: YouTube URL
            audio_only: If True, download audio only
            progress_callback: Progress callback function
            max_quality: Maximum video quality to download
            
        Returns:
            Path to downloaded video file
        """
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                try:
                    percent = d.get('_percent_str', '0%')
                    speed = d.get('_speed_str', 'N/A')
                    progress_callback(f"Downloading... {percent} at {speed}")
                except:
                    pass
        
        format_selector = self.get_best_format(audio_only, max_quality)
        
        # Prepare output template
        output_template = os.path.join(self.temp_dir, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': output_template,
            'progress_hooks': [progress_hook] if progress_callback else [],
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if progress_callback:
                    progress_callback(f"Starting download with format: {format_selector}")
                
                # Extract info first to get expected filename
                info = ydl.extract_info(url, download=False)
                expected_filename = ydl.prepare_filename(info)
                
                if progress_callback:
                    progress_callback(f"Expected filename: {os.path.basename(expected_filename)}")
                
                # Now download
                ydl.download([url])
                
                # Check if the expected file exists and has content
                if os.path.exists(expected_filename):
                    file_size = os.path.getsize(expected_filename)
                    if progress_callback:
                        progress_callback(f"Download completed: {file_size} bytes")
                    
                    if file_size == 0:
                        raise Exception("Downloaded file is empty (0 bytes)")
                    elif file_size < 1000:  # Less than 1KB is suspicious
                        raise Exception(f"Downloaded file is suspiciously small ({file_size} bytes)")
                    
                    return expected_filename
                
                # Fallback: search for any video file in temp directory
                temp_files = []
                if os.path.exists(self.temp_dir):
                    for file in os.listdir(self.temp_dir):
                        file_path = os.path.join(self.temp_dir, file)
                        if os.path.isfile(file_path):
                            file_size = os.path.getsize(file_path)
                            temp_files.append(f"{file} ({file_size} bytes)")
                            
                            if file_size > 1000:  # Valid size threshold
                                if progress_callback:
                                    progress_callback(f"Found fallback file: {file} ({file_size} bytes)")
                                return file_path
                
                raise Exception(f"No valid downloaded file found. Expected: {expected_filename}, Temp files: {temp_files}")
                
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if progress_callback:
                progress_callback(f"yt-dlp download error: {error_msg}")
            
            # Try simplified format fallback
            if not audio_only:
                fallback_formats = [
                    'best[ext=mp4][height<=1440]/best[height<=1440]',
                    'best[ext=mp4]/best'
                ]
                
                for fallback_format in fallback_formats:
                    try:
                        if progress_callback:
                            progress_callback(f"Trying fallback format: {fallback_format}")
                        
                        ydl_opts['format'] = fallback_format
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            expected_filename = ydl.prepare_filename(info)
                            ydl.download([url])
                            
                            if os.path.exists(expected_filename):
                                file_size = os.path.getsize(expected_filename)
                                if file_size > 1000:
                                    if progress_callback:
                                        progress_callback(f"Fallback successful: {file_size} bytes")
                                    return expected_filename
                        
                    except Exception as fallback_e:
                        if progress_callback:
                            progress_callback(f"Fallback {fallback_format} failed: {fallback_e}")
                        continue
            
            raise Exception(f"All download attempts failed. Original error: {error_msg}")
            
        except Exception as e:
            error_msg = str(e)
            if progress_callback:
                progress_callback(f"Unexpected download error: {error_msg}")
            raise Exception(f"Download failed: {error_msg}")
    
    def _extract_clip_ffmpeg(self, input_path: str, start_time: float, end_time: float,
                           output_path: str, audio_only: bool = False,
                           progress_callback: Optional[callable] = None) -> str:
        """
        Extract clip using ffmpeg
        
        Args:
            input_path: Path to input video file
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output file path
            audio_only: If True, extract audio only
            progress_callback: Progress callback function
            
        Returns:
            Path to extracted clip
            
        Note:
            Key optimizations for accurate video clipping:
            1. Place -ss before -i for faster seeking (input seeking vs output seeking)
            2. Use re-encoding for short clips (<60s) to ensure frame accuracy
            3. Use stream copy for longer clips to maintain speed
            4. Fallback to re-encoding if stream copy fails
        """
        # Validate input file
        if not os.path.exists(input_path):
            raise Exception(f"Input file does not exist: {input_path}")
        
        input_size = os.path.getsize(input_path)
        if input_size == 0:
            raise Exception(f"Input file is empty (0 bytes): {input_path}")
        elif input_size < 1000:
            raise Exception(f"Input file is suspiciously small ({input_size} bytes): {input_path}")
        
        if progress_callback:
            progress_callback(f"Input file validated: {input_size} bytes")
        
        duration = end_time - start_time
        
        # Prepare ffmpeg command
        # Place -ss before -i for faster and more accurate seeking
        cmd = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', input_path,
            '-t', str(duration),
            '-y'  # Overwrite output file
        ]
        
        if audio_only:
            # Audio only extraction
            cmd.extend(['-vn', '-acodec', 'copy'])
            # Ensure output has audio extension
            if not output_path.endswith(('.mp3', '.aac', '.m4a', '.wav')):
                output_path = os.path.splitext(output_path)[0] + '.mp3'
        else:
            # For video clips, use re-encoding for better compatibility and precision
            # VP9 videos often have stream copy issues with precise timing
            cmd.extend([
                '-c:v', 'libx264',      # Re-encode to H.264 for compatibility
                '-c:a', 'aac',          # Re-encode audio to AAC
                '-preset', 'fast',      # Faster preset for reasonable speed
                '-crf', '18',           # High quality setting (lower = better quality)
                '-movflags', '+faststart'  # Optimize for web playback
            ])
            
            # Ensure output has video extension
            if not output_path.endswith(('.mp4', '.mkv', '.avi')):
                output_path = os.path.splitext(output_path)[0] + '.mp4'
        
        cmd.append(output_path)
        
        try:
            if progress_callback:
                progress_callback("Extracting clip with ffmpeg (re-encoding for precision)...")
                progress_callback(f"FFmpeg command: {' '.join(cmd)}")
            
            # Run ffmpeg command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if output file was created and has content
            if not os.path.exists(output_path):
                raise Exception(f"FFmpeg did not create output file: {output_path}")
            
            output_size = os.path.getsize(output_path)
            if output_size == 0:
                stderr_info = result.stderr if result.stderr else "No stderr"
                raise Exception(f"FFmpeg created empty file (0 bytes): {output_path}. FFmpeg stderr: {stderr_info}")
            elif output_size < 1000:
                # For very small files, show more debug info
                stderr_info = result.stderr if result.stderr else "No stderr"
                raise Exception(f"FFmpeg created suspiciously small file ({output_size} bytes): {output_path}. FFmpeg stderr: {stderr_info}")
            
            if progress_callback:
                progress_callback(f"Clip extraction completed! Output: {output_size} bytes")
            
            return output_path
            
        except subprocess.CalledProcessError as e:
            # Capture detailed error information
            stderr_info = e.stderr if e.stderr else "No stderr available"
            
            if progress_callback:
                progress_callback(f"FFmpeg failed. Error: {stderr_info}")
            
            # Try with alternative encoding settings as fallback
            if not audio_only:
                if progress_callback:
                    progress_callback("Trying alternative encoding settings...")
                
                # Alternative encoding approach
                fallback_cmd = [
                    'ffmpeg',
                    '-i', input_path,
                    '-ss', str(start_time),
                    '-t', str(duration),
                    '-c:v', 'libx264',
                    '-c:a', 'copy',         # Try copying audio instead
                    '-preset', 'ultrafast', # Fastest preset
                    '-crf', '23',           # Slightly lower quality for speed
                    '-y',
                    output_path
                ]
                
                try:
                    if progress_callback:
                        progress_callback(f"Fallback command: {' '.join(fallback_cmd)}")
                    
                    fallback_result = subprocess.run(
                        fallback_cmd,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    # Validate fallback output
                    if os.path.exists(output_path):
                        output_size = os.path.getsize(output_path)
                        if output_size > 1000:
                            if progress_callback:
                                progress_callback(f"Fallback encoding successful! Output: {output_size} bytes")
                            return output_path
                        else:
                            fallback_stderr = fallback_result.stderr if fallback_result.stderr else "No stderr"
                            raise Exception(f"Fallback encoding created small file ({output_size} bytes). Stderr: {fallback_stderr}")
                    else:
                        raise Exception("Fallback encoding did not create output file")
                    
                except subprocess.CalledProcessError as fallback_e:
                    fallback_stderr = fallback_e.stderr if fallback_e.stderr else "No stderr"
                    raise Exception(f"Both primary and fallback encoding failed. Primary: {stderr_info}, Fallback: {fallback_stderr}")
            
            raise Exception(f"FFmpeg failed: {stderr_info}")
                
        except FileNotFoundError:
            raise Exception("FFmpeg not found. Please install ffmpeg and ensure it's in your PATH.")
    
    def _cleanup_temp_files(self):
        """Clean up temporary files and directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except Exception:
                pass  # Ignore cleanup errors
    
    @staticmethod
    def check_dependencies() -> Tuple[bool, str]:
        """
        Check if required dependencies are available
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Check ffmpeg
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "FFmpeg not found. Please install ffmpeg."
        
        try:
            # Check yt-dlp
            import yt_dlp
        except ImportError:
            return False, "yt-dlp not found. Please install: pip install yt-dlp"
        
        return True, "All dependencies are available." 