#!/usr/bin/env python3
"""
Script to extract additional clips from YouTube videos using YouClip
Now uses the new modular batch processing system!

This script is maintained for backward compatibility, but the new
batch_extract.py provides much more functionality.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path to import utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.batch_processor import BatchProcessor, ClipRequest, BatchJob


def main():
    """Main function to process all additional clips using the new batch system"""
    
    print("=== YouClip Additional Clips Extraction ===")
    print("ℹ️  This script now uses the new modular batch processing system!")
    print("   For more features, try: python3 batch_extract.py")
    print()
    
    # Create the clips using the new modular system
    clips = [
        # Video 7: https://www.youtube.com/watch?v=WMmbg73rHEM
        ClipRequest(
            url="https://www.youtube.com/watch?v=WMmbg73rHEM",
            start_time="14:09",
            end_time="14:12",
            output_filename="video7_clip1_14m09s-14m12s.mp4",
            description="Video 7 clip 1"
        ),
        # Video 8: https://www.youtube.com/watch?v=eKwkoybyS_w
        ClipRequest(
            url="https://www.youtube.com/watch?v=eKwkoybyS_w",
            start_time="1",
            end_time="4",
            output_filename="video8_clip1_1s-4s.mp4",
            description="Video 8 clip 1"
        ),
        ClipRequest(
            url="https://www.youtube.com/watch?v=eKwkoybyS_w",
            start_time="1:35",
            end_time="1:40",
            output_filename="video8_clip2_1m35s-1m40s.mp4",
            description="Video 8 clip 2"
        ),
        ClipRequest(
            url="https://www.youtube.com/watch?v=eKwkoybyS_w",
            start_time="1:58",
            end_time="2:02",
            output_filename="video8_clip3_1m58s-2m02s.mp4",
            description="Video 8 clip 3"
        )
    ]
    
    # Create batch job
    batch_job = BatchJob(
        name="Additional Clips Extraction",
        output_directory="extracted_clips",
        clips=clips
    )
    
    # Initialize batch processor and execute
    processor = BatchProcessor()
    results = processor.execute_batch_job(batch_job)
    
    # Exit with error code if any clips failed
    if results['failed'] > 0:
        sys.exit(1)
    
    print("\n💡 Pro tip: For more advanced features, try the new batch_extract.py:")
    print("   - Natural language input: python3 batch_extract.py -i clips.txt")
    print("   - Interactive mode: python3 batch_extract.py --interactive")
    print("   - JSON/YAML configs: python3 batch_extract.py -i config.json")


if __name__ == "__main__":
    main() 