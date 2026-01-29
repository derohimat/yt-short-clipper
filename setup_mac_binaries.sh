#!/bin/bash

# YT Short Clipper - Mac Binary Setup Script
# This script downloads ffmpeg and yt-dlp for macOS to be bundled with the app.

echo "🚀 Setting up binaries for macOS bundle..."

# Create ffmpeg directory
mkdir -p ffmpeg

# Download ffmpeg (static build for macOS)
if [ ! -f "ffmpeg/ffmpeg" ]; then
    echo "📥 Downloading FFmpeg for macOS..."
    # Using evermeet.cx (common source for mac static builds)
    curl -L https://evermeet.cx/ffmpeg/getrelease/ffmpeg/7z -o ffmpeg.7z
    # We need 7zip to extract it, or try to get the zip version
    # Actually, a better source might be a direct zip
    curl -L https://evermeet.cx/ffmpeg/getrelease/zip -o ffmpeg.zip
    unzip ffmpeg.zip -d ffmpeg
    rm ffmpeg.zip
    chmod +x ffmpeg/ffmpeg
else
    echo "✅ FFmpeg already exists."
fi

# Download yt-dlp
if [ ! -f "yt-dlp" ]; then
    echo "📥 Downloading yt-dlp..."
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o yt-dlp
    chmod +x yt-dlp
else
    echo "✅ yt-dlp already exists."
fi

echo "✨ Done! You can now run: pyinstaller macos_build.spec"
