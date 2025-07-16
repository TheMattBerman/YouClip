#!/usr/bin/env python3
"""
Script to extract specific clips from YouTube videos using YouClip
"""

import os
import subprocess
import sys
from pathlib import Path

def run_youclip(url, start_time, end_time, output_file):
    """Run YouClip to extract a single clip"""
    try:
        print(f"Extracting: {output_file} ({start_time} to {end_time})")
        
        cmd = [
            "python3", "youclip.py",
            url,
            str(start_time),
            str(end_time),
            "-o", output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully created: {output_file}")
            return True
        else:
            print(f"❌ Failed to create: {output_file}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {output_file}: {str(e)}")
        return False

def main():
    """Main function to process all requested clips"""
    
    # Create output directory
    output_dir = "extracted_clips"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=== YouClip Batch Extraction ===")
    print(f"Output directory: {output_dir}")
    print()
    
    # List of all clips to extract
    clips = [
        # Video 1: https://www.youtube.com/watch?v=uwLa-jUakIw
        {
            "url": "https://www.youtube.com/watch?v=uwLa-jUakIw",
            "clips": [
                ("56", "1:03", "video1_clip1_56s-1m03s.mp4"),
                ("6:24", "6:50", "video1_clip2_6m24s-6m50s.mp4"),
                ("7:17", "7:21", "video1_clip3_7m17s-7m21s.mp4")
            ]
        },
        # Video 2: https://www.youtube.com/watch?v=A1GkssdJLfQ
        {
            "url": "https://www.youtube.com/watch?v=A1GkssdJLfQ",
            "clips": [
                ("23", "39", "video2_clip1_23s-39s.mp4"),
                ("3:22", "3:30", "video2_clip2_3m22s-3m30s.mp4")
            ]
        },
        # Video 3: https://www.youtube.com/watch?v=XWzQMUIwZQI
        {
            "url": "https://www.youtube.com/watch?v=XWzQMUIwZQI",
            "clips": [
                ("11", "1:00", "video3_clip1_11s-1m00s.mp4"),
                ("2:18", "2:22", "video3_clip2_2m18s-2m22s.mp4"),
                ("4:17", "4:36", "video3_clip3_4m17s-4m36s.mp4"),
                ("5:13", "5:25", "video3_clip4_5m13s-5m25s.mp4"),
                ("8:27", "8:37", "video3_clip5_8m27s-8m37s.mp4")
            ]
        },
        # Video 4: https://www.youtube.com/watch?v=L_M8bKZKI-w
        {
            "url": "https://www.youtube.com/watch?v=L_M8bKZKI-w",
            "clips": [
                ("6", "12", "video4_clip1_6s-12s.mp4"),
                ("21", "28", "video4_clip2_21s-28s.mp4")
            ]
        },
        # Video 5: https://www.youtube.com/watch?v=aRQIuFqCr28
        {
            "url": "https://www.youtube.com/watch?v=aRQIuFqCr28",
            "clips": [
                ("1:08", "1:10", "video5_clip1_1m08s-1m10s.mp4"),
                ("1:39", "1:43", "video5_clip2_1m39s-1m43s.mp4"),
                ("4:28", "4:38", "video5_clip3_4m28s-4m38s.mp4")
            ]
        },
        # Video 6: https://www.youtube.com/watch?v=WfohKfs1dAg
        {
            "url": "https://www.youtube.com/watch?v=WfohKfs1dAg",
            "clips": [
                ("16", "44", "video6_clip1_16s-44s.mp4")
            ]
        }
    ]
    
    successful_clips = 0
    failed_clips = 0
    
    # Process each video and its clips
    for video_data in clips:
        url = video_data["url"]
        print(f"\n📹 Processing video: {url}")
        
        for start_time, end_time, filename in video_data["clips"]:
            output_path = os.path.join(output_dir, filename)
            
            if run_youclip(url, start_time, end_time, output_path):
                successful_clips += 1
            else:
                failed_clips += 1
            
            print()  # Add spacing between clips
    
    # Summary
    print("=== Summary ===")
    print(f"✅ Successful clips: {successful_clips}")
    print(f"❌ Failed clips: {failed_clips}")
    print(f"📁 Output directory: {os.path.abspath(output_dir)}")
    
    if failed_clips > 0:
        print("\n⚠️  Some clips failed to extract. Check the error messages above.")
        sys.exit(1)
    else:
        print("\n🎉 All clips extracted successfully!")

if __name__ == "__main__":
    main() 