#!/usr/bin/env python3
"""Simple perceptual dedup for Lecture 2 frames."""
import os
import json
import shutil
from pathlib import Path
from PIL import Image
import imagehash

SRC = Path("frames/02_fZNNqcN_UQM")
DST = Path("frames/02_deduped")
THRESHOLD = 8

def get_timestamp(i, interval=5):
    seconds = (i - 1) * interval
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

files = sorted([f for f in SRC.iterdir() if f.suffix == ".jpg"])
print(f"Found {len(files)} raw frames")

kept = []
manifest = []

for idx, f in enumerate(files, 1):
    try:
        img = Image.open(f)
        ph = str(imagehash.phash(img))
        dh = str(imagehash.dhash(img))
    except Exception:
        continue

    is_duplicate = False
    for k in kept:
        if imagehash.hex_to_hash(ph) - imagehash.hex_to_hash(k["phash"]) <= THRESHOLD:
            is_duplicate = True
            k.setdefault("represents", []).append(f.name)
            break

    if not is_duplicate:
        ts = get_timestamp(idx)
        entry = {
            "file": f"t{idx*5:05d}.jpg",
            "orig": f.name,
            "t": idx * 5,
            "ts": ts,
            "phash": ph,
            "dhash": dh,
            "represents": []
        }
        kept.append(entry)
        manifest.append(entry)

print(f"Kept {len(kept)} unique frames after deduplication")

if DST.exists():
    shutil.rmtree(DST)
DST.mkdir(parents=True)

for entry in manifest:
    src_file = SRC / entry["orig"]
    dst_file = DST / entry["file"]
    shutil.copy2(src_file, dst_file)

(DST / "manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest written with {len(manifest)} entries")
print("Done.")