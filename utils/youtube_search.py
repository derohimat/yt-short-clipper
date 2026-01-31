import json
import subprocess
from pathlib import Path
from utils.helpers import get_ytdlp_path

def search_videos(query: str, limit: int = 10) -> list:
    """
    Search YouTube videos using yt-dlp.
    Returns a list of dicts with title, url, thumbnail, views, duration.
    """
    ytdlp_path = get_ytdlp_path()
    
    # Construct command to get JSON dump of search results
    cmd = [
        ytdlp_path,
        f"ytsearch{limit}:{query}",
        "--dump-json",
        "--default-search", "ytsearch",
        "--no-playlist",
        "--no-check-certificate",
        "--geo-bypass",
        "--flat-playlist",  # Faster, but might miss some details
        "--skip-download"
    ]
    
    try:
        # Run command
        # Use shell=True only on Windows to avoid popup, but subprocess usually handles it
        # startupinfo = subprocess.STARTUPINFO()
        # startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if subprocess.os.name == 'nt' else 0
        )
        
        stdout, stderr = process.communicate()
        
        results = []
        for line in stdout.splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                
                # Extract relevant info
                video_id = data.get("id")
                url = f"https://www.youtube.com/watch?v={video_id}"
                title = data.get("title", "Unknown Title")
                thumbnail = data.get("thumbnail") or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
                duration = data.get("duration", 0)
                view_count = data.get("view_count", 0)
                uploader = data.get("uploader", "Unknown")
                
                # Format views
                if view_count:
                    if view_count >= 1000000:
                        views_text = f"{view_count/1000000:.1f}M views"
                    elif view_count >= 1000:
                        views_text = f"{view_count/1000:.1f}K views"
                    else:
                        views_text = f"{view_count} views"
                else:
                    views_text = "N/A"
                
                # Format duration
                if duration:
                    minutes = int(duration // 60)
                    seconds = int(duration % 60)
                    duration_text = f"{minutes}:{seconds:02d}"
                else:
                    duration_text = "N/A"
                
                results.append({
                    "title": title,
                    "url": url,
                    "thumbnail": thumbnail,
                    "views": views_text,
                    "duration": duration_text,
                    "uploader": uploader,
                    "id": video_id
                })
                
            except json.JSONDecodeError:
                continue
                
        return results
        
    except Exception as e:
        print(f"Error searching videos: {e}")
        return []
