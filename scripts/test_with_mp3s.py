"""Test script: process MP3 files through the Gemini pipeline.

Usage:
  python scripts/test_with_mp3s.py

Requirements:
- `pydub` Python package
- `ffmpeg` binary available on PATH (pydub requires ffmpeg for mp3)
- Proper `.env` with Google credentials for Gemini/TTS

This script will:
- Find any `*.mp3` files in the repo root or `backend/` folders
- Convert to 8kHz mono 16-bit PCM
- Convert to mu-law and call `process_voice_turn`
- Print transcript and AI text
- Save AI reply audio (if any) to `output_ai/<original>.reply.wav`
"""

import os
import glob
import sys
import wave
import logging

import imageio_ffmpeg as iio_ffmpeg
import subprocess

import numpy as np

# Ensure repo root is on sys.path so we can import the backend package
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Import project pipeline
try:
    from backend.src.mulaw_converter import linear_to_mulaw
    from backend.src.google_gemini import process_voice_turn
except Exception as e:
    print("Failed to import project modules:", e)
    print("Make sure you're running this from the repo root and the backend package is available.")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_with_mp3s")

SEARCH_PATHS = [".", "backend", "backend/src"]

candidates = []
for p in SEARCH_PATHS:
    candidates += glob.glob(os.path.join(p, "*.mp3"))

if not candidates:
    print("No mp3 files found in repo root or backend folders. Place your files in the repo root or backend/.")
    sys.exit(0)

out_dir = "output_ai"
os.makedirs(out_dir, exist_ok=True)

for filepath in candidates:
    print("Processing:", filepath)
    pcm = None
    if pcm is None:
        # Fallback: use imageio-ffmpeg's bundled ffmpeg to produce s16le PCM
        try:
            ffmpeg_exe = iio_ffmpeg.get_ffmpeg_exe()
            cmd = [
                ffmpeg_exe,
                "-nostdin",
                "-i",
                filepath,
                "-f",
                "s16le",
                "-acodec",
                "pcm_s16le",
                "-ac",
                "1",
                "-ar",
                "8000",
                "-"
            ]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                print("ffmpeg failed:", err.decode(errors='replace'))
                continue
            pcm = np.frombuffer(out, dtype=np.int16)
        except Exception as e:
            print("FFmpeg fallback failed:", e)
            continue

    # Convert to mu-law bytes
    try:
        mulaw_bytes = linear_to_mulaw(pcm)
    except Exception as e:
        print("Error converting to mu-law:", e)
        continue

    # Call the pipeline
    try:
        result = process_voice_turn(mulaw_bytes, context={"name": "TestUser"}) or {}
    except Exception as e:
        logger.exception("process_voice_turn raised")
        result = {}

    print("Transcript:", result.get("transcript"))
    print("AI text:", result.get("ai_text"))

    linear_audio = result.get("linear_audio")
    if linear_audio is not None and isinstance(linear_audio, np.ndarray) and linear_audio.size > 0:
        outname = os.path.basename(filepath) + ".reply.wav"
        outpath = os.path.join(out_dir, outname)
        try:
            with wave.open(outpath, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(8000)
                wf.writeframes(linear_audio.tobytes())
            print("Wrote AI reply to", outpath)
        except Exception as e:
            print("Failed to write reply mp3:", e)
    else:
        print("No reply audio generated for", filepath)

print("Done.")
