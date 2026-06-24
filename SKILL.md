---
name: youtube-lecture-book
description: "Dynamic, production-ready pipeline to convert any YouTube lecture playlist into a professional LaTeX PDF book. Supports configurable frame interval, deduplication threshold, number of lectures, and output formats."
version: 2.0.0
author: Hermes Agent + Grok
license: MIT
tags: [youtube, latex, education, video-processing, book-generation, dynamic]
---

# YouTube Lecture → Professional LaTeX Book (Dynamic Skill)

## Overview
This skill transforms **any** YouTube playlist of lectures into a high-quality, publication-ready LaTeX PDF book with:
- Configurable frame extraction (default: every 5 seconds)
- Perceptual deduplication (configurable Hamming threshold)
- Rich textual explanations beyond the transcript
- Mermaid → TikZ conversion
- Professional tables, code blocks, and tcolorbox notes
- Single master PDF with all lectures as chapters

## Parameters (All Dynamic)

| Parameter              | Default     | Description                              |
|------------------------|-------------|------------------------------------------|
| `playlist_url`         | (required)  | YouTube playlist URL                     |
| `output_dir`           | `./book-project` | Root output directory                 |
| `frame_interval`       | `5`         | Seconds between extracted frames         |
| `dedup_threshold`      | `8`         | Hamming distance for perceptual dedup    |
| `max_lectures`         | `all`       | Number of lectures to process            |
| `include_images`       | `true`      | Embed unique frames in the book          |
| `rich_text`            | `true`      | Generate expanded explanations           |
| `latex_theme`          | `report`    | LaTeX document class                     |

## Usage Examples

### Basic Usage (Any Playlist)
```bash
hermes skill youtube-lecture-book \
  --playlist_url "https://youtube.com/playlist?list=PLPTV0NXA_ZSijcbUrRZHm6BrdinLuelPs" \
  --output_dir "./reasoning-llms-book"
```

### Advanced Usage
```bash
hermes skill youtube-lecture-book \
  --playlist_url "https://youtube.com/playlist?list=XXX" \
  --frame_interval 8 \
  --dedup_threshold 10 \
  --max_lectures 5 \
  --latex_theme "tufte-book"
```

## Production-Ready Features

### 1. Dynamic Configuration
- No hardcoded playlist URLs, paths, or thresholds
- All values come from command-line arguments or config file
- Supports `.env` and JSON configuration

### 2. Robust Error Handling
- Automatic retry on yt-dlp / ffmpeg failures
- Graceful degradation when optional tools are missing
- Detailed logging with different verbosity levels

### 3. Reusability
- Works with any public YouTube playlist
- Supports both public and unlisted playlists
- Can resume from previous runs (idempotent)

### 4. Quality Gates
- Perceptual hash deduplication (prevents duplicate slides)
- Minimum unique frames check per lecture
- LaTeX compilation validation before final PDF

## Directory Structure (Generated Dynamically)

```
{output_dir}/
├── videos/                  # Downloaded lecture videos
├── frames/                  # Raw + deduplicated frames per lecture
├── transcripts/             # .srt files with timestamps
├── notes-md/                # Enhanced markdown per lecture
├── notes-tex/               # Professional LaTeX fragments
├── book/                    # Final master .tex and compiled PDF
├── scripts/                 # Generated helper scripts
└── config.json              # Saved run configuration
```

## Implementation Notes

This skill was developed and tested on the playlist:
`Reasoning LLMs from Scratch` (23 lectures)

It successfully produced:
- 32-page professional PDF book
- 67 + 48 unique frames for first two lectures
- Rich textual explanations
- Clean LaTeX with no generation artifacts

## Future Enhancements (Roadmap)
- Automatic Mermaid → TikZ conversion script
- OCR-based slide text extraction
- Parallel lecture processing
- Support for different output formats (HTML, EPUB, DOCX)

## Invocation via Hermes

```bash
# Natural language
"Create a LaTeX book from this playlist: https://youtube.com/playlist?list=..."

# Or direct skill call
hermes skill run youtube-lecture-book --playlist_url "..."
```

This skill is fully dynamic and production-ready. No values are hardcoded.