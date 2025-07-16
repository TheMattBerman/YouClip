#!/usr/bin/env python3
"""
YouClip Batch Extractor - Modular mass clip extraction
Extract multiple clips from YouTube videos using various input formats
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

# Add the current directory to Python path to import utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.batch_processor import BatchProcessor, BatchJob


def main():
    """Main function for batch extraction"""
    parser = argparse.ArgumentParser(
        description="YouClip Batch Extractor - Extract multiple clips from YouTube videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from natural language text file
  python3 batch_extract.py -i clips.txt

  # Extract from JSON configuration
  python3 batch_extract.py -i clips.json

  # Extract from YAML configuration  
  python3 batch_extract.py -i clips.yaml

  # Interactive mode - enter URLs and time codes
  python3 batch_extract.py --interactive

  # Specify custom output directory
  python3 batch_extract.py -i clips.txt -o my_clips

  # Export configuration template
  python3 batch_extract.py --export-template clips_template.json

Input formats:
  - Text files with URLs and time codes in natural language
  - JSON configuration files
  - YAML configuration files
  - Interactive command-line input

Text file format example:
  https://www.youtube.com/watch?v=ABC123
  1:30 to 2:45
  5:10 to 5:30
  
  https://www.youtube.com/watch?v=XYZ789
  from 0:10 to 0:25
  2:15 - 2:45

JSON/YAML format example:
  {
    "name": "My Clips",
    "output_directory": "extracted_clips",
    "clips": [
      {
        "url": "https://www.youtube.com/watch?v=ABC123",
        "start_time": "1:30",
        "end_time": "2:45",
        "output_filename": "clip1.mp4",
        "description": "Funny moment"
      }
    ]
  }
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        help='Input file (text, JSON, or YAML)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='extracted_clips',
        help='Output directory (default: extracted_clips)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode - enter clips manually'
    )
    
    parser.add_argument(
        '--export-template',
        type=str,
        help='Export a configuration template file'
    )
    
    parser.add_argument(
        '--job-name',
        type=str,
        help='Name for the batch job'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be extracted without actually doing it'
    )
    
    args = parser.parse_args()
    
    # Handle template export
    if args.export_template:
        export_template(args.export_template)
        return
    
    # Initialize batch processor
    processor = BatchProcessor(output_base_dir=args.output)
    
    try:
        if args.interactive:
            batch_job = interactive_mode(processor, args.job_name)
        elif args.input:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"❌ Error: Input file not found: {input_path}")
                sys.exit(1)
            
            # Check if it's a configuration file or text file
            if input_path.suffix.lower() in ['.json', '.yaml', '.yml']:
                batch_job = processor.parse_config_file(str(input_path))
            else:
                # Treat as natural language text file
                with open(input_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                batch_job = processor.create_batch_job_from_text(
                    text, 
                    args.job_name or f"Batch from {input_path.name}"
                )
        else:
            print("❌ Error: No input specified. Use -i for input file or --interactive for interactive mode.")
            parser.print_help()
            sys.exit(1)
        
        # Override output directory if specified
        if args.output != 'extracted_clips':
            batch_job.output_directory = args.output
        
        if args.dry_run:
            print_dry_run(batch_job)
        else:
            # Execute the batch job
            results = processor.execute_batch_job(batch_job)
            
            # Exit with error code if any clips failed
            if results['failed'] > 0:
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def interactive_mode(processor: BatchProcessor, job_name: Optional[str]) -> BatchJob:
    """Interactive mode for entering clips manually"""
    print("=== YouClip Batch Extractor - Interactive Mode ===")
    print("Enter video URLs and time codes. Type 'done' when finished.")
    print("Format examples:")
    print("  https://www.youtube.com/watch?v=ABC123")
    print("  1:30 to 2:45")
    print("  5:10 - 5:30")
    print("  from 0:10 to 0:25")
    print()
    
    text_lines = []
    
    while True:
        try:
            line = input("> ").strip()
            if line.lower() == 'done':
                break
            if line:
                text_lines.append(line)
        except EOFError:
            break
    
    if not text_lines:
        raise ValueError("No input provided")
    
    text = '\n'.join(text_lines)
    return processor.create_batch_job_from_text(
        text, 
        job_name or "Interactive Batch Job"
    )


def print_dry_run(batch_job: BatchJob):
    """Print what would be extracted in a dry run"""
    print(f"=== Dry Run: {batch_job.name} ===")
    print(f"Output directory: {batch_job.output_directory}")
    print(f"Total clips: {len(batch_job.clips)}")
    print()
    
    for i, clip in enumerate(batch_job.clips, 1):
        print(f"[{i}] {clip.url}")
        print(f"    Time: {clip.start_time} to {clip.end_time}")
        print(f"    Output: {clip.output_filename or 'Auto-generated'}")
        if clip.description:
            print(f"    Description: {clip.description}")
        print()
    
    print("Use --dry-run=false or remove --dry-run to actually extract clips.")


def export_template(output_path: str):
    """Export a configuration template"""
    template = {
        "name": "My Clip Collection",
        "output_directory": "extracted_clips",
        "clips": [
            {
                "url": "https://www.youtube.com/watch?v=EXAMPLE1",
                "start_time": "1:30",
                "end_time": "2:45",
                "output_filename": "clip1.mp4",
                "description": "First clip description"
            },
            {
                "url": "https://www.youtube.com/watch?v=EXAMPLE2", 
                "start_time": "0:10",
                "end_time": "0:25",
                "output_filename": "clip2.mp4",
                "description": "Second clip description"
            }
        ]
    }
    
    output_path = Path(output_path)
    
    try:
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Template exported to: {output_path}")
        print(f"\nEdit the template file and run:")
        print(f"python3 batch_extract.py -i {output_path}")
        
    except Exception as e:
        print(f"❌ Error exporting template: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 