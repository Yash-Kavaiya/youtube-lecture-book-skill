---
name: youtube-lecture-book
description: "End-to-end pipeline to create a professional LaTeX PDF book from a YouTube playlist of lectures. Includes frame extraction every 5s, perceptual deduplication, enhanced Markdown notes with Mermaid/TikZ, tables, code blocks, and master book compilation."
version: 1.0.0
author: Hermes Agent + Grok
license: MIT
tags: [youtube, latex, education, video-processing, book-generation]
---

# YouTube Lecture → Professional LaTeX Book Pipeline

## Goal
Convert an entire YouTube lecture playlist into a high-quality, double-enhanced LaTeX PDF book with:
- Unique relevant screenshots (frames every 5 seconds, perceptually deduplicated)
- Timestamped captions + full transcripts
- Rich textual explanations
- Mermaid diagrams converted to TikZ
- Tables, code blocks, tcolorbox notes
- One master PDF book containing all lectures as chapters

## Prerequisites
- yt-dlp
- ffmpeg
- Python with: pillow, imagehash, pytesseract (optional)
- LaTeX distribution (MiKTeX / TeX Live) with packages: tcolorbox, tikz, pgfplots, booktabs, listings, pdfpages, hyperref
- Optional: Claude Code for initial note generation

## Step-by-Step Workflow

### 1. Setup Project
```bash
mkdir -p reasoning-llms-book/{videos,frames,transcripts,notes-md,notes-tex,book,scripts}
cd reasoning-llms-book
```

### 2. Fetch Playlist Metadata
```bash
yt-dlp --flat-playlist --dump-json "PLAYLIST_URL" > data/playlist.json
```

### 3. Extract Frames (every 5 seconds)
Use `ffmpeg` or the provided `extract_frames.py`:
```bash
ffmpeg -i video.mp4 -vf "fps=1/5" -q:v 2 frames/XX/video/frame_%05d.jpg
```

### 4. Perceptual Deduplication
Run deduplication script (Hamming distance ≤ 8 on pHash/dHash):
- Keeps ~7–10% of raw frames as unique relevant images
- Generates `manifest.json` with timestamps

### 5. Generate Enhanced Notes
For each lecture create:
- `notes-md/XX_lecture.md` — timed transcript + embedded images + Mermaid + tables + code + rich explanations
- `notes-tex/XX_lecture.tex` — professional LaTeX fragment (no `\documentclass`)

### 6. Create Master Book
```latex
\documentclass{report}
...
\chapter{Lecture 1}
\includepdf{notes-tex/01_lecture1.pdf}   % or \input for fragments
...
```

Compile with `pdflatex` (run twice).

## Key Quality Rules (Hard Requirements)
**1. No timestamps in final PDF**  
Generation timestamps, frame numbers, or agent metadata must NEVER appear in the reader-facing PDF. They are only for internal processing. This is a non-negotiable final gate — always verify the compiled PDF before delivery.

**2. All images must be unique and pedagogically relevant**  
**3. Text explanations must be substantially expanded** beyond the raw transcript  
**4. Use tcolorbox for definitions, key ideas, warnings**  
**5. Convert Mermaid to native TikZ** for professional typesetting  
**6. Maintain consistent styling across all chapters**

## Mandatory Final Verification Step
Before handing over the PDF:
- Open the compiled book and search for any occurrence of “timestamp”, “t=”, “00:”, or frame numbers in visible text.
- If any appear, regenerate the affected chapter(s) without the metadata.

## Files Created in This Run
- `scripts/dedup_lecture2.py` — working deduplication example
- `book/main.tex` — clean master book template (uses `\includepdf`)
- `notes-tex/01_lecture1.pdf` — verified 23-page chapter

## Future Improvements
- Add OCR for slide text extraction
- Automatic Mermaid → TikZ conversion script
- Parallel processing for multiple lectures
- Support for different LaTeX themes (tufte, memoir, etc.)

This skill was developed while processing the "Reasoning LLMs from Scratch" playlist (PLPTV0NXA_ZSijcbUrRZHm6BrdinLuelPs).