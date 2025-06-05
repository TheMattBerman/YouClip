#!/bin/bash

# YouClip Batch Processing Example
# This script demonstrates how to extract multiple clips from YouTube videos

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== YouClip Batch Processing Example ===${NC}"
echo

# Example video URL (replace with your own)
VIDEO_URL="https://youtube.com/watch?v=dQw4w9WgXcQ"

# Create output directory
OUTPUT_DIR="clips"
mkdir -p "$OUTPUT_DIR"

echo -e "${YELLOW}Processing video: $VIDEO_URL${NC}"
echo -e "${YELLOW}Output directory: $OUTPUT_DIR${NC}"
echo

# Function to extract clip with error handling
extract_clip() {
    local url="$1"
    local start_time="$2"
    local end_time="$3"
    local output_file="$4"
    local extra_args="$5"
    
    echo -e "${BLUE}Extracting: $output_file (${start_time} to ${end_time})${NC}"
    
    if python youclip.py "$url" "$start_time" "$end_time" -o "$OUTPUT_DIR/$output_file" $extra_args; then
        echo -e "${GREEN}✅ Successfully created: $output_file${NC}"
    else
        echo -e "${RED}❌ Failed to create: $output_file${NC}"
    fi
    echo
}

# Example 1: Extract intro (first 30 seconds)
extract_clip "$VIDEO_URL" "0" "30" "intro.mp4"

# Example 2: Extract a middle segment (1:30 to 2:15)
extract_clip "$VIDEO_URL" "1:30" "2:15" "middle_segment.mp4"

# Example 3: Extract audio-only clip (2:30 to 3:00)
extract_clip "$VIDEO_URL" "2:30" "3:00" "audio_sample.mp3" "--audio-only"

# Example 4: Extract ending (last 45 seconds - you'll need to know video duration)
# extract_clip "$VIDEO_URL" "3:15" "4:00" "ending.mp4"

# Example 5: Extract multiple short clips for highlights reel
HIGHLIGHTS=(
    "0:15 0:25 highlight_1.mp4"
    "0:45 0:55 highlight_2.mp4"
    "1:15 1:25 highlight_3.mp4"
)

echo -e "${YELLOW}Creating highlights reel clips:${NC}"
for highlight in "${HIGHLIGHTS[@]}"; do
    read -r start end filename <<< "$highlight"
    extract_clip "$VIDEO_URL" "$start" "$end" "$filename"
done

# Show results
echo -e "${GREEN}=== Processing Complete ===${NC}"
echo -e "${BLUE}Created files:${NC}"
ls -la "$OUTPUT_DIR/"

echo
echo -e "${YELLOW}Tips:${NC}"
echo "- Use 'python youclip.py URL --preview' to check video duration first"
echo "- Modify the VIDEO_URL variable to process different videos"
echo "- Adjust time ranges according to your video content"
echo "- Add --audio-only flag for audio extraction" 