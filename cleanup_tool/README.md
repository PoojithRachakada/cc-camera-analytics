# CC Camera Analytics - Cleanup Tool

A user-friendly GUI application to manage and delete detection files based on time frames.

## 🎯 Purpose

This tool helps you clean up accumulated detection files (images, videos, and logs) to free up disk space. You can select specific time frames and file types to delete.

## 🚀 Quick Start

### Windows
Double-click `CLEANUP.bat` to launch the tool.

### Linux/Mac
```bash
python3 cleanup_detections.py
```

## 📋 Features

### Time Frame Options
- **Older than 1 day** - Delete files older than 24 hours
- **Older than 3 days** - Delete files older than 3 days
- **Older than 7 days** - Delete files older than 1 week (default)
- **Older than 30 days** - Delete files older than 1 month
- **All files** - Delete all detection files
- **Custom date range** - Specify exact date range (YYYY-MM-DD format)

### File Types
- ✅ **Detection Images** (.jpg) - Saved detection snapshots
- ✅ **Recorded Videos** (.mp4) - Recorded video files
- ✅ **Detection Logs** (.json) - Detection metadata logs

### Safety Features
- 📊 **Preview before delete** - See count and size of files to be deleted
- ⚠️ **Confirmation dialog** - Requires confirmation before deletion
- 🔍 **Scan function** - Update statistics without deleting
- 📁 **Selective deletion** - Choose which file types to delete

## 🖥️ User Interface

### Main Window
```
┌─────────────────────────────────────┐
│  🗑️ Cleanup Tool                    │
├─────────────────────────────────────┤
│  Select Time Frame                  │
│  ○ Older than 1 day                 │
│  ○ Older than 3 days                │
│  ● Older than 7 days                │
│  ○ Older than 30 days               │
│  ○ All files                        │
│  ○ Custom date range                │
│                                     │
│  Select File Types                  │
│  ☑ Detection Images (.jpg)          │
│  ☑ Recorded Videos (.mp4)           │
│  ☑ Detection Logs (.json)           │
│                                     │
│  Current Statistics                 │
│  ┌─────────────────────────────┐   │
│  │ Detection Images:  150 (45MB)│   │
│  │ Recorded Videos:    12 (2GB) │   │
│  │ Detection Logs:     150 (2MB)│   │
│  │ TOTAL:             312 (2.05GB)│  │
│  └─────────────────────────────┘   │
│                                     │
│  [🔍 Scan] [🗑️ Delete] [✖ Close]   │
└─────────────────────────────────────┘
```

## 📖 How to Use

### Step 1: Select Time Frame
Choose when files should be deleted:
- Use preset options (1, 3, 7, or 30 days)
- Or select "Custom date range" and enter dates in YYYY-MM-DD format

### Step 2: Select File Types
Check the boxes for file types you want to delete:
- Detection Images - Individual snapshots of detections
- Recorded Videos - Full video recordings
- Detection Logs - JSON metadata files

### Step 3: Scan Files
Click **"🔍 Scan Files"** to see:
- How many files match your criteria
- Total size of files to be deleted
- No files are deleted during scanning

### Step 4: Review Statistics
Check the statistics panel to verify:
- Number of files per type
- Total disk space to be freed
- Make sure the numbers look correct

### Step 5: Delete Files
Click **"🗑️ Delete Selected"** to:
1. See a confirmation dialog with details
2. Confirm deletion (cannot be undone!)
3. Files are permanently deleted
4. Statistics automatically update

## ⚠️ Important Notes

### Safety
- **Deletion is permanent** - Files cannot be recovered
- **Always scan first** - Review what will be deleted
- **Confirmation required** - You must confirm before deletion
- **Main log preserved** - The main `detections.json` log is never deleted

### File Dating
Files are dated based on:
1. **Filename timestamp** - Extracted from filename (most accurate)
2. **File modification time** - Used as fallback if filename parsing fails

### Custom Date Range
When using custom dates:
- Format must be: `YYYY-MM-DD` (e.g., 2024-01-15)
- "From" date is inclusive (00:00:00)
- "To" date is inclusive (23:59:59)
- Invalid dates will show an error

## 🔧 Requirements

- Python 3.8 or higher
- tkinter (included with Python on Windows)
- No additional packages required

### Installing tkinter (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

## 📁 File Structure

```
cleanup_tool/
├── cleanup_detections.py    # Main application
├── CLEANUP.bat              # Windows launcher
└── README.md                # This file
```

## 🐛 Troubleshooting

### "Python is not installed"
- Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "Tkinter is not installed"
- On Windows: Reinstall Python with "tcl/tk and IDLE" option
- On Linux: Install python3-tk package (see above)
- On macOS: Install python-tk via Homebrew

### "No files found"
- Check that detections directory exists
- Verify files match the selected time frame
- Try "All files" option to see if any files exist

### Files not deleting
- Check file permissions
- Close any programs that might be using the files
- Run as administrator (Windows) if needed

## 💡 Tips

1. **Regular Cleanup** - Run weekly to prevent disk space issues
2. **Keep Recent Files** - Use "Older than 7 days" for regular maintenance
3. **Backup Important Files** - Copy important detections before cleanup
4. **Test First** - Use scan function to preview before deleting
5. **Selective Deletion** - Uncheck file types you want to keep

## 📞 Support

For issues or questions:
1. Check this README for solutions
2. Review the main application documentation
3. Check file permissions and disk space
4. Verify Python and tkinter installation

## 🔄 Version History

- **v1.0** - Initial release
  - Time frame selection
  - File type filtering
  - Statistics preview
  - Safe deletion with confirmation