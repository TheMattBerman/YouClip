# YouClip Batch Extraction System

The YouClip Batch Extraction system allows you to extract multiple clips from YouTube videos en masse using various input formats. This modular system uses AI-powered parsing to understand natural language requests and can process clips from multiple videos in a single operation.

## Features

- 🤖 **AI-Powered Parsing**: Understands natural language descriptions of video clips
- 📄 **Multiple Input Formats**: Supports text files, JSON, YAML, and interactive input
- 🔄 **Modular Design**: Easy to extend and customize
- 📊 **Progress Tracking**: Shows detailed progress and results
- 🎯 **Flexible Time Formats**: Supports various time code formats
- 📁 **Organized Output**: Automatically organizes clips in directories
- 🔧 **Configuration Export**: Generate template files for reuse

## Quick Start

### 1. Natural Language Text File

Create a text file with URLs and time codes:

```text
# my_clips.txt
https://www.youtube.com/watch?v=ABC123
1:30 to 2:45
5:10 to 5:30

https://www.youtube.com/watch?v=XYZ789
from 0:10 to 0:25
2:15 - 2:45
```

Extract clips:

```bash
python3 batch_extract.py -i my_clips.txt
```

### 2. Interactive Mode

```bash
python3 batch_extract.py --interactive
```

Then enter URLs and time codes when prompted.

### 3. JSON Configuration

```bash
python3 batch_extract.py -i examples/clips_example.json
```

### 4. YAML Configuration

```bash
python3 batch_extract.py -i examples/clips_example.yaml
```

## Usage Examples

### Basic Usage

```bash
# Extract from text file
python3 batch_extract.py -i clips.txt

# Custom output directory
python3 batch_extract.py -i clips.txt -o my_videos

# Interactive mode
python3 batch_extract.py --interactive

# Dry run (preview without extracting)
python3 batch_extract.py -i clips.txt --dry-run
```

### Advanced Usage

```bash
# Custom job name
python3 batch_extract.py -i clips.txt --job-name "My Collection"

# Export configuration template
python3 batch_extract.py --export-template template.json
```

## Input Formats

### Natural Language Text Files

The system understands various natural language patterns:

```text
# Comments are ignored
https://www.youtube.com/watch?v=VIDEO_ID

# Various time formats
1:30 to 2:45          # MM:SS format
14:09 to 14:12        # MM:SS format
1:23:45 to 1:25:30    # HH:MM:SS format
30 to 60 seconds      # Seconds only
from 1:30 to 2:00     # "from X to Y" format
1:30 - 2:00           # Dash separator
1:30 – 2:00           # En-dash separator

# Descriptions (optional)
This is a funny moment
```

### JSON Configuration

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

### YAML Configuration

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

## Supported Time Formats

The system supports various time code formats:

- `MM:SS` (e.g., `1:30`, `14:09`)
- `HH:MM:SS` (e.g., `1:23:45`)
- Seconds only (e.g., `90`, `120`)
- Natural language (e.g., `1 to 4 seconds`)

## Time Range Separators

- `to` - `1:30 to 2:45`
- `-` - `1:30 - 2:45`
- `–` - `1:30 – 2:45` (en-dash)
- `from...to` - `from 1:30 to 2:45`

## Command Line Options

| Option              | Description                                   |
| ------------------- | --------------------------------------------- |
| `-i, --input`       | Input file (text, JSON, or YAML)              |
| `-o, --output`      | Output directory (default: extracted_clips)   |
| `--interactive`     | Interactive mode - enter clips manually       |
| `--export-template` | Export a configuration template file          |
| `--job-name`        | Name for the batch job                        |
| `--dry-run`         | Show what would be extracted without doing it |

## Examples Directory

The `examples/` directory contains sample files:

- `clips_example.txt` - Natural language format
- `clips_example.json` - JSON configuration
- `clips_example.yaml` - YAML configuration
- `batch_example.sh` - Shell script example

## Output Structure

```
extracted_clips/
├── VIDEO_ID_1m30s-2m45s.mp4
├── VIDEO_ID_5m10s-5m30s.mp4
└── ...
```

Filenames are automatically generated based on:

- Video ID from the URL
- Start and end times
- Or custom filenames from configuration

## Error Handling

The system provides detailed error reporting:

- ✅ Success indicators for completed clips
- ❌ Error messages for failed extractions
- 📊 Summary statistics at the end
- 🔍 Detailed progress tracking

## Integration with Existing YouClip

The batch system is fully compatible with the existing YouClip functionality:

- Uses the same underlying video processing
- Respects all YouClip settings and options
- Maintains the same output quality and formats
- Can be used alongside individual clip extraction

## Programming Interface

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

## Requirements

The batch extraction system requires the same dependencies as YouClip:

- Python 3.6+
- yt-dlp
- ffmpeg
- Optional: PyYAML (for YAML support)

Install YAML support:

```bash
pip install PyYAML
```

## Troubleshooting

### Common Issues

1. **No clips found in text**: Check time format and URL format
2. **YAML errors**: Install PyYAML with `pip install PyYAML`
3. **Permission errors**: Ensure write access to output directory
4. **ffmpeg errors**: Check ffmpeg installation and PATH

### Debug Mode

Use `--dry-run` to see what the system would extract:

```bash
python3 batch_extract.py -i clips.txt --dry-run
```

## Migration from Existing Scripts

If you have existing extraction scripts like `extract_user_clips.py`, you can easily migrate:

1. Convert your clip data to one of the supported formats
2. Use the new batch extraction system
3. Enjoy improved error handling and progress tracking

The new system is backward compatible and provides all the same functionality with additional features.
