# 🗂️ File Organizer

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**Created by Soumit Santra**  
© 2026 File Organizer. All rights reserved.

---

## 🎯 Overview

**File Organizer** is a powerful, user-friendly desktop application that automatically organizes your files into structured folders based on multiple criteria. Whether you're dealing with thousands of photos, documents, videos, or any other file type, this tool saves you hours of manual work.

### 🎯 Perfect For:

- 📸 **Photographers** — Organize thousands of photos by date
- 💼 **Professionals** — Keep documents and files structured
- 🎬 **Content Creators** — Manage media files efficiently
- 🎓 **Students** — Organize study materials and assignments
- 🏠 **Home Users** — Clean up cluttered Downloads folders
- 💻 **Developers** — Keep project files and resources organized
- 🗄️ **Archivists** — Maintain large file collections

### Why File Organizer?

- 🚀 **Blazingly Fast** - Process thousands of files in seconds
- 🎨 **Beautiful GUI** - Modern, intuitive interface built with Tkinter
- 🔧 **Highly Customizable** - Multiple organization methods and filters
- 🔒 **Safe Operations** - Dry run mode and full undo support
- 👁️ **Real-time Monitoring** - Watch folders for automatic organization
- ☁️ **Cloud Integration** - Automatic sync to Google Drive, Dropbox, OneDrive, and more
- 🔍 **Smart Duplicate Detection** - SHA-256 hash-based duplicate handling

### 📸 Quick Preview

| Feature | Description |
|---------|-------------|
| 🗂️ **Smart Organization** | Organize by date, alphabet, or file size |
| ⚡ **Dual Mode** | Move or copy files with one click |
| 🔍 **Preview Mode** | Dry run to see changes before applying |
| 👁️ **Watch Mode** | Auto-organize new files in real-time |
| 🔄 **Undo Support** | Safely reverse operations |
| ☁️ **Cloud Sync** | Keep files synced across platforms |
| 🎯 **File Filters** | Process only specific file types |
| 🔐 **Duplicate Detection** | Smart hash-based duplicate handling |

---

## ✨ Features

### Core Features

- **🗂️ Multiple Organization Methods**
  - By Date (Year/Month/Day structure)
  - Alphabetically (A-Z folders)
  - By File Size (Small/Medium/Large/Very Large)

- **📁 Comprehensive File Type Support**
  - Images (JPG, PNG, GIF, BMP, TIFF, WebP, HEIC, SVG, RAW, CR2, NEF, ICO)
  - Videos (MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, MPG, MPEG, 3GP)
  - Audio (MP3, WAV, FLAC, AAC, OGG, WMA, M4A, OPUS, AIFF)
  - Documents (PDF, DOC, DOCX, TXT, RTF, ODT, Pages, TEX, WPD, MD)
  - Spreadsheets (XLS, XLSX, CSV, ODS, Numbers, TSV)
  - Presentations (PPT, PPTX, KEY, ODP)
  - Archives (ZIP, RAR, 7Z, TAR, GZ, BZ2, XZ, ISO, DMG)
  - Code files (PY, JS, Java, C++, C, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, HTML, CSS, XML, JSON, YAML)
  - Executables (EXE, MSI, APP, DEB, RPM, APK, DMG, PKG)
  - Fonts (TTF, OTF, WOFF, WOFF2, EOT)
  - Databases (DB, SQLite, SQL, MDB, ACCDB)

- **🎛️ Operation Modes**
  - Move files (relocate originals)
  - Copy files (keep originals intact)
  - Dry run mode (preview changes without executing)

- **📸 Smart Date Extraction**
  - EXIF metadata parsing for images
  - Fallback to file modification dates
  - Organized into Year/Month/Day folder structure

### Advanced Features

- **🔍 Duplicate Detection**
  - SHA-256 hash-based comparison
  - Multiple handling options: Skip, Rename, or Delete
  - Prevents wasting storage space

- **👁️ Watch Mode**
  - Real-time folder monitoring
  - Automatic organization of new files
  - Perfect for Downloads folders
  - Background processing with minimal resource usage

- **☁️ Cloud Drive Sync**
  - Automatic sync to cloud storage
  - Support for Google Drive, Dropbox, OneDrive, iCloud Drive
  - Maintains folder structure across platforms
  - Configurable sync paths

- **⏮️ Undo Functionality**
  - Complete operation logging
  - One-click undo of entire batches
  - JSON-based persistent log
  - Safe rollback of move operations

- **🎯 File Type Filtering**
  - Filter by specific categories
  - Process only selected file types
  - Reduce processing time for large folders

---

## 📦 Installation

### 🎯 Option 1: Download EXE (Easiest - Windows Only)

**✅ No Python installation required!**

1. **Download the latest release**
   - Go to [Releases](https://github.com/yourusername/universal-file-organizer/releases)
   - Download `FileOrganizer.exe` (or `FileOrganizer-v1.0.exe`)
   - File size: ~50-100 MB (includes Python and all dependencies)

2. **Run the application**
   - Double-click `FileOrganizer.exe` to launch
   - **Windows SmartScreen Warning**: If Windows Defender shows a warning:
     - Click "More info"
     - Click "Run anyway"
     - This is normal for new executables without a code signing certificate

3. **Optional: Create shortcuts**
   - **Desktop shortcut**: Right-click EXE → "Send to" → "Desktop (create shortcut)"
   - **Start Menu**: Right-click EXE → "Pin to Start"
   - **Taskbar**: Right-click EXE → "Pin to taskbar"

4. **First run**
   - The app may take 5-10 seconds to launch initially
   - Subsequent launches will be faster

> **💡 Tip**: Keep the EXE in a permanent location before creating shortcuts (e.g., `C:\Program Files\FileOrganizer\` or `C:\Tools\FileOrganizer\`)

> **🔒 Security Note**: The EXE is virus-free and safe. You can verify the file hash on the releases page or scan it with your antivirus software.

---

### 🐍 Option 2: Run from Source (All Platforms)

**For advanced users, developers, or non-Windows platforms (macOS, Linux)**

#### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

#### Platform-Specific Requirements

##### Windows
```bash
# Python usually includes tkinter by default
python --version  # Verify Python 3.8+
```

##### macOS
```bash
# Python usually includes tkinter by default
python3 --version  # Verify Python 3.8+
```

##### Linux (Ubuntu/Debian)
```bash
# Install Python and tkinter
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk
```

##### Linux (Fedora)
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

##### Linux (Arch)
```bash
sudo pacman -S python python-pip tk
```

#### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Soumit-Santra/File-Organizer.git
   cd File-Organizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python file_organizer.py
   ```

#### Alternative: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python file_organizer.py
```

---

### 🔨 Option 3: Build EXE Yourself (Advanced)

If you want to create your own executable from source:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the EXE (Windows)
pyinstaller --onefile --windowed --icon=icon.ico --name="FileOrganizer" file_organizer.py

# The EXE will be in the 'dist' folder
```

**Build options:**
- `--onefile`: Creates a single EXE file
- `--windowed`: Hides the console window (GUI only)
- `--icon=icon.ico`: Sets custom icon (optional)
- `--name`: Sets the output filename

---

## 🚀 Usage

### Basic Workflow

1. **Launch the Application**
   - **EXE users**: Double-click `FileOrganizer.exe`
   - **Source users**: Run `python file_organizer.py`

2. **Select Operation Mode**
   - Choose between "Move Files" or "Copy Files"
   - Enable "Dry Run" to preview changes without executing

3. **Choose Organization Method**
   - Date: Organize by Year/Month/Day
   - Alphabetical: Sort into A-Z folders
   - File Size: Group by size categories

4. **Set File Type Filter** (Optional)
   - Select "All Files" or specific category (Images, Videos, Documents, etc.)

5. **Select Source**
   - Click "Browse Folder" to organize an entire directory
   - Or click "Select Files" to organize specific files

6. **Select Destination**
   - Choose where organized files will be placed

7. **Click "Organize Files"**
   - Monitor progress in real-time
   - View detailed logs of all operations

### Advanced Usage

#### Using Watch Mode

1. Navigate to the "Advanced Options" tab
2. Enable "Enable watch mode"
3. Set your source and destination folders
4. Click "Start Watching"
5. Any new files added to the source folder will be automatically organized

#### Enabling Duplicate Detection

1. Go to "Advanced Options" tab
2. Check "Enable duplicate detection"
3. Choose action for duplicates:
   - **Skip**: Ignore duplicate files
   - **Rename**: Add suffix to duplicate filenames
   - **Delete source**: Remove duplicate source files

#### Cloud Drive Sync

1. Install your cloud drive desktop application
2. Ensure it's syncing to your local filesystem
3. In "Advanced Options", enable "Sync organized files to cloud drive"
4. Browse and select your cloud drive folder
5. Files will be automatically copied to cloud after organization

#### Undo Operations

- Click "Undo Last" button to reverse the most recent batch operation
- Only works for "Move" operations (copied files will be deleted)
- Undo log persists between sessions

---

## 📊 Organization Methods

### By Date (Default)

Files are organized into a hierarchical structure:
```
Destination/
├── Images/
│   ├── 2024/
│   │   ├── January_2024/
│   │   │   ├── 01_January_2024/
│   │   │   ├── 02_January_2024/
│   │   │   └── ...
│   │   ├── February_2024/
│   │   └── ...
│   └── 2023/
├── Videos/
└── Documents/
```

**Best for:** Photo libraries, archival storage, time-based organization

### Alphabetically

Files organized by first letter of filename:
```
Destination/
├── Images/
│   ├── A/
│   ├── B/
│   ├── C/
│   ├── 0-9/
│   └── Special/
├── Documents/
└── ...
```

**Best for:** Quick lookup, name-based organization

### By File Size

Files grouped by size categories:
```
Destination/
├── Images/
│   ├── Small (< 1 MB)/
│   ├── Medium (1-10 MB)/
│   ├── Large (10-100 MB)/
│   └── Very Large (> 100 MB)/
├── Videos/
└── ...
```

**Best for:** Storage optimization, finding large files

---

## 🎨 Screenshots

### Main Interface
The clean, modern interface makes file organization intuitive and straightforward.

### Advanced Options
Fine-tune your organization with duplicate detection, watch mode, and cloud sync.

### Real-time Progress
Monitor your file organization with live progress bars and detailed logging.

---

## 🔧 Configuration

### Undo Log Location

The undo log is stored as `file_organizer_undo_log.json` in the same directory as the script or EXE.

### Customizing File Categories

Edit the `file_categories` dictionary in `file_organizer.py` to add or modify file type categories:

```python
self.file_categories = {
    'Custom Category': {'.ext1', '.ext2', '.ext3'},
    # Add more categories as needed
}
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/Soumit-Santra/File-Organizer.git
cd universal-file-organizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies including dev tools
pip install -r requirements.txt

# Run the application
python file_organizer.py
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><strong>Q: Is this tool safe to use? Will it delete my files?</strong></summary>
<br>
A: Yes, it's completely safe! The tool has a dry run mode to preview changes, an undo feature for move operations, and extensive error handling. Your files are only moved or copied according to your settings.
</details>

<details>
<summary><strong>Q: Why does Windows show a security warning for the EXE?</strong></summary>
<br>
A: This is normal for new executables that don't have a Microsoft code signing certificate (which costs hundreds of dollars annually). The EXE is safe and virus-free. Click "More info" → "Run anyway" to proceed. You can also scan it with your antivirus software or build it yourself from source.
</details>

<details>
<summary><strong>Q: Can I organize files from multiple folders at once?</strong></summary>
<br>
A: Currently, you can organize one folder at a time, or select multiple individual files. For batch processing of multiple folders, you can run the operation sequentially.
</details>

<details>
<summary><strong>Q: Does watch mode run in the background?</strong></summary>
<br>
A: Watch mode runs as long as the application is open. It monitors the source folder in real-time and automatically organizes new files as they appear.
</details>

<details>
<summary><strong>Q: How does duplicate detection work?</strong></summary>
<br>
A: The tool uses SHA-256 hashing to compare file contents. Even if files have different names, identical content will be detected as duplicates. You can choose to skip, rename, or delete duplicates.
</details>

<details>
<summary><strong>Q: Will this work with network drives or external hard drives?</strong></summary>
<br>
A: Yes! As long as the drive is mounted and accessible, you can organize files on any connected storage device.
</details>

<details>
<summary><strong>Q: Can I customize the folder structure?</strong></summary>
<br>
A: The folder structure is based on the organization method you choose (Date/Alphabetical/Size). Future versions may include custom templates.
</details>

<details>
<summary><strong>Q: Does it preserve file metadata (creation date, EXIF, etc.)?</strong></summary>
<br>
A: Yes! The tool uses `shutil.copy2()` which preserves metadata, and it reads EXIF data from images to organize them by their actual capture date.
</details>

<details>
<summary><strong>Q: What happens if I lose power during organization?</strong></summary>
<br>
A: Operations are performed file-by-file with logging. If interrupted, already-processed files remain organized, and you can run the tool again on remaining files. The undo log tracks completed operations.
</details>

<details>
<summary><strong>Q: Why is the EXE file so large (50-100 MB)?</strong></summary>
<br>
A: The EXE is a standalone executable that bundles Python, all libraries (Pillow, watchdog, etc.), and the application code. This makes it portable and eliminates the need for users to install Python separately.
</details>

<details>
<summary><strong>Q: Can I run this on macOS or Linux?</strong></summary>
<br>
A: Yes! The EXE is Windows-only, but you can run from source code on any platform (Windows, macOS, Linux) by installing Python and the required dependencies.
</details>

---

## 🐛 Known Issues

- **Windows EXE**: First launch may take 5-10 seconds as files are extracted
- **Windows Defender**: May show SmartScreen warning for unsigned executables
- **macOS**: Some cloud drive paths may require full disk access permissions
- **Linux**: Watch mode may require increased inotify limits for large folders
  ```bash
  # Increase inotify limits temporarily
  sudo sysctl fs.inotify.max_user_watches=524288
  ```

---

## 🗺️ Roadmap

- [x] Windows EXE executable for easy distribution
- [ ] macOS app bundle (.app)
- [ ] Linux AppImage/Flatpak
- [ ] Support for additional organization methods (by file extension, by camera model)
- [ ] Batch processing profiles (save and load configurations)
- [ ] Multi-language support
- [ ] Plugin system for custom organization rules
- [ ] CLI version for server/headless environments
- [ ] Web interface option
- [ ] Integration with major cloud APIs (not just local sync)

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/universal-file-organizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/universal-file-organizer/discussions)
- **Download EXE**: [Latest Releases](https://github.com/yourusername/universal-file-organizer/releases)

---

## 🙏 Acknowledgments

- Built with [Pillow](https://python-pillow.org/) for image processing
- File system monitoring powered by [Watchdog](https://github.com/gorakhargosh/watchdog)
- UI framework: [Tkinter](https://docs.python.org/3/library/tkinter.html)
- EXE packaging: [PyInstaller](https://www.pyinstaller.org/)

---

## 📧 Contact & Author

**Soumit Santra**  
*Creator & Lead Developer*

For questions, suggestions, feature requests, or collaboration opportunities, feel free to reach out!

- 🐙 **GitHub**: [github.com/Soumit-Santra](https://github.com/Soumit-Santra)

---

<p align="center">
  Made with ❤️ by <strong>Soumit Santra</strong>
</p>

<p align="center">
  <sub>A developer who hates disorganized files</sub>
</p>

<p align="center">
  <sub>If this tool saved you time, consider giving it a ⭐️ on GitHub!</sub>
</p>

---

## 🎉 Final Note

> **"Organization is not about perfection; it's about efficiency, reducing stress and clutter, saving time and money, and improving your overall quality of life."** — Christina Scalise

Thank you for using File Organizer! May your files always be perfectly organized! 🗂️✨

*Stay organized, stay productive! 📁🚀*
