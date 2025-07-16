# YouClip - YouTube Video Clip Downloader

A powerful command-line tool to download specific segments from YouTube videos using ffmpeg. Extract the exact parts you need from any YouTube video with ease!

## ✨ Features

- **Precise Clipping**: Download exact segments using start and end times
- **🚀 Batch Extraction**: Process multiple clips from multiple videos with AI-powered parsing
- **🤖 Natural Language Input**: Understands "1:30 to 2:45" and other natural time expressions
- **📄 Multiple Input Formats**: Text files, JSON, YAML, and interactive input
- **High Quality Video**: Support for 720p, 1080p, 1440p, 2160p (4K), and best available quality
- **Multiple Time Formats**: Supports HH:MM:SS, MM:SS, or seconds
- **Audio Extraction**: Option to extract audio-only clips (MP3)
- **Smart Naming**: Automatically generates descriptive filenames
- **Progress Tracking**: Real-time download and processing progress
- **Input Validation**: Comprehensive validation for URLs and time ranges
- **Interactive Mode**: User-friendly prompts for easy operation
- **CLI Mode**: Full command-line interface for automation
- **Preview Mode**: Check video information before downloading

## 🛠️ Prerequisites

### FFmpeg Installation

**macOS (using Homebrew):**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**

1. Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract and add to your PATH environment variable
3. Or use: `winget install ffmpeg`

**Verify Installation:**

```bash
ffmpeg -version
```

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/YouClip.git
   cd YouClip
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Make the script executable (optional):**
   ```bash
   chmod +x youclip.py
   ```

## ⚡ Quick Start

**For GUI users (easiest):**

```bash
python3 launch_gui.py
```

**For CLI users:**

```bash
# Interactive mode
python3 youclip.py

# Direct command
python3 youclip.py "https://youtube.com/watch?v=VIDEO_ID" 1:30 2:00
```

## 🚀 Usage

### GUI Mode (Recommended for all users)

Launch the modern graphical user interface:

```bash
python3 youclip_gui.py
# or use the launcher with dependency checks
python3 launch_gui.py
```

The GUI provides:

- **Easy URL input** with real-time validation
- **Video preview** showing title, duration, and uploader
- **Visual time range selection** with format helpers
- **Output options** for video/audio with auto-filename generation
- **Progress tracking** with real-time status updates
- **File browser** for easy output location selection
- **Status logging** for troubleshooting

### Interactive CLI Mode (Terminal-based)

For terminal enthusiasts, run the CLI without arguments:

```bash
python3 youclip.py
```

The interactive mode will guide you through:

- Entering the YouTube URL
- Selecting video or audio-only extraction
- Specifying start and end times
- Choosing output filename

### Command Line Mode

For automation and quick operations:

**Basic Usage:**

```bash
python youclip.py "YOUTUBE_URL" START_TIME END_TIME
```

**Examples:**

1. **Extract 30-second clip (from 1:30 to 2:00):**

   ```bash
   python youclip.py "https://youtube.com/watch?v=dQw4w9WgXcQ" 1:30 2:00
   ```

2. **Extract using seconds:**

   ```bash
   python youclip.py "https://youtube.com/watch?v=dQw4w9WgXcQ" 90 120
   ```

3. **Custom output filename:**

   ```bash
   python youclip.py "https://youtube.com/watch?v=dQw4w9WgXcQ" 1:30 3:45 -o "my_clip.mp4"
   ```

4. **High quality 4K download:**

   ```bash
   python youclip.py "https://youtube.com/watch?v=dQw4w9WgXcQ" 1:30 3:45 --quality 2160p
   ```

5. **Best available quality:**

   ```bash
   python youclip.py "https://youtube.com/watch?v=dQw4w9WgXcQ" 0:30 2:00 --quality best
   ```

6. **Audio-only extraction:**

   ```bash
   python youclip.py "https://youtube.com/watch?v=dQw4w9WgXcQ" 0:30 2:00 --audio-only
   ```

7. **Preview video information:**
   ```bash
   python youclip.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --preview
   ```

### Time Format Examples

YouClip supports multiple time formats:

- **Seconds**: `30`, `120`, `1800`
- **MM:SS**: `1:30`, `5:45`, `12:00`
- **HH:MM:SS**: `0:01:30`, `1:05:45`, `2:30:00`

### Command Line Options

```
usage: youclip.py [-h] [-o OUTPUT] [--audio-only] [--quality {720p,1080p,1440p,2160p,best}]
                  [--preview] [--version] [url] [start] [end]

positional arguments:
  url                   YouTube video URL
  start                 Start time (HH:MM:SS, MM:SS, or seconds)
  end                   End time (HH:MM:SS, MM:SS, or seconds)

optional arguments:
  -h, --help           show this help message and exit
  -o OUTPUT, --output OUTPUT
                       Output filename
  --audio-only         Extract audio only (MP3)
  --quality {720p,1080p,1440p,2160p,best}
                       Maximum video quality (default: 1440p)
  --preview           Preview video information only
  --version           show program's version number and exit
```

## 📁 Output Files

### Default Naming Convention

YouClip automatically creates descriptive filenames:

```
VideoTitle_clip_START_to_END.extension
```

**Examples:**

- `How to Code in Python_clip_01-30-000_to_03-45-500.mp4`
- `Best Music Mix_clip_00-30-000_to_02-00-000.mp3`

### Custom Filenames

Use the `-o` or `--output` option to specify custom filenames:

```bash
python youclip.py "URL" 1:30 2:00 -o "important_segment.mp4"
```

## 🔧 Advanced Usage

### Batch Processing

Create a script for multiple clips:

```bash
#!/bin/bash

# Multiple clips from the same video
VIDEO_URL="https://youtube.com/watch?v=dQw4w9WgXcQ"

python youclip.py "$VIDEO_URL" 0:30 1:00 -o "intro.mp4"
python youclip.py "$VIDEO_URL" 2:30 3:45 -o "main_part.mp4"
python youclip.py "$VIDEO_URL" 5:00 5:30 --audio-only -o "outro_music.mp3"
```

## 🚀 Batch Extraction System

YouClip now features a powerful modular batch extraction system that can process multiple clips from multiple videos using AI-powered parsing!

### 🎯 Key Features

- **🤖 AI-Powered Parsing**: Understands natural language descriptions
- **📄 Multiple Input Formats**: Text files, JSON, YAML, and interactive input
- **🔄 Modular Design**: Easy to extend and customize
- **📊 Progress Tracking**: Detailed progress and error reporting
- **🎯 Flexible Time Formats**: Supports various time code formats

### Quick Start Examples

**1. Natural Language Text File:**

Create a text file (`my_clips.txt`) with URLs and time codes:

```text
# Video highlights collection
https://www.youtube.com/watch?v=ABC123
1:30 to 2:45
5:10 to 5:30

https://www.youtube.com/watch?v=XYZ789
from 0:10 to 0:25
2:15 - 2:45
```

Extract all clips:

```bash
python3 batch_extract.py -i my_clips.txt
```

**2. Interactive Mode:**

```bash
python3 batch_extract.py --interactive
```

**3. JSON Configuration:**

```bash
python3 batch_extract.py -i examples/clips_example.json
```

**4. YAML Configuration:**

```bash
python3 batch_extract.py -i examples/clips_example.yaml
```

### Command Line Options

```bash
# Basic usage
python3 batch_extract.py -i clips.txt

# Custom output directory
python3 batch_extract.py -i clips.txt -o my_videos

# Dry run (preview without extracting)
python3 batch_extract.py -i clips.txt --dry-run

# Custom job name
python3 batch_extract.py -i clips.txt --job-name "My Collection"

# Export configuration template
python3 batch_extract.py --export-template template.json
```

### Supported Input Formats

**Natural Language Text:**

```text
# Comments are ignored
https://www.youtube.com/watch?v=VIDEO_ID

# Various time formats work
1:30 to 2:45          # MM:SS format
14:09 to 14:12        # MM:SS format
1:23:45 to 1:25:30    # HH:MM:SS format
30 to 60 seconds      # Seconds only
from 1:30 to 2:00     # "from X to Y" format
1:30 - 2:00           # Dash separator
```

**JSON Configuration:**

```json
{
  "name": "My Clips Collection",
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
```

**YAML Configuration:**

```yaml
name: "My Clips Collection"
output_directory: "extracted_clips"
clips:
  - url: "https://www.youtube.com/watch?v=ABC123"
    start_time: "1:30"
    end_time: "2:45"
    output_filename: "clip1.mp4"
    description: "Funny moment"
```

### Programming Interface

You can also use the batch processor programmatically:

```python
from utils.batch_processor import BatchProcessor, ClipRequest, BatchJob

# Create processor
processor = BatchProcessor(output_base_dir="my_clips")

# Create clips programmatically
clips = [
    ClipRequest(
        url="https://www.youtube.com/watch?v=ABC123",
        start_time="1:30",
        end_time="2:45",
        output_filename="my_clip.mp4"
    )
]

# Create and execute batch job
batch_job = BatchJob(
    name="My Job",
    output_directory="clips",
    clips=clips
)

results = processor.execute_batch_job(batch_job)
```

### Backward Compatibility

Your existing scripts still work! The old `extract_additional_clips.py` now uses the new modular system internally while maintaining the same interface.

### Integration with Other Tools

YouClip can be easily integrated into larger workflows:

```python
import subprocess
import sys

def extract_clip(url, start, end, output):
    cmd = [sys.executable, "youclip.py", url, start, end, "-o", output]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

# Usage
success = extract_clip(
    "https://youtube.com/watch?v=dQw4w9WgXcQ",
    "1:30", "2:00", "my_clip.mp4"
)
```

## 🐛 Troubleshooting

### Common Issues

**1. "FFmpeg not found" error:**

- Ensure ffmpeg is installed and in your PATH
- Test with: `ffmpeg -version`

**2. "Invalid YouTube URL" error:**

- Check the URL format
- Ensure the video is publicly accessible
- Try copying the URL directly from YouTube

**3. "Download failed" error:**

- Check your internet connection
- Some videos may be geo-restricted or require login
- Try a different video to test

**4. "Time exceeds video duration" error:**

- Use `--preview` to check video duration first
- Ensure your end time is less than the video length

**5. Permission errors:**

- Ensure you have write permissions in the output directory
- Try specifying a different output location

### Performance Tips

1. **For shorter clips**: The tool downloads the full video first, then clips it. This ensures maximum quality but may take longer for very long videos.

2. **Audio-only extraction**: Use `--audio-only` for faster processing when you only need audio.

3. **Network issues**: The tool includes retry mechanisms, but unstable connections may cause failures.

### Debug Mode

For detailed error information, you can modify the script to show more verbose output:

```bash
python -u youclip.py "URL" 1:30 2:00 2>&1 | tee debug.log
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Legal Notice

This tool is for educational and personal use only. Users are responsible for complying with YouTube's Terms of Service and copyright laws. Only download content you have permission to use.

## 🔗 Dependencies

- **yt-dlp**: YouTube video information and download
- **ffmpeg**: Video/audio processing and clipping
- **colorama**: Cross-platform colored terminal output
- **tqdm**: Progress bars
- **click**: Command-line interface utilities
- **validators**: Input validation

## 📊 Project Structure

```
YouClip/
├── youclip.py                 # CLI application
├── youclip_gui.py             # GUI application
├── launch_gui.py              # GUI launcher with checks
├── batch_extract.py           # Batch extraction system
├── extract_additional_clips.py # Legacy batch script (now uses new system)
├── extract_user_clips.py      # User clips batch script
├── requirements.txt           # Python dependencies
├── setup.py                  # Automated setup script
├── test_youclip.py           # Test suite
├── README.md                 # This file
├── BATCH_EXTRACTION.md       # Detailed batch extraction docs
├── utils/
│   ├── __init__.py
│   ├── video_processor.py     # Core video processing
│   ├── batch_processor.py     # Batch processing engine
│   ├── time_parser.py         # Time format handling
│   └── validators.py          # Input validation
└── examples/                 # Usage examples
    ├── batch_example.sh        # Batch processing script
    ├── python_integration.py   # API integration examples
    ├── clips_example.txt       # Natural language format
    ├── clips_example.json      # JSON configuration
    └── clips_example.yaml      # YAML configuration
```

## 🆕 Version History

### v1.0.0

- Initial release
- Interactive and CLI modes
- Audio/video extraction
- Comprehensive time format support
- Progress tracking and error handling

---

**Happy clipping! 🎬✂️**
