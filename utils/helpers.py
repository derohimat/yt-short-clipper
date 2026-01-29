"""
Helper utility functions for YT Short Clipper
"""

import sys
import re
from pathlib import Path


import os

def get_app_dir():
    """Get executable/application directory (where binaries are)"""
    if getattr(sys, 'frozen', False):
        if sys.platform == 'darwin':
            # On macOS, sys.executable is inside the .app bundle
            return Path(sys.executable).parent
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


def get_data_dir():
    """Get persistent data directory (for config, logs, etc.)"""
    if sys.platform == 'win32':
        data_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'YTShortClipper'
    elif sys.platform == 'darwin':
        data_dir = Path.home() / 'Library' / 'Application Support' / 'YTShortClipper'
    else:
        data_dir = Path.home() / '.config' / 'yt-short-clipper'
    
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_bundle_dir():
    """Get bundled resources directory"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else get_app_dir()
    return get_app_dir()


def get_ffmpeg_path():
    """Get FFmpeg executable path"""
    ext = ".exe" if sys.platform == "win32" else ""
    
    # 1. Check in bundled/local ffmpeg directory
    local_path = get_app_dir() / "ffmpeg" / f"ffmpeg{ext}"
    if local_path.exists():
        return str(local_path)
    
    # 2. Check in app dir directly (alternate bundle)
    alt_local = get_app_dir() / f"ffmpeg{ext}"
    if alt_local.exists():
        return str(alt_local)
        
    # 3. Fallback to system PATH
    return "ffmpeg"


def get_ytdlp_path():
    """Get yt-dlp executable path"""
    ext = ".exe" if sys.platform == "win32" else ""
    
    # 1. Check in local project directory
    local_path = get_app_dir() / f"yt-dlp{ext}"
    if local_path.exists():
        return str(local_path)
        
    # 2. Fallback to system PATH
    return "yt-dlp"


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
