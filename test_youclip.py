#!/usr/bin/env python3
"""
Test script for YouClip
Tests core functionality without actually downloading videos
"""

import sys
from utils.time_parser import TimeParser
from utils.validators import Validators
from utils.video_processor import VideoProcessor


def test_time_parser():
    """Test time parsing functionality"""
    print("Testing TimeParser...")
    
    test_cases = [
        ("30", 30.0),
        ("1:30", 90.0),
        ("0:01:30", 90.0),
        ("2:30:45", 9045.0)
    ]
    
    for time_str, expected in test_cases:
        try:
            result = TimeParser.parse_time(time_str)
            status = "✅" if result == expected else "❌"
            print(f"  {status} {time_str} -> {result}s (expected {expected}s)")
        except Exception as e:
            print(f"  ❌ {time_str} -> Error: {e}")


def test_validators():
    """Test validation functionality"""
    print("\nTesting Validators...")
    
    # Test YouTube URL validation
    urls = [
        ("https://youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://youtu.be/dQw4w9WgXcQ", True),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://example.com/video", False),
        ("not-a-url", False)
    ]
    
    for url, expected in urls:
        result = Validators.is_valid_youtube_url(url)
        status = "✅" if result == expected else "❌"
        print(f"  {status} URL validation: {url[:30]}... -> {result}")
    
    # Test filename sanitization
    filenames = [
        ("normal_file.mp4", "normal_file.mp4"),
        ("file with spaces.mp4", "file with spaces.mp4"),
        ('file<with>bad|chars.mp4', "file_with_bad_chars.mp4"),
        ("", "untitled")
    ]
    
    for filename, expected in filenames:
        result = Validators.sanitize_filename(filename)
        status = "✅" if result == expected else "❌"
        print(f"  {status} Filename sanitization: '{filename}' -> '{result}'")


def test_dependencies():
    """Test dependency checking"""
    print("\nTesting Dependencies...")
    
    success, message = VideoProcessor.check_dependencies()
    status = "✅" if success else "❌"
    print(f"  {status} {message}")


def test_video_info_structure():
    """Test that we can import and create processor instance"""
    print("\nTesting VideoProcessor initialization...")
    
    try:
        processor = VideoProcessor()
        print("  ✅ VideoProcessor created successfully")
    except Exception as e:
        print(f"  ❌ Failed to create VideoProcessor: {e}")


def main():
    """Run all tests"""
    print("YouClip Test Suite")
    print("=" * 50)
    
    test_time_parser()
    test_validators()
    test_dependencies()
    test_video_info_structure()
    
    print("\n" + "=" * 50)
    print("Test suite completed!")
    print("\nTo test with real YouTube videos, run:")
    print("python3 youclip.py --preview \"https://youtube.com/watch?v=VIDEO_ID\"")


if __name__ == '__main__':
    main() 