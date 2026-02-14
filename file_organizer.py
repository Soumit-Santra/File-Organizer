# File Organizer
# Organizes any file type into folders based on date: Category/Year/Month_Year/Day_Month_Year structure
# Moves or copies files from source to organized destination folders
# Features: Copy/Move toggle, Undo log, Dry run preview, Watch folder, Cloud drive support, Hash duplicate detection
#**Created by Soumit Santra**  
# © 2026 File Organizer. All rights reserved.

import os
import shutil
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from PIL.ExifTags import TAGS
import threading
import json
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import platform


class FileOrganizerHandler(FileSystemEventHandler):
    # Handler for file system events in watch mode
    def __init__(self, organizer_gui):
        self.organizer_gui = organizer_gui
        self.processing = set()  # Track files being processed to avoid duplicates
        
    def on_created(self, event):
        if event.is_directory:
            return
        
        # Avoid processing the same file multiple times
        if event.src_path in self.processing:
            return
            
        self.processing.add(event.src_path)
        
        # Small delay to ensure file is fully written
        time.sleep(0.5)
        
        # Process the new file
        self.organizer_gui.process_single_file_watch(event.src_path)
        
        # Remove from processing set after a delay
        threading.Timer(2.0, lambda: self.processing.discard(event.src_path)).start()


class ImageOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer By Soumit Santra")
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set window size (50% of screen or minimum )
        window_width = max(900, int(screen_width * 0.5))
        window_height = max(700, int(screen_height * 0.5))
        
        # Center window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(900, 750)  # INCREASED from 700 to 750
        self.root.resizable(True, True)
        
        # Set color scheme
        self.bg_color = "#f5f5f5"
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.selected_files = []
        self.file_list = []
        self.is_organizing = False
        self.cancel_requested = False
        self.file_type_filter = tk.StringVar(value="All Files")
        
        # Feature variables
        self.operation_mode = tk.StringVar(value="move")
        self.dry_run_mode = tk.BooleanVar(value=False)
        self.organization_method = tk.StringVar(value="date")  # date, alphabetical, or size
        self.operation_log = []
        self.log_file = "file_organizer_undo_log.json"
        
        # Watch mode variables
        self.watch_mode = tk.BooleanVar(value=False)
        self.observer = None
        self.watch_thread = None
        
        # Duplicate detection variables
        self.detect_duplicates = tk.BooleanVar(value=False)
        self.file_hashes = {}  # Store hash: filepath mapping
        self.duplicate_action = tk.StringVar(value="skip")  # skip, rename, or delete
        
        # Cloud drive variables
        self.cloud_drive_path = tk.StringVar()
        self.sync_to_cloud = tk.BooleanVar(value=False)
        
        # File type categories
        self.file_categories = {
            'Images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.svg', '.raw', '.cr2', '.nef', '.ico'},
            'Videos': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.f4v'},
            'Audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.aiff', '.ape'},
            'Documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages', '.tex', '.wpd', '.md'},
            'Spreadsheets': {'.xls', '.xlsx', '.csv', '.ods', '.numbers', '.tsv'},
            'Presentations': {'.ppt', '.pptx', '.key', '.odp'},
            'Archives': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg'},
            'Code': {'.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.html', '.css', '.xml', '.json', '.yaml', '.yml'},
            'Executables': {'.exe', '.msi', '.app', '.deb', '.rpm', '.apk', '.dmg', '.pkg'},
            'Fonts': {'.ttf', '.otf', '.woff', '.woff2', '.eot'},
            'Database': {'.db', '.sqlite', '.sql', '.mdb', '.accdb'},
            'Other': set()
        }
        
        self.setup_ui()
        self.load_undo_log()
        
    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=15, pady=8)
        
        # Buttons frame with better layout - PACK FIRST to ensure always visible
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(side="bottom", pady=8, fill="x")
        
        # Main notebook for tabs with better styling - FIXED HEIGHT
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill="both", expand=False, pady=(0, 8))
        notebook.configure(height=450)  # INCREASED from 380 to 450 since we removed title
        
        # Configure notebook style
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[18, 8], font=('Segoe UI', 10, 'bold'))
        
        # Tab 1: Basic Options
        basic_tab = tk.Frame(notebook, bg="white")
        notebook.add(basic_tab, text="  Basic Options  ")
        
        # Tab 2: Advanced Options
        advanced_tab = tk.Frame(notebook, bg="white")
        notebook.add(advanced_tab, text="  Advanced Options  ")
        
        # ===== BASIC TAB =====
        self.setup_basic_tab(basic_tab)
        
        # ===== ADVANCED TAB =====
        self.setup_advanced_tab(advanced_tab)
        
        # Progress section (outside tabs) with better design
        progress_frame = tk.LabelFrame(
            main_container,
            text="  📊 Progress & Logs  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=8,
            height=160  # REDUCED from 180 to 160
        )
        progress_frame.pack(fill="x", expand=False, pady=(4, 4))  # REDUCED pady from 8 to 4
        progress_frame.pack_propagate(False)  # Prevent frame from shrinking to fit contents
        
        # Progress bar with better styling
        progress_container = tk.Frame(progress_frame, bg="white")
        progress_container.pack(fill="x", pady=(0, 4))
        
        self.progress_bar = ttk.Progressbar(
            progress_container, 
            mode='determinate', 
            length=400,
            style="custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=2)
        
        # Configure progress bar style
        style.configure("custom.Horizontal.TProgressbar", 
                       thickness=18,
                       troughcolor='#ecf0f1',
                       background='#3498db')
        
        # Status text area with better design
        text_frame = tk.Frame(progress_frame, bg="white")
        text_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.status_text = tk.Text(
            text_frame, 
            height=3,  # REDUCED to 3 lines for more compact display
            width=80,
            font=("Consolas", 9),
            bg="#fafafa",
            fg="#2c3e50",
            yscrollcommand=scrollbar.set,
            state="disabled",
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=4
        )
        self.status_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.status_text.yview)
        
        # Create inner frame to center buttons
        button_inner = tk.Frame(button_frame, bg=self.bg_color)
        button_inner.pack(expand=True)
        
        # Button style configuration
        button_config = {
            'font': ("Segoe UI", 10, "bold"),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 22,
            'pady': 10,
            'width': 13,
            'borderwidth': 0
        }
        
        # Organize button
        self.organize_btn = tk.Button(
            button_inner,
            text="Organize Files",
            command=self.start_organizing,
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            **button_config
        )
        self.organize_btn.pack(side="left", padx=4)
        
        # Cancel button
        self.cancel_btn = tk.Button(
            button_inner,
            text="Cancel",
            command=self.cancel_organizing,
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            disabledforeground="#ecf0f1",
            state="disabled",
            **button_config
        )
        self.cancel_btn.pack(side="left", padx=4)
        
        # Undo button
        self.undo_btn = tk.Button(
            button_inner,
            text="Undo Last",
            command=self.undo_last_operation,
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            activeforeground="white",
            **button_config
        )
        self.undo_btn.pack(side="left", padx=4)
        
        # Watch mode toggle button
        self.watch_btn = tk.Button(
            button_inner,
            text="Start Watching",
            command=self.toggle_watch_mode,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            **button_config
        )
        self.watch_btn.pack(side="left", padx=4)
        
        self.update_undo_button_state()
        
    def setup_basic_tab(self, parent):
        # Setup basic options tab
        parent.configure(bg="white")
        
        # Add padding container
        container = tk.Frame(parent, bg="white")
        container.pack(fill="both", expand=True, padx=18, pady=10)
        
        # Options frame with better styling
        options_frame = tk.LabelFrame(
            container,
            text="  ⚙️ Operation Mode  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        options_frame.pack(fill="x", pady=(0, 8))
        
        # Inner frame for better layout
        inner_frame = tk.Frame(options_frame, bg="white")
        inner_frame.pack(fill="x")
        
        # Copy/Move toggle with better design
        mode_frame = tk.Frame(inner_frame, bg="white")
        mode_frame.pack(side="left", padx=8)
        
        tk.Label(
            mode_frame,
            text="Action:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#34495e"
        ).pack(side="left", padx=(0, 8))
        
        tk.Radiobutton(
            mode_frame, 
            text="Move Files", 
            variable=self.operation_mode, 
            value="move",
            font=("Segoe UI", 9),
            bg="white",
            activebackground="white",
            selectcolor="#3498db"
        ).pack(side="left", padx=4)
        
        tk.Radiobutton(
            mode_frame, 
            text="Copy Files", 
            variable=self.operation_mode, 
            value="copy",
            font=("Segoe UI", 9),
            bg="white",
            activebackground="white",
            selectcolor="#3498db"
        ).pack(side="left", padx=4)
        
        # Separator
        tk.Frame(inner_frame, width=2, bg="#ecf0f1").pack(side="left", fill="y", padx=15)
        
        # Dry run checkbox with better styling
        tk.Checkbutton(
            inner_frame,
            text="🔍 Dry Run (Preview only - no changes)",
            variable=self.dry_run_mode,
            font=("Segoe UI", 9),
            bg="white",
            activebackground="white",
            selectcolor="#9b59b6"
        ).pack(side="left", padx=8)
        
        # Organization method dropdown
        org_method_frame = tk.LabelFrame(
            container,
            text="  📋 Organization Method  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        org_method_frame.pack(fill="x", pady=(0, 8))
        
        org_method_inner = tk.Frame(org_method_frame, bg="white")
        org_method_inner.pack(fill="x")
        
        tk.Label(
            org_method_inner,
            text="Organize by:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#34495e"
        ).pack(side="left", padx=(0, 12))
        
        org_methods = ["Date", "Alphabetical", "File Size"]
        org_method_dropdown = ttk.Combobox(
            org_method_inner, 
            textvariable=self.organization_method,
            values=org_methods,
            state="readonly",
            width=20,
            font=("Segoe UI", 9),
            style='Custom.TCombobox'
        )
        org_method_dropdown.pack(side="left", padx=(0, 8))
        org_method_dropdown.set("Date")
        
        # Description based on selection
        self.org_method_desc = tk.Label(
            org_method_inner, 
            text="← Organize files into folders by date (Year/Month/Day)",
            font=("Segoe UI", 8, "italic"),
            fg="#7f8c8d",
            bg="white"
        )
        self.org_method_desc.pack(side="left", padx=4)
        
        # Update description when method changes
        def update_org_description(*args):
            method = self.organization_method.get()
            if method == "Date":
                self.org_method_desc.config(text="← Organize files into folders by date (Year/Month/Day)")
            elif method == "Alphabetical":
                self.org_method_desc.config(text="← Organize files alphabetically (A-Z folders)")
            elif method == "File Size":
                self.org_method_desc.config(text="← Organize files by size (Small/Medium/Large/Very Large)")
        
        self.organization_method.trace('w', update_org_description)
        
        # File type filter with better design
        filter_frame = tk.LabelFrame(
            container,
            text="  🗂️ File Type Filter  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        filter_frame.pack(fill="x", pady=(0, 8))
        
        filter_inner = tk.Frame(filter_frame, bg="white")
        filter_inner.pack(fill="x")
        
        filter_options = ["All Files"] + sorted(list(self.file_categories.keys()))
        
        # Style the combobox
        style = ttk.Style()
        style.configure('Custom.TCombobox', padding=4)
        
        filter_dropdown = ttk.Combobox(
            filter_inner, 
            textvariable=self.file_type_filter,
            values=filter_options,
            state="readonly",
            width=28,
            font=("Segoe UI", 9),
            style='Custom.TCombobox'
        )
        filter_dropdown.pack(side="left", padx=(0, 8))
        filter_dropdown.current(0)
        
        tk.Label(
            filter_inner, 
            text="← Choose to organize specific file types only",
            font=("Segoe UI", 8, "italic"),
            fg="#7f8c8d",
            bg="white"
        ).pack(side="left", padx=4)
        
        # Source folder selection with better design
        source_frame = tk.LabelFrame(
            container,
            text="  📥 Source Location  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        source_frame.pack(fill="x", pady=(0, 8))
        
        source_inner = tk.Frame(source_frame, bg="white")
        source_inner.pack(fill="x")
        
        source_entry = tk.Entry(
            source_inner,
            textvariable=self.source_folder,
            font=("Segoe UI", 9),
            relief="solid",
            borderwidth=1,
            width=48
        )
        source_entry.pack(side="left", padx=(0, 8), ipady=4)
        
        # Button style
        btn_style = {
            'font': ("Segoe UI", 9, "bold"),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 12,
            'pady': 6,
            'borderwidth': 0
        }
        
        tk.Button(
            source_inner,
            text="📁 Browse Folder",
            command=self.browse_source_folder,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            **btn_style
        ).pack(side="left", padx=2)
        
        tk.Button(
            source_inner,
            text="📄 Select Files",
            command=self.browse_source_files,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            **btn_style
        ).pack(side="left", padx=2)
        
        # Destination folder selection with better design
        dest_frame = tk.LabelFrame(
            container,
            text="  📤 Destination Folder  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        dest_frame.pack(fill="x", pady=(0, 8))
        
        dest_inner = tk.Frame(dest_frame, bg="white")
        dest_inner.pack(fill="x")
        
        dest_entry = tk.Entry(
            dest_inner,
            textvariable=self.dest_folder,
            font=("Segoe UI", 9),
            relief="solid",
            borderwidth=1,
            width=62
        )
        dest_entry.pack(side="left", padx=(0, 8), ipady=4)
        
        tk.Button(
            dest_inner,
            text="📁 Browse",
            command=self.browse_dest,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            **btn_style
        ).pack(side="left")
        
    def setup_advanced_tab(self, parent):
        # Setup advanced options tab
        parent.configure(bg="white")
        
        # Add padding container
        container = tk.Frame(parent, bg="white")
        container.pack(fill="both", expand=True, padx=18, pady=10)
        
        # Duplicate detection with better design
        dup_frame = tk.LabelFrame(
            container,
            text="  🔍 Duplicate Detection (Hash-based)  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        dup_frame.pack(fill="x", pady=(0, 8))
        
        tk.Checkbutton(
            dup_frame,
            text="Enable duplicate detection using SHA-256 hash comparison",
            variable=self.detect_duplicates,
            font=("Segoe UI", 9),
            bg="white",
            activebackground="white",
            selectcolor="#e74c3c"
        ).pack(anchor="w", padx=4, pady=(0, 8))
        
        action_frame = tk.Frame(dup_frame, bg="white")
        action_frame.pack(fill="x", padx=4)
        
        tk.Label(
            action_frame,
            text="When duplicate found:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#34495e"
        ).pack(side="left", padx=(0, 12))
        
        tk.Radiobutton(
            action_frame,
            text="⏭️ Skip",
            variable=self.duplicate_action,
            value="skip",
            font=("Segoe UI", 8),
            bg="white",
            activebackground="white",
            selectcolor="#95a5a6"
        ).pack(side="left", padx=6)
        
        tk.Radiobutton(
            action_frame,
            text="✏️ Rename",
            variable=self.duplicate_action,
            value="rename",
            font=("Segoe UI", 8),
            bg="white",
            activebackground="white",
            selectcolor="#f39c12"
        ).pack(side="left", padx=6)
        
        tk.Radiobutton(
            action_frame,
            text="🗑️ Delete source",
            variable=self.duplicate_action,
            value="delete",
            font=("Segoe UI", 8),
            bg="white",
            activebackground="white",
            selectcolor="#e74c3c"
        ).pack(side="left", padx=6)
        
        # Watch folder with better design
        watch_frame = tk.LabelFrame(
            container,
            text="  👁️ Real-time Watch Mode  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        watch_frame.pack(fill="x", pady=(0, 8))
        
        tk.Checkbutton(
            watch_frame,
            text="Enable watch mode (automatically organize new files in real-time)",
            variable=self.watch_mode,
            font=("Segoe UI", 9),
            bg="white",
            activebackground="white",
            selectcolor="#3498db"
        ).pack(anchor="w", padx=4, pady=(0, 4))
        
        info_frame = tk.Frame(watch_frame, bg="#e8f5e9", relief="solid", borderwidth=1)
        info_frame.pack(fill="x", padx=4, pady=4)
        
        tk.Label(
            info_frame,
            text="ℹ️ Info: Watch mode monitors your source folder and automatically organizes\n"
                 "any new files that are added. Perfect for Downloads folders!",
            font=("Segoe UI", 8),
            bg="#e8f5e9",
            fg="#2e7d32",
            justify="left"
        ).pack(padx=8, pady=6)
        
        # Cloud drive sync with better design
        cloud_frame = tk.LabelFrame(
            container,
            text="  ☁️ Cloud Drive Sync  ",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=8
        )
        cloud_frame.pack(fill="x", pady=(0, 8))
        
        tk.Checkbutton(
            cloud_frame,
            text="Sync organized files to cloud drive automatically",
            variable=self.sync_to_cloud,
            font=("Segoe UI", 9),
            bg="white",
            activebackground="white",
            selectcolor="#00bcd4"
        ).pack(anchor="w", padx=4, pady=(0, 8))
        
        cloud_path_frame = tk.Frame(cloud_frame, bg="white")
        cloud_path_frame.pack(fill="x", padx=4, pady=(0, 8))
        
        tk.Label(
            cloud_path_frame,
            text="Cloud path:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#34495e"
        ).pack(side="left", padx=(0, 8))
        
        cloud_entry = tk.Entry(
            cloud_path_frame,
            textvariable=self.cloud_drive_path,
            font=("Segoe UI", 9),
            relief="solid",
            borderwidth=1,
            width=48
        )
        cloud_entry.pack(side="left", padx=(0, 8), ipady=4)
        
        tk.Button(
            cloud_path_frame,
            text="📁 Browse",
            command=self.browse_cloud_drive,
            font=("Segoe UI", 9, "bold"),
            bg="#00bcd4",
            fg="white",
            activebackground="#0097a7",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            borderwidth=0
        ).pack(side="left")
        
        info_frame2 = tk.Frame(cloud_frame, bg="#e3f2fd", relief="solid", borderwidth=1)
        info_frame2.pack(fill="x", padx=4)
        
        tk.Label(
            info_frame2,
            text="💡 Supported: Google Drive, Dropbox, OneDrive, iCloud Drive\n"
                 "Make sure your cloud service is installed and syncing to your local filesystem.",
            font=("Segoe UI", 8),
            bg="#e3f2fd",
            fg="#1565c0",
            justify="left"
        ).pack(padx=8, pady=6)
        
    def browse_source_folder(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_folder.set(folder)
            self.selected_files = []
            
    def browse_source_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[
                ("All files", "*.*"),
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp *.heic"),
                ("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv"),
                ("Audio files", "*.mp3 *.wav *.flac *.aac *.ogg"),
                ("Documents", "*.pdf *.doc *.docx *.txt"),
                ("Archives", "*.zip *.rar *.7z *.tar *.gz")
            ]
        )
        if files:
            self.selected_files = list(files)
            self.source_folder.set(f"{len(files)} files selected")
            
    def browse_dest(self):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_folder.set(folder)
            
    def browse_cloud_drive(self):
        folder = filedialog.askdirectory(title="Select Cloud Drive Folder")
        if folder:
            self.cloud_drive_path.set(folder)
    
    def calculate_file_hash(self, file_path, algorithm='sha256'):
        # Calculate hash of file content
        hash_func = hashlib.new(algorithm)
        try:
            with open(file_path, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(8192), b''):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            self.log_message(f"Error calculating hash for {file_path}: {str(e)}")
            return None
    
    def check_duplicate(self, file_path):
        # Check if file is a duplicate based on hash
        if not self.detect_duplicates.get():
            return False, None
        
        file_hash = self.calculate_file_hash(file_path)
        if file_hash is None:
            return False, None
        
        if file_hash in self.file_hashes:
            return True, self.file_hashes[file_hash]
        
        return False, None
    
    def toggle_watch_mode(self):
        # Start or stop watch mode
        if self.observer is None:
            # Start watching
            self.start_watch_mode()
        else:
            # Stop watching
            self.stop_watch_mode()
    
    def start_watch_mode(self):
        # Start monitoring the source folder for new files
        source = self.source_folder.get()
        dest = self.dest_folder.get()
        
        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Please select a valid source folder to watch!")
            return
        
        if not dest:
            messagebox.showerror("Error", "Please select a destination folder!")
            return
        
        if self.selected_files:
            messagebox.showwarning("Warning", "Watch mode works with folders only.\nPlease select a source folder instead of individual files.")
            return
        
        try:
            self.observer = Observer()
            event_handler = FileOrganizerHandler(self)
            self.observer.schedule(event_handler, source, recursive=True)
            self.observer.start()
            
            self.watch_btn.config(text="⏹ Stop Watching", bg="#e74c3c", activebackground="#c0392b")
            self.organize_btn.config(state="disabled")
            self.log_message(f"👁️ Watch mode STARTED - Monitoring: {source}")
            self.log_message("Waiting for new files...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start watch mode:\n{str(e)}")
    
    def stop_watch_mode(self):
        # Stop monitoring the source folder
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            
            self.watch_btn.config(text="👁 Start Watching", bg="#3498db", activebackground="#2980b9")
            self.organize_btn.config(state="normal")
            self.log_message("👁️ Watch mode STOPPED")
    
    def process_single_file_watch(self, file_path):
        # Process a single file in watch mode
        try:
            if not os.path.exists(file_path):
                return
            
            # Check if file matches filter
            filter_type = self.file_type_filter.get()
            if filter_type != "All Files":
                filtered_extensions = self.file_categories.get(filter_type, set())
                if Path(file_path).suffix.lower() not in filtered_extensions:
                    return
            
            dest = self.dest_folder.get()
            operation = self.operation_mode.get()
            
            # Check for duplicates
            is_duplicate, existing_file = self.check_duplicate(file_path)
            if is_duplicate:
                action = self.duplicate_action.get()
                filename = os.path.basename(file_path)
                
                if action == "skip":
                    self.log_message(f"⚠️ Skipped duplicate: {filename} (matches {existing_file})")
                    return
                elif action == "delete":
                    os.remove(file_path)
                    self.log_message(f"🗑️ Deleted duplicate: {filename}")
                    return
                # If rename, continue with processing
            
            # Get file info and folder structure
            folder_structure = self.get_folder_structure(file_path)
            dest_path = os.path.join(dest, folder_structure)
            os.makedirs(dest_path, exist_ok=True)
            
            filename = os.path.basename(file_path)
            dest_file = os.path.join(dest_path, filename)
            
            # Handle duplicate filenames
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(dest_file):
                new_filename = f"{base_name}_{counter}{ext}"
                dest_file = os.path.join(dest_path, new_filename)
                counter += 1
            
            # Perform operation
            if operation == "move":
                shutil.move(file_path, dest_file)
                action_text = "Moved"
            else:
                shutil.copy2(file_path, dest_file)
                action_text = "Copied"
            
            # Store hash if duplicate detection is enabled
            if self.detect_duplicates.get():
                file_hash = self.calculate_file_hash(dest_file)
                if file_hash:
                    self.file_hashes[file_hash] = dest_file
            
            # Add to undo log
            self.add_to_undo_log(operation, file_path, dest_file)
            self.save_undo_log()
            
            self.log_message(f"✓ {action_text}: {filename} → {folder_structure}")
            
            # Sync to cloud if enabled
            if self.sync_to_cloud.get():
                self.sync_file_to_cloud(dest_file, folder_structure)
            
        except Exception as e:
            self.log_message(f"✗ Error processing {os.path.basename(file_path)}: {str(e)}")
    
    def sync_file_to_cloud(self, source_file, folder_structure):
        # Sync a file to cloud drive - creates same folder structure in cloud and copies file
        try:
            cloud_path = self.cloud_drive_path.get()
            if not cloud_path or not os.path.exists(cloud_path):
                return
            
            # Create same folder structure in cloud
            cloud_dest_path = os.path.join(cloud_path, folder_structure)
            os.makedirs(cloud_dest_path, exist_ok=True)
            
            filename = os.path.basename(source_file)
            cloud_dest_file = os.path.join(cloud_dest_path, filename)
            
            # Copy to cloud
            shutil.copy2(source_file, cloud_dest_file)
            self.log_message(f"☁️ Synced to cloud: {filename}")
            
        except Exception as e:
            self.log_message(f"⚠️ Cloud sync failed for {os.path.basename(source_file)}: {str(e)}")
    
    def cancel_organizing(self):
        # Cancel the ongoing organization process 
        self.cancel_requested = True
        self.log_message("\n⚠️ Cancellation requested... stopping after current file")
    
    def load_undo_log(self):
        # Load the undo log from file
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    self.operation_log = json.load(f)
        except Exception as e:
            self.operation_log = []
    
    def save_undo_log(self):
        # Save the undo log to file
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.operation_log, f, indent=2)
        except Exception as e:
            self.log_message(f"Warning: Could not save undo log: {str(e)}")
    
    def add_to_undo_log(self, operation_type, source, destination):
        # Add an operation to the undo log
        operation = {
            'type': operation_type,
            'source': source,
            'destination': destination,
            'timestamp': datetime.now().isoformat()
        }
        self.operation_log.append(operation)
    
    def update_undo_button_state(self):
        # Enable/disable undo button based on log
        if self.operation_log and not self.is_organizing:
            self.undo_btn.config(state="normal")
        else:
            self.undo_btn.config(state="disabled")
    
    def undo_last_operation(self):
        # Undo the last batch of operations
        if not self.operation_log:
            messagebox.showinfo("No Operations", "No operations to undo!")
            return
        
        result = messagebox.askyesno(
            "Confirm Undo",
            f"This will undo the last operation batch containing {len(self.operation_log)} operations.\n\n"
            "Do you want to continue?"
        )
        
        if not result:
            return
        
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, "end")
        self.status_text.config(state="disabled")
        
        self.log_message("Starting undo operation...")
        self.log_message("="*50)
        
        success_count = 0
        error_count = 0
        
        for operation in reversed(self.operation_log):
            try:
                dest = operation['destination']
                src = operation['source']
                op_type = operation['type']
                
                if op_type == 'move':
                    if os.path.exists(dest):
                        os.makedirs(os.path.dirname(src), exist_ok=True)
                        shutil.move(dest, src)
                        self.log_message(f"✓ Restored: {os.path.basename(dest)} → {src}")
                        success_count += 1
                    else:
                        self.log_message(f"✗ File not found: {dest}")
                        error_count += 1
                        
                elif op_type == 'copy':
                    if os.path.exists(dest):
                        os.remove(dest)
                        self.log_message(f"✓ Removed copy: {dest}")
                        success_count += 1
                    else:
                        self.log_message(f"✗ File not found: {dest}")
                        error_count += 1
                        
            except Exception as e:
                self.log_message(f"✗ Error undoing operation: {str(e)}")
                error_count += 1
        
        self.operation_log = []
        self.save_undo_log()
        self.update_undo_button_state()
        
        self.log_message("="*50)
        self.log_message(f"Undo complete!")
        self.log_message(f"Successfully restored: {success_count} files")
        if error_count > 0:
            self.log_message(f"Errors: {error_count}")
        
        messagebox.showinfo("Undo Complete", f"Successfully restored {success_count} files!\nErrors: {error_count}")
            
    def log_message(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.status_text.config(state="disabled")
        self.root.update_idletasks()
        
    def get_file_category(self, file_path):
        # Determine which category a file belongs to based on extension
        ext = Path(file_path).suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if ext in extensions:
                return category
        
        return 'Other'
    
    def get_file_date(self, file_path):
        # Extract date from file - tries metadata for images, falls back to modification date
        try:
            ext = Path(file_path).suffix.lower()
            
            if ext in self.file_categories['Images']:
                try:
                    image = Image.open(file_path)
                    exif_data = image._getexif()
                    
                    if exif_data:
                        for tag_id, value in exif_data.items():
                            tag = TAGS.get(tag_id, tag_id)
                            
                            if tag in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']:
                                try:
                                    date_obj = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                                    return date_obj
                                except ValueError:
                                    continue
                except:
                    pass
            
            mod_time = os.path.getmtime(file_path)
            return datetime.fromtimestamp(mod_time)
            
        except Exception as e:
            mod_time = os.path.getmtime(file_path)
            return datetime.fromtimestamp(mod_time)
    
    def get_alphabetical_folder(self, file_path):
        # Get alphabetical folder structure based on filename
        filename = os.path.basename(file_path)
        first_char = filename[0].upper()
        
        # Check if it's a letter
        if first_char.isalpha():
            return first_char
        elif first_char.isdigit():
            return "0-9"
        else:
            return "Special"
    
    def get_size_folder(self, file_path):
        # Get size-based folder structure
        try:
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
            
            if size_mb < 1:
                return "Small (< 1 MB)"
            elif size_mb < 10:
                return "Medium (1-10 MB)"
            elif size_mb < 100:
                return "Large (10-100 MB)"
            else:
                return "Very Large (> 100 MB)"
        except:
            return "Unknown Size"
    
    def get_folder_structure(self, file_path):
        # Get folder structure based on organization method and file category
        method = self.organization_method.get()
        category = self.get_file_category(file_path)
        
        if method == "Date":
            date_obj = self.get_file_date(file_path)
            year = str(date_obj.year)
            month_name = date_obj.strftime('%B')
            month_folder = f"{month_name}_{year}"
            day_folder = f"{date_obj.day:02d}_{month_name}_{year}"
            return os.path.join(category, year, month_folder, day_folder)
        
        elif method == "Alphabetical":
            alpha_folder = self.get_alphabetical_folder(file_path)
            return os.path.join(category, alpha_folder)
        
        elif method == "File Size":
            size_folder = self.get_size_folder(file_path)
            return os.path.join(category, size_folder)
        
        else:
            # Default to date
            date_obj = self.get_file_date(file_path)
            year = str(date_obj.year)
            month_name = date_obj.strftime('%B')
            month_folder = f"{month_name}_{year}"
            day_folder = f"{date_obj.day:02d}_{month_name}_{year}"
            return os.path.join(category, year, month_folder, day_folder)
    
    def organize_files(self):
        try:
            source = self.source_folder.get()
            dest = self.dest_folder.get()
            filter_type = self.file_type_filter.get()
            is_dry_run = self.dry_run_mode.get()
            operation = self.operation_mode.get()
            
            if not dest:
                messagebox.showerror("Error", "Please select a destination folder!")
                self.organize_btn.config(state="normal", text="▶ Organize Files")
                self.cancel_btn.config(state="disabled")
                self.is_organizing = False
                return
            
            if not is_dry_run:
                os.makedirs(dest, exist_ok=True)
            
            if not is_dry_run:
                self.operation_log = []
                self.file_hashes = {}  # Reset hash database
            
            mode_text = "DRY RUN - PREVIEW ONLY" if is_dry_run else f"{operation.upper()} MODE"
            self.log_message(f"Mode: {mode_text}")
            
            if self.detect_duplicates.get():
                self.log_message("Duplicate detection: ENABLED (SHA-256)")
            if self.sync_to_cloud.get():
                self.log_message(f"Cloud sync: ENABLED → {self.cloud_drive_path.get()}")
            
            self.log_message("="*50)
            
            all_files = []
            
            if self.selected_files:
                all_files = self.selected_files
                self.log_message(f"Processing {len(all_files)} selected files")
            elif source and os.path.exists(source):
                self.log_message(f"Scanning folder: {source}")
                
                for root, dirs, files in os.walk(source):
                    for file in files:
                        if not file.startswith('.'):
                            all_files.append(os.path.join(root, file))
            else:
                messagebox.showerror("Error", "Please select a source folder or files!")
                self.organize_btn.config(state="normal", text="▶ Organize Files")
                self.cancel_btn.config(state="disabled")
                self.is_organizing = False
                return
            
            if filter_type != "All Files":
                filtered_extensions = self.file_categories.get(filter_type, set())
                files_to_process = [
                    f for f in all_files 
                    if Path(f).suffix.lower() in filtered_extensions
                ]
                self.log_message(f"Filter: {filter_type} - Found {len(files_to_process)} matching files")
            else:
                files_to_process = all_files
                self.log_message(f"Processing all file types")
            
            if not files_to_process:
                messagebox.showwarning("No Files", f"No files found matching the selected filter: {filter_type}")
                self.log_message("No matching files found!")
                self.organize_btn.config(state="normal", text="▶ Organize Files")
                self.cancel_btn.config(state="disabled")
                self.is_organizing = False
                return
            
            self.log_message(f"Found {len(files_to_process)} files to organize")
            self.progress_bar['maximum'] = len(files_to_process)
            
            organized_count = 0
            error_count = 0
            duplicate_count = 0
            category_counts = {}
            
            for idx, file_path in enumerate(files_to_process):
                if self.cancel_requested:
                    self.log_message("\n❌ Organization cancelled by user")
                    break
                    
                try:
                    # Check for duplicates
                    is_duplicate, existing_file = self.check_duplicate(file_path)
                    if is_duplicate:
                        duplicate_count += 1
                        action = self.duplicate_action.get()
                        filename = os.path.basename(file_path)
                        
                        if action == "skip":
                            self.log_message(f"⚠️ Skipped duplicate: {filename}")
                            continue
                        elif action == "delete" and not is_dry_run:
                            os.remove(file_path)
                            self.log_message(f"🗑️ Deleted duplicate: {filename}")
                            continue
                        # If rename or dry run, continue with processing
                    
                    category = self.get_file_category(file_path)
                    category_counts[category] = category_counts.get(category, 0) + 1
                    
                    # Get folder structure based on organization method
                    folder_structure = self.get_folder_structure(file_path)
                    dest_path = os.path.join(dest, folder_structure)
                    
                    filename = os.path.basename(file_path)
                    dest_file = os.path.join(dest_path, filename)
                    
                    counter = 1
                    base_name, ext = os.path.splitext(filename)
                    while os.path.exists(dest_file):
                        new_filename = f"{base_name}_{counter}{ext}"
                        dest_file = os.path.join(dest_path, new_filename)
                        counter += 1
                    
                    if is_dry_run:
                        action = "Would move" if operation == "move" else "Would copy"
                        dup_suffix = " [DUPLICATE]" if is_duplicate else ""
                        self.log_message(f"🔍 {action}: {filename}{dup_suffix} → {folder_structure}")
                    else:
                        os.makedirs(dest_path, exist_ok=True)
                        
                        if operation == "move":
                            shutil.move(file_path, dest_file)
                            self.log_message(f"✓ Moved {filename} → {folder_structure}")
                        else:
                            shutil.copy2(file_path, dest_file)
                            self.log_message(f"✓ Copied {filename} → {folder_structure}")
                        
                        # Store hash
                        if self.detect_duplicates.get():
                            file_hash = self.calculate_file_hash(dest_file)
                            if file_hash:
                                self.file_hashes[file_hash] = dest_file
                        
                        self.add_to_undo_log(operation, file_path, dest_file)
                        
                        # Sync to cloud
                        if self.sync_to_cloud.get():
                            self.sync_file_to_cloud(dest_file, folder_structure)
                    
                    organized_count += 1
                    
                except Exception as e:
                    error_count += 1
                    self.log_message(f"✗ Error processing {os.path.basename(file_path)}: {str(e)}")
                
                self.progress_bar['value'] = idx + 1
                self.root.update_idletasks()
            
            # Summary
            self.log_message("\n" + "="*50)
            if self.cancel_requested:
                self.log_message(f"Operation cancelled!")
                self.log_message(f"Processed: {organized_count} files before cancellation")
            else:
                if is_dry_run:
                    self.log_message(f"DRY RUN PREVIEW COMPLETE!")
                    self.log_message(f"Would organize: {organized_count} files")
                    self.log_message(f"(No files were actually moved or copied)")
                else:
                    self.log_message(f"Organization complete!")
                    action = "moved" if operation == "move" else "copied"
                    self.log_message(f"Successfully {action}: {organized_count} files")
            
            if duplicate_count > 0:
                self.log_message(f"Duplicates found: {duplicate_count}")
            
            if category_counts:
                self.log_message("\nFiles by category:")
                for cat, count in sorted(category_counts.items()):
                    self.log_message(f"  • {cat}: {count} files")
            
            if error_count > 0:
                self.log_message(f"\nErrors: {error_count} files")
            self.log_message("="*50)
            
            if not is_dry_run and not self.cancel_requested:
                self.save_undo_log()
                self.update_undo_button_state()
            
            if not self.cancel_requested:
                summary_text = ""
                if is_dry_run:
                    summary_text = f"DRY RUN PREVIEW\n\nWould organize {organized_count} files\n"
                    summary_text += "(No files were actually moved or copied)\n\n"
                else:
                    action = "moved" if operation == "move" else "copied"
                    summary_text = f"Successfully {action} {organized_count} files!\n"
                    summary_text += f"Errors: {error_count}\n"
                
                if duplicate_count > 0:
                    summary_text += f"Duplicates: {duplicate_count}\n"
                
                summary_text += "\nCategory breakdown:\n"
                for cat, count in sorted(category_counts.items()):
                    summary_text += f"  {cat}: {count}\n"
                
                messagebox.showinfo("Complete", summary_text)
            
        except Exception as e:
            self.log_message(f"\n❌ Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
        
        finally:
            self.organize_btn.config(state="normal", text="▶ Organize Files")
            self.cancel_btn.config(state="disabled")
            self.is_organizing = False
            self.cancel_requested = False
            self.update_undo_button_state()
        
    def start_organizing(self):
        if self.is_organizing:
            return
            
        self.organize_btn.config(state="disabled", text="Organizing...")
        self.cancel_btn.config(state="normal")
        self.undo_btn.config(state="disabled")
        self.progress_bar['value'] = 0
        self.is_organizing = True
        self.cancel_requested = False
        
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, "end")
        self.status_text.config(state="disabled")
        
        thread = threading.Thread(target=self.organize_files)
        thread.daemon = True
        thread.start()


def main():
    root = tk.Tk()
    app = ImageOrganizerGUI(root)
    
    # Handle window close while watch mode is active
    def on_closing():
        if app.observer:
            app.stop_watch_mode()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()