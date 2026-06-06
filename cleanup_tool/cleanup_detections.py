#!/usr/bin/env python3
"""
CC Camera Analytics - Cleanup Tool
Deletes recorded videos, captured images, and logs based on time frames
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Optional

class CleanupTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CC Camera Analytics - Cleanup Tool")
        self.root.geometry("700x700")
        self.root.resizable(True, True)
        
        # Get parent directory (cc_camera_analytics)
        self.parent_dir = Path(__file__).parent.parent
        self.detections_dir = self.parent_dir / "detections"
        self.images_dir = self.detections_dir / "images"
        self.videos_dir = self.detections_dir / "videos"
        self.logs_dir = self.detections_dir / "logs"
        
        # Statistics
        self.stats = {
            'images': {'count': 0, 'size': 0, 'files': []},
            'videos': {'count': 0, 'size': 0, 'files': []},
            'logs': {'count': 0, 'size': 0, 'files': []}
        }
        
        self.setup_ui()
        self.scan_files()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🗑️ Cleanup Tool", 
                              font=("Arial", 18, "bold"), 
                              bg="#2c3e50", fg="white")
        title_label.pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Time frame selection
        time_frame = tk.LabelFrame(content_frame, text="Select Time Frame", 
                                   font=("Arial", 11, "bold"), padx=15, pady=15)
        time_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.time_option = tk.StringVar(value="older_than_7_days")
        
        options = [
            ("Older than 1 day", "older_than_1_day"),
            ("Older than 3 days", "older_than_3_days"),
            ("Older than 7 days", "older_than_7_days"),
            ("Older than 30 days", "older_than_30_days"),
            ("All files", "all_files"),
            ("Custom date range", "custom_range")
        ]
        
        for text, value in options:
            rb = tk.Radiobutton(time_frame, text=text, variable=self.time_option, 
                               value=value, font=("Arial", 10),
                               command=self.on_time_option_change)
            rb.pack(anchor=tk.W, pady=2)
        
        # Custom date range frame (initially hidden)
        self.custom_frame = tk.Frame(time_frame)
        
        tk.Label(self.custom_frame, text="From:", font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        self.from_date = tk.Entry(self.custom_frame, width=12, font=("Arial", 9))
        self.from_date.insert(0, (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
        self.from_date.grid(row=0, column=1, padx=5)
        
        tk.Label(self.custom_frame, text="To:", font=("Arial", 9)).grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.to_date = tk.Entry(self.custom_frame, width=12, font=("Arial", 9))
        self.to_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.to_date.grid(row=0, column=3, padx=5)
        
        tk.Label(self.custom_frame, text="(YYYY-MM-DD)", 
                font=("Arial", 8), fg="gray").grid(row=1, column=0, columnspan=4, pady=(2, 0))
        
        # File type selection
        type_frame = tk.LabelFrame(content_frame, text="Select File Types", 
                                   font=("Arial", 11, "bold"), padx=15, pady=15)
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.delete_images = tk.BooleanVar(value=True)
        self.delete_videos = tk.BooleanVar(value=True)
        self.delete_logs = tk.BooleanVar(value=True)
        
        tk.Checkbutton(type_frame, text="Detection Images (.jpg)", 
                      variable=self.delete_images, font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        tk.Checkbutton(type_frame, text="Recorded Videos (.mp4/.avi)",
                      variable=self.delete_videos, font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        tk.Checkbutton(type_frame, text="Detection Logs (.json)", 
                      variable=self.delete_logs, font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        
        # Statistics frame
        stats_frame = tk.LabelFrame(content_frame, text="Current Statistics",
                                    font=("Arial", 11, "bold"), padx=15, pady=15)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.stats_text = tk.Text(stats_frame, height=6, font=("Courier", 9),
                                 bg="#f8f9fa", relief=tk.FLAT, wrap=tk.NONE)
        self.stats_text.pack(fill=tk.X)
        
        # Buttons frame
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        
        self.scan_btn = tk.Button(button_frame, text="🔍 Scan Files", 
                                  command=self.scan_files, font=("Arial", 10, "bold"),
                                  bg="#3498db", fg="white", padx=20, pady=8,
                                  cursor="hand2")
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_btn = tk.Button(button_frame, text="🗑️ Delete Selected", 
                                    command=self.delete_files, font=("Arial", 10, "bold"),
                                    bg="#e74c3c", fg="white", padx=20, pady=8,
                                    cursor="hand2")
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.close_btn = tk.Button(button_frame, text="✖ Close", 
                                   command=self.root.quit, font=("Arial", 10),
                                   bg="#95a5a6", fg="white", padx=20, pady=8,
                                   cursor="hand2")
        self.close_btn.pack(side=tk.RIGHT)
        
    def on_time_option_change(self):
        """Show/hide custom date range based on selection"""
        if self.time_option.get() == "custom_range":
            self.custom_frame.pack(pady=(10, 0))
        else:
            self.custom_frame.pack_forget()
    
    def get_time_filter(self) -> Tuple[Optional[datetime], Optional[datetime]]:
        """Get start and end datetime based on selected option"""
        now = datetime.now()
        option = self.time_option.get()
        
        if option == "older_than_1_day":
            return datetime.min, now - timedelta(days=1)
        elif option == "older_than_3_days":
            return datetime.min, now - timedelta(days=3)
        elif option == "older_than_7_days":
            return datetime.min, now - timedelta(days=7)
        elif option == "older_than_30_days":
            return datetime.min, now - timedelta(days=30)
        elif option == "all_files":
            return datetime.min, datetime.max
        elif option == "custom_range":
            try:
                from_date = datetime.strptime(self.from_date.get(), "%Y-%m-%d")
                to_date = datetime.strptime(self.to_date.get(), "%Y-%m-%d")
                to_date = to_date.replace(hour=23, minute=59, second=59)
                return from_date, to_date
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return None, None
        
        return datetime.min, datetime.max
    
    def parse_filename_date(self, filename: str) -> Optional[datetime]:
        """Extract datetime from filename (format: detection_YYYYMMDD_HHMMSS_microseconds.ext or recording_YYYYMMDD_HHMMSS.ext)"""
        try:
            # Remove extension and split
            parts = filename.replace('.jpg', '').replace('.mp4', '').replace('.avi', '').replace('.json', '').split('_')
            if len(parts) >= 3:
                date_str = parts[1]  # YYYYMMDD
                time_str = parts[2]  # HHMMSS
                
                year = int(date_str[0:4])
                month = int(date_str[4:6])
                day = int(date_str[6:8])
                hour = int(time_str[0:2])
                minute = int(time_str[2:4])
                second = int(time_str[4:6])
                
                return datetime(year, month, day, hour, minute, second)
        except (ValueError, IndexError):
            pass
        
        # Fallback to file modification time
        return None
    
    def get_file_date(self, filepath: Path) -> datetime:
        """Get file date from filename or modification time"""
        file_date = self.parse_filename_date(filepath.name)
        if file_date is None:
            # Use file modification time as fallback
            file_date = datetime.fromtimestamp(filepath.stat().st_mtime)
        return file_date
    
    def scan_files(self):
        """Scan and count files based on current filters"""
        start_date, end_date = self.get_time_filter()
        if start_date is None or end_date is None:
            return
        
        # Reset statistics
        self.stats = {
            'images': {'count': 0, 'size': 0, 'files': []},
            'videos': {'count': 0, 'size': 0, 'files': []},
            'logs': {'count': 0, 'size': 0, 'files': []}
        }
        
        # Check if detections directory exists
        if not self.detections_dir.exists():
            messagebox.showinfo("Info",
                f"Detections directory not found:\n{self.detections_dir}\n\n"
                "No files to scan. Run the camera analytics app first to generate detection files.")
            self.update_stats_display()
            return
        
        # Debug info
        debug_info = []
        
        # Scan images
        if self.delete_images.get():
            if self.images_dir.exists():
                img_files = list(self.images_dir.glob("*.jpg"))
                debug_info.append(f"Images dir: {len(img_files)} .jpg files found")
                for img_file in img_files:
                    file_date = self.get_file_date(img_file)
                    if file_date and start_date <= file_date <= end_date:
                        size = img_file.stat().st_size
                        self.stats['images']['count'] += 1
                        self.stats['images']['size'] += size
                        self.stats['images']['files'].append(img_file)
            else:
                debug_info.append(f"Images dir not found: {self.images_dir}")
        
        # Scan videos (both .mp4 and .avi formats)
        if self.delete_videos.get():
            if self.videos_dir.exists():
                mp4_files = list(self.videos_dir.glob("*.mp4"))
                avi_files = list(self.videos_dir.glob("*.avi"))
                vid_files = mp4_files + avi_files
                debug_info.append(f"Videos dir: {len(mp4_files)} .mp4 + {len(avi_files)} .avi files found")
                for vid_file in vid_files:
                    file_date = self.get_file_date(vid_file)
                    if file_date and start_date <= file_date <= end_date:
                        size = vid_file.stat().st_size
                        self.stats['videos']['count'] += 1
                        self.stats['videos']['size'] += size
                        self.stats['videos']['files'].append(vid_file)
            else:
                debug_info.append(f"Videos dir not found: {self.videos_dir}")
        
        # Scan logs
        if self.delete_logs.get():
            if self.logs_dir.exists():
                log_files = [f for f in self.logs_dir.glob("*.json") if f.name != "detections.json"]
                debug_info.append(f"Logs dir: {len(log_files)} .json files found (excluding detections.json)")
                for log_file in log_files:
                    file_date = self.get_file_date(log_file)
                    if file_date and start_date <= file_date <= end_date:
                        size = log_file.stat().st_size
                        self.stats['logs']['count'] += 1
                        self.stats['logs']['size'] += size
                        self.stats['logs']['files'].append(log_file)
            else:
                debug_info.append(f"Logs dir not found: {self.logs_dir}")
        
        # Show debug info if no files matched
        total_found = sum(s['count'] for s in self.stats.values())
        if total_found == 0 and debug_info:
            msg = "Scan complete but no files matched the criteria.\n\n"
            msg += "Debug Info:\n" + "\n".join(debug_info)
            msg += f"\n\nTime filter: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            messagebox.showinfo("Scan Results", msg)
        
        # Update display
        self.update_stats_display()
    
    def format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable size"""
        size = float(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def update_stats_display(self):
        """Update statistics text display"""
        self.stats_text.delete(1.0, tk.END)
        
        total_count = sum(s['count'] for s in self.stats.values())
        total_size = sum(s['size'] for s in self.stats.values())
        
        stats_str = f"""
╔══════════════════════════════════════════════════════╗
║  FILE TYPE          COUNT        SIZE                ║
╠══════════════════════════════════════════════════════╣
║  Detection Images   {self.stats['images']['count']:5d}        {self.format_size(self.stats['images']['size']):>12s}    ║
║  Recorded Videos    {self.stats['videos']['count']:5d}        {self.format_size(self.stats['videos']['size']):>12s}    ║
║  Detection Logs     {self.stats['logs']['count']:5d}        {self.format_size(self.stats['logs']['size']):>12s}    ║
╠══════════════════════════════════════════════════════╣
║  TOTAL              {total_count:5d}        {self.format_size(total_size):>12s}    ║
╚══════════════════════════════════════════════════════╝
"""
        self.stats_text.insert(1.0, stats_str)
        
        # Enable/disable delete button
        if total_count > 0:
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.delete_btn.config(state=tk.DISABLED)
    
    def delete_files(self):
        """Delete selected files after confirmation"""
        total_count = sum(s['count'] for s in self.stats.values())
        total_size = sum(s['size'] for s in self.stats.values())
        
        if total_count == 0:
            messagebox.showinfo("Info", "No files to delete based on current filters.")
            return
        
        # Confirmation dialog
        msg = f"Are you sure you want to delete:\n\n"
        msg += f"• {self.stats['images']['count']} detection images\n"
        msg += f"• {self.stats['videos']['count']} recorded videos\n"
        msg += f"• {self.stats['logs']['count']} log files\n\n"
        msg += f"Total: {total_count} files ({self.format_size(total_size)})\n\n"
        msg += "This action cannot be undone!"
        
        if not messagebox.askyesno("Confirm Deletion", msg, icon='warning'):
            return
        
        # Delete files
        deleted_count = 0
        errors = []
        
        for file_type in ['images', 'videos', 'logs']:
            files_list = self.stats[file_type].get('files', [])
            for filepath in files_list:
                try:
                    filepath.unlink()
                    deleted_count += 1
                except Exception as e:
                    errors.append(f"{filepath.name}: {str(e)}")
        
        # Show result
        if errors:
            error_msg = f"Deleted {deleted_count} files.\n\nErrors:\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... and {len(errors) - 10} more errors"
            messagebox.showwarning("Partial Success", error_msg)
        else:
            messagebox.showinfo("Success", f"Successfully deleted {deleted_count} files!")
        
        # Rescan
        self.scan_files()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CleanupTool()
    app.run()

# Made with Bob
