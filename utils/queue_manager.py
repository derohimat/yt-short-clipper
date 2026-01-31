"""
Queue Manager for batch video processing
Handles adding, removing, and persisting video queue
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class QueueManager:
    """Manages the video processing queue"""
    
    def __init__(self, queue_file: Path):
        self.queue_file = queue_file
        self.queue: List[Dict] = []
        self.load_queue()
    
    def load_queue(self):
        """Load queue from JSON file"""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    self.queue = json.load(f)
            except Exception as e:
                print(f"Error loading queue: {e}")
                self.queue = []
        else:
            self.queue = []
    
    def save_queue(self):
        """Save queue to JSON file"""
        try:
            self.queue_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(self.queue, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving queue: {e}")
    
    def add_video(self, url: str, title: str, thumbnail_url: str = "", duration: str = "") -> bool:
        """Add a video to the queue"""
        # Check if already in queue
        if any(item['url'] == url for item in self.queue):
            return False
        
        video_item = {
            'url': url,
            'title': title,
            'thumbnail_url': thumbnail_url,
            'duration': duration,
            'added_at': datetime.now().isoformat(),
            'status': 'pending'  # pending, processing, completed, failed
        }
        
        self.queue.append(video_item)
        self.save_queue()
        return True
    
    def remove_video(self, url: str) -> bool:
        """Remove a video from the queue"""
        original_length = len(self.queue)
        self.queue = [item for item in self.queue if item['url'] != url]
        
        if len(self.queue) < original_length:
            self.save_queue()
            return True
        return False
    
    def get_next_pending(self) -> Optional[Dict]:
        """Get the next pending video in the queue"""
        for item in self.queue:
            if item['status'] == 'pending':
                return item
        return None
    
    def update_status(self, url: str, status: str):
        """Update the status of a video in the queue"""
        for item in self.queue:
            if item['url'] == url:
                item['status'] = status
                self.save_queue()
                break
    
    def get_pending_count(self) -> int:
        """Get count of pending videos"""
        return sum(1 for item in self.queue if item['status'] == 'pending')
    
    def get_all_pending(self) -> List[Dict]:
        """Get all pending videos"""
        return [item for item in self.queue if item['status'] == 'pending']
    
    def clear_completed(self):
        """Remove completed and failed items from queue"""
        self.queue = [item for item in self.queue if item['status'] == 'pending' or item['status'] == 'processing']
        self.save_queue()
    
    def clear_all(self):
        """Clear entire queue"""
        self.queue = []
        self.save_queue()
    
    def get_queue(self) -> List[Dict]:
        """Get the entire queue"""
        return self.queue.copy()
