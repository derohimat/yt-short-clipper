"""
History manager for YT Short Clipper
"""

import json
from pathlib import Path
from datetime import datetime

class HistoryManager:
    """Manages application process history"""
    
    def __init__(self, history_file: Path):
        self.history_file = history_file
        self.history = self.load()
    
    def load(self):
        """Load history from file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save(self):
        """Save history to file"""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)
    
    def add_entry(self, url, title=None, status="processing", options=None):
        """Add or update a history entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = {
            "url": url,
            "title": title or "YouTube Video",
            "timestamp": timestamp,
            "status": status,
            "options": options or {}
        }
        
        # Insert at the beginning
        self.history.insert(0, entry)
        
        # Limit to 50 entries
        self.history = self.history[:50]
        self.save()
        return entry

    def update_status(self, url, status, title=None):
        """Update the status of the most recent entry for a URL"""
        for entry in self.history:
            if entry["url"] == url:
                entry["status"] = status
                if title:
                    entry["title"] = title
                self.save()
                break

    def get_history(self, status_filter=None):
        """Get history, optionally filtered by status"""
        if status_filter:
            return [e for e in self.history if e["status"] == status_filter]
        return self.history
