
import os
import sys
import zipfile
import urllib.request
import shutil
from pathlib import Path

# URLs
YTDLP_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
FFMPEG_ZIP_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

APP_DIR = Path(os.getcwd())
FFMPEG_DIR = APP_DIR / "ffmpeg"
FFMPEG_EXE = FFMPEG_DIR / "ffmpeg.exe"
YTDLP_EXE = APP_DIR / "yt-dlp.exe"

def report(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = (downloaded / total_size) * 100
        print(f"\rDownloading... {percent:.1f}%", end="")
    else:
        print(f"\rDownloading... {downloaded} bytes", end="")

def install_ytdlp():
    print(f"\nDownloading yt-dlp from {YTDLP_URL}...")
    try:
        urllib.request.urlretrieve(YTDLP_URL, YTDLP_EXE, reporthook=report)
        print("\n✅ yt-dlp downloaded successfully!")
    except Exception as e:
        print(f"\n❌ Failed to download yt-dlp: {e}")

def install_ffmpeg():
    print(f"\nDownloading ffmpeg from {FFMPEG_ZIP_URL}...")
    zip_path = APP_DIR / "ffmpeg.zip"
    try:
        urllib.request.urlretrieve(FFMPEG_ZIP_URL, zip_path, reporthook=report)
        print("\nExtracting FFmpeg...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Find the bin/ffmpeg.exe path in the zip
            ffmpeg_src = None
            for name in zip_ref.namelist():
                if name.endswith("bin/ffmpeg.exe"):
                    ffmpeg_src = name
                    break
            
            if ffmpeg_src:
                # Extract specifically to temp then move
                zip_ref.extract(ffmpeg_src, path=APP_DIR)
                
                # Move to final location
                extracted_path = APP_DIR / ffmpeg_src
                FFMPEG_DIR.mkdir(exist_ok=True)
                
                # Move
                shutil.move(str(extracted_path), str(FFMPEG_EXE))
                print(f"✅ FFmpeg installed to {FFMPEG_EXE}")
                
                # Cleanup extracted folder
                top_dir = APP_DIR / ffmpeg_src.split('/')[0]
                if top_dir.exists() and top_dir != APP_DIR:
                    shutil.rmtree(top_dir)
            else:
                 print("❌ Could not find bin/ffmpeg.exe in zip")
        
        # Cleanup zip
        if zip_path.exists():
            os.remove(zip_path)
            
    except Exception as e:
        print(f"\n❌ Failed to download/install ffmpeg: {e}")

if __name__ == "__main__":
    if not YTDLP_EXE.exists():
        install_ytdlp()
    else:
        print(f"yt-dlp already exists at {YTDLP_EXE}")
        
    if not FFMPEG_EXE.exists():
        install_ffmpeg()
    else:
        print(f"ffmpeg already exists at {FFMPEG_EXE}")

    print("\nDone!")
