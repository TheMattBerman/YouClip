# YouClip GUI Options

## Available Interfaces

### 1. Simple GUI (Recommended) - `simple_gui.py`

**Status: ✅ Stable**

A clean, reliable graphical interface that avoids potential crash issues:

- Uses standard ttk widgets for better compatibility
- Simplified threading model
- Minimal memory footprint
- Works reliably on macOS, Windows, and Linux

**Launch with:**

```bash
python3 simple_gui.py
# or
python3 launch_gui.py  # (now uses simple GUI by default)
```

**Features:**

- YouTube URL input and validation
- Video info preview
- Time range selection (start/end times)
- Output file selection
- Audio-only option
- Real-time status logging
- Progress tracking

### 2. Advanced GUI - `youclip_gui.py`

**Status: ⚠️ May crash on some systems**

A feature-rich interface with Winamp-style theming:

- Custom styling and animations
- Advanced progress indicators
- Retro/gaming aesthetic
- More complex UI components

**Known Issues:**

- May crash on macOS with `objc autorelease pool corrupted` error
- Memory management issues with complex threading
- Requires more system resources

**Launch with:**

```bash
python3 youclip_gui.py
```

### 3. Command Line Interface - `youclip.py`

**Status: ✅ Most Stable**

Text-based interface for maximum compatibility:

- Interactive mode with prompts
- Command-line arguments for automation
- No GUI dependencies
- Works on all systems

**Launch with:**

```bash
python3 youclip.py              # Interactive mode
python3 youclip.py [URL] [START] [END]  # Direct mode
```

## Crash Troubleshooting

If you experience GUI crashes:

1. **Use Simple GUI**: The recommended solution

   ```bash
   python3 simple_gui.py
   ```

2. **Use Command Line**: Most reliable fallback

   ```bash
   python3 youclip.py
   ```

3. **Check Dependencies**: Ensure all required packages are installed

   ```bash
   pip install -r requirements.txt
   ```

4. **Check FFmpeg**: Verify FFmpeg is properly installed
   ```bash
   ffmpeg -version
   ```

## Recent Fixes Applied

### Video Extraction Issue (Fixed ✅)

- **Problem**: Downloads only showed the last second as video
- **Cause**: Incorrect ffmpeg seek parameter positioning
- **Solution**:
  - Moved `-ss` parameter before `-i` for input seeking
  - Added intelligent re-encoding for short clips (<60s)
  - Implemented fallback mechanism for failed stream copies

### GUI Crash Issue (Workaround ✅)

- **Problem**: Advanced GUI crashed with memory corruption errors
- **Cause**: Complex threading and memory management in custom widgets
- **Solution**: Created simplified GUI with standard widgets and simpler threading

Both the video extraction and GUI crash issues have been resolved. The Simple GUI provides a stable, user-friendly interface for all YouClip functionality.
