#!/usr/bin/env python3
"""
Batch processing utilities for YouClip
Handles mass extraction of clips from multiple videos
"""

import os
import json
import yaml
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Union, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

from .video_processor import VideoProcessor
from .time_parser import TimeParser
from .validators import Validators


@dataclass
class ClipRequest:
    """Represents a single clip extraction request"""
    url: str
    start_time: str
    end_time: str
    output_filename: Optional[str] = None
    description: Optional[str] = None


@dataclass
class BatchJob:
    """Represents a batch job with multiple clip requests"""
    name: str
    output_directory: str
    clips: List[ClipRequest]
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class BatchProcessor:
    """Handles batch processing of multiple video clips"""
    
    def __init__(self, output_base_dir: str = "extracted_clips"):
        self.video_processor = VideoProcessor()
        self.output_base_dir = output_base_dir
        self.time_parser = TimeParser()
        
    def parse_config_file(self, config_path: str) -> BatchJob:
        """
        Parse a configuration file (JSON or YAML) into a BatchJob
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            BatchJob object
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                try:
                    data = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML is required for YAML files. Install with: pip install PyYAML")
            elif config_path.suffix.lower() == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {config_path.suffix}")
        
        return self._parse_config_data(data)
    
    def _parse_config_data(self, data: Dict) -> BatchJob:
        """Parse configuration data into BatchJob"""
        clips = []
        
        for clip_data in data.get('clips', []):
            clip = ClipRequest(
                url=clip_data['url'],
                start_time=str(clip_data['start_time']),
                end_time=str(clip_data['end_time']),
                output_filename=clip_data.get('output_filename'),
                description=clip_data.get('description')
            )
            clips.append(clip)
        
        return BatchJob(
            name=data.get('name', 'Batch Job'),
            output_directory=data.get('output_directory', self.output_base_dir),
            clips=clips
        )
    
    def parse_natural_language(self, text: str) -> List[ClipRequest]:
        """
        Parse natural language text to extract clip requests
        Uses regex patterns to identify URLs and time codes
        
        Args:
            text: Natural language text containing URLs and time codes
            
        Returns:
            List of ClipRequest objects
        """
        clips = []
        
        # Pattern to match YouTube URLs
        url_pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
        
        # Pattern to match time codes (various formats)
        time_patterns = [
            r'(\d{1,2}:\d{2}:\d{2})\s*(?:to|[-–])\s*(\d{1,2}:\d{2}:\d{2})',  # HH:MM:SS to HH:MM:SS
            r'(\d{1,2}:\d{2})\s*(?:to|[-–])\s*(\d{1,2}:\d{2})',              # MM:SS to MM:SS
            r'(\d+)\s*(?:to|[-–])\s*(\d+)\s*(?:seconds?|s)',                 # X to Y seconds
            r'(?:from\s+)?(\d{1,2}:\d{2}:\d{2})\s+(?:to\s+)?(\d{1,2}:\d{2}:\d{2})',  # from X to Y
            r'(?:from\s+)?(\d{1,2}:\d{2})\s+(?:to\s+)?(\d{1,2}:\d{2})',      # from X to Y (MM:SS)
        ]
        
        lines = text.strip().split('\n')
        current_url = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for YouTube URL
            url_match = re.search(url_pattern, line)
            if url_match:
                current_url = line if line.startswith('http') else f"https://www.youtube.com/watch?v={url_match.group(1)}"
                continue
            
            # Check for time codes
            if current_url:
                for pattern in time_patterns:
                    time_match = re.search(pattern, line)
                    if time_match:
                        start_time = time_match.group(1)
                        end_time = time_match.group(2)
                        
                        # Generate filename if not provided
                        output_filename = self._generate_filename(current_url, start_time, end_time)
                        
                        clips.append(ClipRequest(
                            url=current_url,
                            start_time=start_time,
                            end_time=end_time,
                            output_filename=output_filename,
                            description=line
                        ))
                        break
        
        return clips
    
    def _generate_filename(self, url: str, start_time: str, end_time: str) -> str:
        """Generate a filename for a clip"""
        # Extract video ID from URL
        video_id_match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)', url)
        video_id = video_id_match.group(1) if video_id_match else "video"
        
        def clean_time_for_filename(time_str):
            """Clean time string for use in filename"""
            # Split by colons to handle different time formats
            parts = time_str.split(':')
            
            if len(parts) == 1:
                # Just seconds or "X seconds" format
                return time_str.replace(' seconds', 's').replace(' ', '')
            elif len(parts) == 2:
                # MM:SS format
                return f"{parts[0]}m{parts[1]}s"
            elif len(parts) == 3:
                # HH:MM:SS format
                return f"{parts[0]}h{parts[1]}m{parts[2]}s"
            else:
                return time_str.replace(':', 'm') + 's'
        
        start_clean = clean_time_for_filename(start_time)
        end_clean = clean_time_for_filename(end_time)
        
        return f"{video_id}_{start_clean}-{end_clean}.mp4"
    
    def create_batch_job_from_text(self, text: str, job_name: str = None) -> BatchJob:
        """
        Create a BatchJob from natural language text
        
        Args:
            text: Natural language text
            job_name: Optional name for the batch job
            
        Returns:
            BatchJob object
        """
        clips = self.parse_natural_language(text)
        
        if not clips:
            raise ValueError("No clips found in the provided text")
        
        return BatchJob(
            name=job_name or f"Batch Job {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            output_directory=self.output_base_dir,
            clips=clips
        )
    
    def execute_batch_job(self, batch_job: BatchJob) -> Dict[str, any]:
        """
        Execute a batch job to extract all clips
        
        Args:
            batch_job: BatchJob to execute
            
        Returns:
            Dictionary with execution results
        """
        # Create output directory
        output_dir = Path(batch_job.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"=== Executing Batch Job: {batch_job.name} ===")
        print(f"Output directory: {output_dir.absolute()}")
        print(f"Total clips to extract: {len(batch_job.clips)}")
        print()
        
        successful_clips = 0
        failed_clips = []
        
        for i, clip in enumerate(batch_job.clips, 1):
            print(f"[{i}/{len(batch_job.clips)}] Processing clip...")
            
            # Generate output filename if not provided
            if not clip.output_filename:
                clip.output_filename = self._generate_filename(
                    clip.url, clip.start_time, clip.end_time
                )
            
            output_path = output_dir / clip.output_filename
            
            # Execute YouClip
            success = self._extract_single_clip(
                clip.url, 
                clip.start_time, 
                clip.end_time, 
                str(output_path)
            )
            
            if success:
                successful_clips += 1
                print(f"✅ Successfully created: {clip.output_filename}")
            else:
                failed_clips.append(clip)
                print(f"❌ Failed to create: {clip.output_filename}")
            
            print()
        
        # Generate summary
        results = {
            'job_name': batch_job.name,
            'total_clips': len(batch_job.clips),
            'successful': successful_clips,
            'failed': len(failed_clips),
            'failed_clips': failed_clips,
            'output_directory': str(output_dir.absolute())
        }
        
        self._print_summary(results)
        return results
    
    def _extract_single_clip(self, url: str, start_time: str, end_time: str, output_path: str) -> bool:
        """Extract a single clip using YouClip"""
        try:
            cmd = [
                "python3", "youclip.py",
                url,
                str(start_time),
                str(end_time),
                "-o", output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def _print_summary(self, results: Dict):
        """Print execution summary"""
        print("=== Batch Job Summary ===")
        print(f"Job: {results['job_name']}")
        print(f"✅ Successful clips: {results['successful']}")
        print(f"❌ Failed clips: {results['failed']}")
        print(f"📁 Output directory: {results['output_directory']}")
        
        if results['failed'] > 0:
            print(f"\n⚠️  {results['failed']} clips failed to extract.")
            for clip in results['failed_clips']:
                print(f"   - {clip.url} ({clip.start_time} to {clip.end_time})")
        else:
            print("\n🎉 All clips extracted successfully!")
    
    def export_job_config(self, batch_job: BatchJob, output_path: str):
        """Export a BatchJob to a configuration file"""
        config_data = {
            'name': batch_job.name,
            'output_directory': batch_job.output_directory,
            'created_at': batch_job.created_at,
            'clips': [
                {
                    'url': clip.url,
                    'start_time': clip.start_time,
                    'end_time': clip.end_time,
                    'output_filename': clip.output_filename,
                    'description': clip.description
                }
                for clip in batch_job.clips
            ]
        }
        
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if output_path.suffix.lower() == '.yaml':
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            else:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuration exported to: {output_path}") 