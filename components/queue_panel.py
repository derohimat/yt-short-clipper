"""
Queue Panel Component
Displays queued videos on the home page
"""
import customtkinter as ctk
from tkinter import messagebox

class QueuePanel(ctk.CTkFrame):
    """Panel to display and manage queued videos"""
    
    def __init__(self, parent, queue_manager, on_process_queue, on_remove_item):
        super().__init__(parent, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=10)
        self.queue_manager = queue_manager
        self.on_process_queue = on_process_queue
        self.on_remove_item = on_remove_item
        
        self.create_ui()
        self.refresh_queue()
    
    def create_ui(self):
        """Create the queue panel UI"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(12, 8))
        
        ctk.CTkLabel(header_frame, text="📋 Processing Queue", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            anchor="w").pack(side="left", fill="x", expand=True)
        
        self.count_label = ctk.CTkLabel(header_frame, text="0 videos", 
            font=ctk.CTkFont(size=11), text_color="gray")
        self.count_label.pack(side="right")
        
        # Queue list container (scrollable)
        self.queue_container = ctk.CTkScrollableFrame(self, 
            fg_color="transparent", height=200)
        self.queue_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Action buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        self.process_btn = ctk.CTkButton(btn_frame, text="▶️ Process Queue", 
            height=40, font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#27ae60", "#229954"), hover_color=("#1e8449", "#1a7a3e"),
            command=self.on_process_clicked, state="disabled")
        self.process_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.clear_btn = ctk.CTkButton(btn_frame, text="🗑️ Clear", 
            height=40, width=80, font=ctk.CTkFont(size=12),
            fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40"),
            command=self.on_clear_clicked, state="disabled")
        self.clear_btn.pack(side="right")
    
    def refresh_queue(self):
        """Refresh the queue display"""
        # Clear existing items
        for widget in self.queue_container.winfo_children():
            widget.destroy()
        
        # Get pending videos
        pending_videos = self.queue_manager.get_all_pending()
        
        # Update count
        count = len(pending_videos)
        self.count_label.configure(text=f"{count} video{'s' if count != 1 else ''}")
        
        # Enable/disable buttons
        if count > 0:
            self.process_btn.configure(state="normal")
            self.clear_btn.configure(state="normal")
        else:
            self.process_btn.configure(state="disabled")
            self.clear_btn.configure(state="disabled")
        
        # Display videos
        if count == 0:
            # Empty state
            empty_label = ctk.CTkLabel(self.queue_container, 
                text="No videos in queue\nAdd videos from Discovery page",
                font=ctk.CTkFont(size=12), text_color="gray", justify="center")
            empty_label.pack(pady=40)
        else:
            for video in pending_videos:
                self.create_queue_item(video)
    
    def create_queue_item(self, video):
        """Create a single queue item"""
        item_frame = ctk.CTkFrame(self.queue_container, 
            fg_color=("#3a3a3a", "#2a2a2a"), corner_radius=8)
        item_frame.pack(fill="x", pady=3)
        
        # Content frame
        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="x", padx=10, pady=8)
        
        # Title
        title = video["title"]
        if len(title) > 50:
            title = title[:47] + "..."
        
        ctk.CTkLabel(content, text=title, 
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w").pack(side="left", fill="x", expand=True)
        
        # Duration (if available)
        if video.get("duration"):
            ctk.CTkLabel(content, text=f"⏱ {video['duration']}", 
                font=ctk.CTkFont(size=10), text_color="gray").pack(side="left", padx=(5, 10))
        
        # Remove button
        remove_btn = ctk.CTkButton(content, text="✕", width=30, height=25,
            fg_color=("gray70", "gray30"), hover_color=("#e74c3c", "#c0392b"),
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda v=video: self.remove_item(v))
        remove_btn.pack(side="right")
    
    def remove_item(self, video):
        """Remove an item from the queue"""
        self.queue_manager.remove_video(video["url"])
        self.on_remove_item(video)
        self.refresh_queue()
    
    def on_process_clicked(self):
        """Handle process queue button click"""
        count = self.queue_manager.get_pending_count()
        if count > 0:
            response = messagebox.askyesno(
                "Process Queue",
                f"Process {count} video{'s' if count != 1 else ''} in queue?\n\n"
                "Videos will be processed one at a time."
            )
            if response:
                self.on_process_queue()
    
    def on_clear_clicked(self):
        """Handle clear queue button click"""
        count = self.queue_manager.get_pending_count()
        if count > 0:
            response = messagebox.askyesno(
                "Clear Queue",
                f"Remove all {count} video{'s' if count != 1 else ''} from queue?"
            )
            if response:
                self.queue_manager.clear_all()
                self.refresh_queue()
