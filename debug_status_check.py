
import sys
import os
import subprocess
from pathlib import Path

# Mock helpers to match app structure
def get_app_dir():
    return Path(os.getcwd())

def get_ffmpeg_path():
    ext = ".exe" if sys.platform == "win32" else ""
    
    # 1. Check in bundled/local ffmpeg directory
    local_path = get_app_dir() / "ffmpeg" / f"ffmpeg{ext}"
    print(f"Checking {local_path}: {local_path.exists()}")
    if local_path.exists():
        return str(local_path)
    
    # 2. Check in app dir directly (alternate bundle)
    alt_local = get_app_dir() / f"ffmpeg{ext}"
    print(f"Checking {alt_local}: {alt_local.exists()}")
    if alt_local.exists():
        return str(alt_local)
        
    # 3. Fallback to system PATH
    print("Fallback to system PATH 'ffmpeg'")
    return "ffmpeg"

def get_ytdlp_path():
    ext = ".exe" if sys.platform == "win32" else ""
    
    # 1. Check in local project directory
    local_path = get_app_dir() / f"yt-dlp{ext}"
    print(f"Checking {local_path}: {local_path.exists()}")
    if local_path.exists():
        return str(local_path)
        
    # 2. Fallback to system PATH
    print("Fallback to system PATH 'yt-dlp'")
    return "yt-dlp"

print("--- TESTING RESOLUTION ---")
ffmpeg_path = get_ffmpeg_path()
ytdlp_path = get_ytdlp_path()
print(f"Resolved FFmpeg: {ffmpeg_path}")
print(f"Resolved yt-dlp: {ytdlp_path}")

print("\n--- TESTING EXECUTION ---")
try:
    print(f"Executing: {ffmpeg_path} -version")
    result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)
    print(f"FFmpeg Return Code: {result.returncode}")
    print(f"FFmpeg Output: {result.stdout[:50]}...")
except Exception as e:
    print(f"FFmpeg Error: {e}")

try:
    print(f"Executing: {ytdlp_path} --version")
    result = subprocess.run([ytdlp_path, "--version"], capture_output=True, text=True)
    print(f"yt-dlp Return Code: {result.returncode}")
    print(f"yt-dlp Output: {result.stdout.strip()}")
except Exception as e:
    print(f"yt-dlp Error: {e}")
