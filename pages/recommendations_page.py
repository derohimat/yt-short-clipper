import customtkinter as ctk
import threading
from PIL import Image
from io import BytesIO
import requests
from utils.youtube_search import search_videos

class RecommendationsPage(ctk.CTkFrame):
    """Discovery page for finding viral video candidates"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.search_results = []
        self.thumbnails = {}  # Cache for PhotoImages
        
        self.create_ui()
        
    def create_ui(self):
        """Create page UI"""
        # Import footer
        from components.page_layout import PageFooter
        
        self.configure(fg_color=("#1a1a1a", "#0a0a0a"))
        
        # Header with back button
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        # Back button
        back_btn = ctk.CTkButton(header, text="← Back", width=80, height=35,
            font=ctk.CTkFont(size=13),
            fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40"),
            command=lambda: self.controller.show_page("home"))
        back_btn.pack(side="left", padx=(0, 15))
        
        # Title section
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(title_frame, text="Discovery", 
            font=ctk.CTkFont(size=28, weight="bold"), anchor="w").pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Find high-potential videos to clip", 
            font=ctk.CTkFont(size=14), text_color="gray", anchor="w").pack(anchor="w")
        
        
        # Search Section
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(search_frame, height=50, 
            placeholder_text="Search for podcasts, interviews, etc...",
            font=ctk.CTkFont(size=15))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.perform_search())
        
        self.search_btn = ctk.CTkButton(search_frame, text="Search", height=50, width=100,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.perform_search)
        self.search_btn.pack(side="left")
        
        # Categories / Chips
        chips_frame = ctk.CTkScrollableFrame(self, height=50, fg_color="transparent", orientation="horizontal")
        chips_frame.pack(fill="x", padx=25, pady=(0, 20))
        
        categories = [
            "Trending Podcasts", "Elon Musk", "Joe Rogan", "Lex Fridman", 
            "Business News", "Tech Reviews", "Gaming Funny Moments", 
            "Standup Comedy", "Motivational Speech"
        ]
        
        for cat in categories:
            btn = ctk.CTkButton(chips_frame, text=cat, height=32, 
                fg_color=("gray85", "gray20"), text_color=("black", "white"),
                hover_color=("gray70", "gray30"),
                command=lambda c=cat: self.search_category(c))
            btn.pack(side="left", padx=5)
            
        # Results Grid (Scrollable)
        self.results_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Initial State
        self.status_label = ctk.CTkLabel(self.results_scroll, 
            text="🔍 Type a search query or select a category to start",
            font=ctk.CTkFont(size=16), text_color="gray")
        self.status_label.pack(pady=50)
        
        # Footer
        footer = PageFooter(self, self.controller)
        footer.pack(fill="x", padx=30, pady=20)
        
    def search_category(self, category):
        """Search based on category click"""
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, category)
        self.perform_search()
        
    def perform_search(self):
        """Execute search logic"""
        query = self.search_entry.get().strip()
        if not query:
            return
            
        self.search_btn.configure(state="disabled", text="Searching...")
        self.status_label.configure(text="Searching YouTube...")
        
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        self.status_label = ctk.CTkLabel(self.results_scroll, text="Searching...", font=ctk.CTkFont(size=16))
        self.status_label.pack(pady=50)
        
        def run_search():
            results = search_videos(query, limit=20)
            self.after(0, lambda: self.display_results(results))
            
        threading.Thread(target=run_search, daemon=True).start()
        
    def display_results(self, results):
        """Render search results"""
        self.search_btn.configure(state="normal", text="Search")
        self.search_results = results
        
        # Clear loading status
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        if not results:
            ctk.CTkLabel(self.results_scroll, 
                text="❌ No results found. Try a different query.",
                font=ctk.CTkFont(size=16), text_color="gray").pack(pady=50)
            return
            
        # Grid layout configuration
        self.results_scroll.grid_columnconfigure(0, weight=1)
        self.results_scroll.grid_columnconfigure(1, weight=1)
        
        # Render cards
        row = 0
        col = 0
        
        for video in results:
            self.create_video_card(video, row, col)
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
                
    def create_video_card(self, video, row, col):
        """Create a UI card for a single video"""
        card = ctk.CTkFrame(self.results_scroll, fg_color=("gray90", "gray17"), corner_radius=15)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        # Thumbnail placeholder
        thumb_height = 180
        thumb_frame = ctk.CTkFrame(card, height=thumb_height, fg_color="#000000", corner_radius=10)
        thumb_frame.pack(fill="x", padx=0, pady=0)
        thumb_frame.pack_propagate(False) # Force height
        
        thumb_label = ctk.CTkLabel(thumb_frame, text="", image=None)
        thumb_label.pack(expand=True)
        
        # Load thumbnail async
        self.load_thumbnail(video["thumbnail"], thumb_label, card)
        
        # Video Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title
        title = video["title"]
        if len(title) > 60:
            title = title[:57] + "..."
            
        ctk.CTkLabel(info_frame, text=title, 
            font=ctk.CTkFont(size=14, weight="bold"), 
            wraplength=350, justify="left", anchor="w").pack(fill="x")
            
        # Meta (Views • Duration)
        meta_text = f"👁 {video.get('views', 'N/A')} • ⏱ {video.get('duration', 'N/A')}"
        ctk.CTkLabel(info_frame, text=meta_text, 
            font=ctk.CTkFont(size=12), text_color="gray", anchor="w").pack(fill="x", pady=(5, 15))
            
        # Action Button
        ctk.CTkButton(info_frame, text="➕ Add to Queue", height=40,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("#27ae60", "#229954"), hover_color=("#1e8449", "#1a7a3e"),
            command=lambda v=video: self.add_to_queue(v)).pack(fill="x")
            
    def load_thumbnail(self, url, label, card_ref):
        """Asynchronously load thumbnail image"""
        def load():
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    img_data = response.content
                    image = Image.open(BytesIO(img_data))
                    
                    # Resize while maintaining aspect ratio (cover)
                    # Target height 180, width dynamic based on card (approx 400)
                    image.thumbnail((400, 225), Image.Resampling.LANCZOS)
                    
                    self.after(0, lambda: self.show_thumbnail(image, label))
            except Exception as e:
                pass
                
        threading.Thread(target=load, daemon=True).start()
        
    def show_thumbnail(self, image, label):
        """Display loaded thumbnail"""
        try:
            ctk_img = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
            # Store reference to prevent garbage collection
            self.thumbnails[str(image)] = ctk_img 
            label.configure(image=ctk_img)
        except:
            pass

    def add_to_queue(self, video):
        """Add video to processing queue"""
        success = self.controller.queue_manager.add_video(
            url=video["url"],
            title=video["title"],
            thumbnail_url=video.get("thumbnail", ""),
            duration=video.get("duration", "")
        )
        
        if success:
            # Show success feedback
            self.after(0, lambda: self.show_queue_feedback(video["title"]))
        else:
            # Already in queue
            self.after(0, lambda: self.show_already_queued_feedback(video["title"]))
    
    def show_queue_feedback(self, title):
        """Show temporary success message"""
        # Refresh queue panel on home page
        if hasattr(self.controller, 'queue_panel'):
            self.controller.queue_panel.refresh_queue()
    
    
    def show_already_queued_feedback(self, title):
        """Show message that video is already queued"""
        pass
