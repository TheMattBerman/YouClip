#!/usr/bin/env python3
"""
YouClip Python Integration Example
Demonstrates how to use YouClip programmatically in Python applications
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add parent directory to path to import YouClip modules
sys.path.append(str(Path(__file__).parent.parent))

from utils.video_processor import VideoProcessor
from utils.time_parser import TimeParser
from utils.validators import Validators


class YouClipAPI:
    """
    Python API wrapper for YouClip functionality
    Use this class to integrate YouClip into your Python applications
    """
    
    def __init__(self):
        self.processor = VideoProcessor()
    
    def get_video_info(self, url: str) -> Dict:
        """Get video information from YouTube URL"""
        return self.processor.get_video_info(url)
    
    def create_clip(self, url: str, start_time: str, end_time: str, 
                   output_path: str, audio_only: bool = False) -> Tuple[bool, str]:
        """
        Create a clip from YouTube video
        
        Returns:
            Tuple of (success, message/path)
        """
        try:
            # Parse times
            start_seconds = TimeParser.parse_time(start_time)
            end_seconds = TimeParser.parse_time(end_time)
            
            # Create clip
            result_path = self.processor.create_clip(
                url, start_seconds, end_seconds, output_path, audio_only
            )
            
            return True, result_path
        
        except Exception as e:
            return False, str(e)
    
    def batch_extract(self, clips_config: List[Dict]) -> List[Dict]:
        """
        Extract multiple clips in batch
        
        Args:
            clips_config: List of clip configurations
            Each config should have: url, start, end, output, audio_only (optional)
        
        Returns:
            List of results with success status and paths/errors
        """
        results = []
        
        for i, config in enumerate(clips_config):
            print(f"Processing clip {i+1}/{len(clips_config)}: {config.get('output', 'unknown')}")
            
            success, result = self.create_clip(
                config['url'],
                config['start'],
                config['end'],
                config['output'],
                config.get('audio_only', False)
            )
            
            results.append({
                'config': config,
                'success': success,
                'result': result
            })
        
        return results


def example_1_basic_usage():
    """Example 1: Basic video info and single clip extraction"""
    print("=== Example 1: Basic Usage ===")
    
    api = YouClipAPI()
    
    # Example URL (replace with actual video)
    url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        # Get video information
        print("Fetching video info...")
        info = api.get_video_info(url)
        print(f"Title: {info['title']}")
        print(f"Duration: {TimeParser.seconds_to_timestamp(info['duration'])}")
        print(f"Uploader: {info['uploader']}")
        
        # Create a clip
        print("\nCreating clip...")
        success, result = api.create_clip(
            url, "30", "60", "example_clip.mp4"
        )
        
        if success:
            print(f"✅ Clip created: {result}")
        else:
            print(f"❌ Failed: {result}")
    
    except Exception as e:
        print(f"Error: {e}")


def example_2_batch_processing():
    """Example 2: Batch processing multiple clips"""
    print("\n=== Example 2: Batch Processing ===")
    
    api = YouClipAPI()
    
    # Define multiple clips to extract
    clips_config = [
        {
            'url': 'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'start': '0:15',
            'end': '0:30',
            'output': 'batch_clips/intro.mp4'
        },
        {
            'url': 'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'start': '1:00',
            'end': '1:30',
            'output': 'batch_clips/middle.mp4'
        },
        {
            'url': 'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'start': '2:00',
            'end': '2:30',
            'output': 'batch_clips/audio_only.mp3',
            'audio_only': True
        }
    ]
    
    # Create output directory
    os.makedirs('batch_clips', exist_ok=True)
    
    # Process all clips
    results = api.batch_extract(clips_config)
    
    # Show results
    print("\nResults:")
    for result in results:
        status = "✅" if result['success'] else "❌"
        output = result['config']['output']
        message = result['result']
        print(f"{status} {output}: {message}")


def example_3_command_line_integration():
    """Example 3: Using YouClip via command line from Python"""
    print("\n=== Example 3: Command Line Integration ===")
    
    def run_youclip_cli(url: str, start: str, end: str, output: str, 
                       audio_only: bool = False) -> Tuple[bool, str]:
        """Run YouClip via command line"""
        cmd = [sys.executable, 'youclip.py', url, start, end, '-o', output]
        
        if audio_only:
            cmd.append('--audio-only')
        
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent
            )
            
            if result.returncode == 0:
                return True, f"Success: {output}"
            else:
                return False, result.stderr
        
        except Exception as e:
            return False, str(e)
    
    # Example usage
    success, message = run_youclip_cli(
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "45", "75", "cli_example.mp4"
    )
    
    print(f"CLI Result: {'✅' if success else '❌'} {message}")


def example_4_web_app_integration():
    """Example 4: Web application integration pattern"""
    print("\n=== Example 4: Web App Integration Pattern ===")
    
    # Simulate a web application request handler
    def handle_clip_request(request_data: Dict) -> Dict:
        """
        Example function that could be used in a web application
        (Flask, Django, FastAPI, etc.)
        """
        api = YouClipAPI()
        
        try:
            # Validate input
            required_fields = ['url', 'start_time', 'end_time']
            for field in required_fields:
                if field not in request_data:
                    return {'error': f'Missing required field: {field}'}
            
            # Validate YouTube URL
            if not Validators.is_valid_youtube_url(request_data['url']):
                return {'error': 'Invalid YouTube URL'}
            
            # Generate unique filename
            import uuid
            unique_id = str(uuid.uuid4())[:8]
            output_filename = f"clip_{unique_id}.mp4"
            
            # Create clip
            success, result = api.create_clip(
                request_data['url'],
                request_data['start_time'],
                request_data['end_time'],
                output_filename,
                request_data.get('audio_only', False)
            )
            
            if success:
                return {
                    'success': True,
                    'filename': output_filename,
                    'path': result,
                    'download_url': f'/downloads/{output_filename}'
                }
            else:
                return {'error': result}
        
        except Exception as e:
            return {'error': str(e)}
    
    # Example request
    request = {
        'url': 'https://youtube.com/watch?v=dQw4w9WgXcQ',
        'start_time': '1:00',
        'end_time': '1:15',
        'audio_only': False
    }
    
    response = handle_clip_request(request)
    print(f"Web app response: {json.dumps(response, indent=2)}")


def example_5_advanced_features():
    """Example 5: Advanced features and error handling"""
    print("\n=== Example 5: Advanced Features ===")
    
    api = YouClipAPI()
    
    # Function to safely extract clip with comprehensive error handling
    def safe_extract_clip(url: str, start: str, end: str, output: str) -> Dict:
        """Extract clip with comprehensive error handling"""
        result = {
            'success': False,
            'error': None,
            'info': None,
            'output_path': None,
            'file_size': None
        }
        
        try:
            # Step 1: Validate URL
            if not Validators.is_valid_youtube_url(url):
                result['error'] = 'Invalid YouTube URL'
                return result
            
            # Step 2: Get video info
            try:
                info = api.get_video_info(url)
                result['info'] = {
                    'title': info['title'],
                    'duration': info['duration'],
                    'uploader': info['uploader']
                }
            except Exception as e:
                result['error'] = f'Failed to get video info: {e}'
                return result
            
            # Step 3: Validate time range
            try:
                start_seconds = TimeParser.parse_time(start)
                end_seconds = TimeParser.parse_time(end)
                
                if info['duration']:
                    start_seconds, end_seconds = TimeParser.validate_time_range(
                        start_seconds, end_seconds, info['duration']
                    )
            except Exception as e:
                result['error'] = f'Invalid time range: {e}'
                return result
            
            # Step 4: Extract clip
            success, clip_result = api.create_clip(url, start, end, output)
            
            if success:
                result['success'] = True
                result['output_path'] = clip_result
                
                # Get file size if file exists
                if os.path.exists(clip_result):
                    result['file_size'] = os.path.getsize(clip_result)
            else:
                result['error'] = clip_result
        
        except Exception as e:
            result['error'] = f'Unexpected error: {e}'
        
        return result
    
    # Test the advanced function
    result = safe_extract_clip(
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "30", "45", "advanced_example.mp4"
    )
    
    print("Advanced extraction result:")
    print(json.dumps(result, indent=2, default=str))


if __name__ == '__main__':
    print("YouClip Python Integration Examples")
    print("=" * 50)
    
    # Check if dependencies are available
    success, message = VideoProcessor.check_dependencies()
    if not success:
        print(f"❌ {message}")
        print("Please install dependencies before running examples.")
        sys.exit(1)
    
    print("✅ All dependencies available!")
    
    # Run examples (comment out the ones you don't want to test)
    try:
        # example_1_basic_usage()
        # example_2_batch_processing()
        # example_3_command_line_integration()
        example_4_web_app_integration()
        # example_5_advanced_features()
        
        print("\n" + "=" * 50)
        print("Examples completed! Check the created files.")
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError running examples: {e}") 