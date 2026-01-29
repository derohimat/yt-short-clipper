"""
History list component for Home Page
"""

import customtkinter as ctk

class HistoryList(ctk.CTkFrame):
    def __init__(self, parent, history_manager, on_resume_callback):
        super().__init__(parent, fg_color="transparent")
        self.history_manager = history_manager
        self.on_resume = on_resume_callback
        
        # Section Header
        self.header_label = ctk.CTkLabel(self, text="History", 
                                        font=ctk.CTkFont(size=13, weight="bold"), 
                                        anchor="w")
        self.header_label.pack(fill="x", pady=(20, 5))
        
        # Filter row (Mockup style: Success | Failed)
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 10))
        
        self.filter_all = ctk.CTkLabel(filter_frame, text="All", 
                                      font=ctk.CTkFont(size=11), text_color=("#3B8ED0", "#1F6AA5"), 
                                      cursor="hand2")
        self.filter_all.pack(side="left")
        self.filter_all.bind("<Button-1>", lambda e: self.set_filter("All"))
        
        ctk.CTkLabel(filter_frame, text=" | ", font=ctk.CTkFont(size=11), text_color="gray").pack(side="left")
        
        self.filter_success = ctk.CTkLabel(filter_frame, text="Success", 
                                          font=ctk.CTkFont(size=11), text_color="gray", 
                                          cursor="hand2")
        self.filter_success.pack(side="left")
        self.filter_success.bind("<Button-1>", lambda e: self.set_filter("Success"))
        
        ctk.CTkLabel(filter_frame, text=" | ", font=ctk.CTkFont(size=11), text_color="gray").pack(side="left")
        
        self.filter_failed = ctk.CTkLabel(filter_frame, text="Failed", 
                                         font=ctk.CTkFont(size=11), text_color="gray", 
                                         cursor="hand2")
        self.filter_failed.pack(side="left")
        self.filter_failed.bind("<Button-1>", lambda e: self.set_filter("Failed"))
        
        self.current_filter = "All"
        
        # Scrollable area for history items
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent", 
                                                  scrollbar_button_color=("#3a3a3a", "#2a2a2a"),
                                                  scrollbar_button_hover_color=("#4a4a4a", "#3a3a3a"))
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.refresh()

    def set_filter(self, val):
        self.current_filter = val
        
        # Update colors
        self.filter_all.configure(text_color=("#3B8ED0", "#1F6AA5") if val == "All" else "gray")
        self.filter_success.configure(text_color=("#3B8ED0", "#1F6AA5") if val == "Success" else "gray")
        self.filter_failed.configure(text_color=("#3B8ED0", "#1F6AA5") if val == "Failed" else "gray")
        
        self.refresh()

    def refresh(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        history = self.history_manager.get_history()
        
        if self.current_filter == "Success":
            filtered = [e for e in history if e["status"] == "success"]
        elif self.current_filter == "Failed":
            filtered = [e for e in history if e["status"] == "failed"]
        else:
            filtered = history
            
        if not filtered:
            msg = "No history found" if self.current_filter == "All" else f"No {self.current_filter.lower()} history"
            ctk.CTkLabel(self.scroll_frame, text=msg, 
                         font=ctk.CTkFont(size=11), text_color="gray").pack(pady=20)
            return
            
        for entry in filtered:
            # Build item card
            status = entry.get("status", "processing")
            
            item = ctk.CTkFrame(self.scroll_frame, fg_color=("#2b2b2b", "#161616"), corner_radius=8)
            item.pack(fill="x", pady=4, padx=2)
            
            # Status Border color
            if status == "success":
                border_color = "#27ae60"
                status_icon = "✅"
            elif status == "failed":
                border_color = "#e74c3c"
                status_icon = "❌"
            elif status == "cancelled":
                border_color = "#f39c12"
                status_icon = "⚠️"
            else:
                border_color = "#3B8ED0"
                status_icon = "⏳"
            
            # Sidebar indicator
            indicator = ctk.CTkFrame(item, width=4, fg_color=border_color, corner_radius=0)
            indicator.pack(side="left", fill="y")
            
            content = ctk.CTkFrame(item, fg_color="transparent")
            content.pack(side="left", fill="both", expand=True, padx=8, pady=6)
            
            title = entry.get("title", "YouTube Video")
            if len(title) > 40: title = title[:37] + "..."
            
            title_lbl = ctk.CTkLabel(content, text=title, 
                                    font=ctk.CTkFont(size=11, weight="bold"), 
                                    anchor="w", justify="left")
            title_lbl.pack(fill="x")
            
            bottom_row = ctk.CTkFrame(content, fg_color="transparent")
            bottom_row.pack(fill="x")
            
            time_lbl = ctk.CTkLabel(bottom_row, text=f"{status_icon} {entry.get('timestamp', '')}", 
                                   font=ctk.CTkFont(size=10), text_color="gray", anchor="w")
            time_lbl.pack(side="left")
            
            # Action button
            if status != "success" and status != "processing":
                resume_btn = ctk.CTkButton(item, text="Resume", width=60, height=24, 
                                          font=ctk.CTkFont(size=10),
                                          fg_color=("#3a3a3a", "#2a2a2a"),
                                          hover_color=("#4a4a4a", "#3a3a3a"),
                                          command=lambda e=entry: self.on_resume(e))
                resume_btn.pack(side="right", padx=10)
            elif status == "success":
                # Maybe a "Re-run" button or "Open Folder"
                view_btn = ctk.CTkButton(item, text="Use URL", width=60, height=24, 
                                        font=ctk.CTkFont(size=10),
                                        fg_color=("#3a3a3a", "#2a2a2a"),
                                        hover_color=("#4a4a4a", "#3a3a3a"),
                                        command=lambda e=entry: self.on_resume(e))
                view_btn.pack(side="right", padx=10)
