# CC Camera Analytics - User Guide

## Quick Start

### Option 1: Standalone Executable (Easiest - No Python Needed)

**For End Users:**
1. Download `CC_Camera_Analytics.exe` from your developer
2. Double-click the `.exe` file
3. Wait 10-20 seconds for first launch
4. Press 'h' for help

**For Developers (Creating the Executable):**
1. Double-click `BUILD_EXE.bat` in the main folder
2. Wait 5-15 minutes for build to complete
3. Executable will be in `dist/` folder
4. Share the `dist/` folder with users

### Option 2: Python Script (Requires Python)

1. **Install Dependencies** (One-time only)
   - Double-click `INSTALL.bat` in the main folder
   - Wait for installation to complete (5-10 minutes)
   - If you see "Long Path" error, see [Troubleshooting](#troubleshooting) below

2. **Run the Application**
   - Double-click `START.bat` in the main folder
   - The camera window will open automatically
   - Click on the video window to activate controls

### Using the Application

#### Basic Controls
- **Press 'Q'** - Quit the application
- **Press 'P'** - Pause/Resume video
- **Press 'S'** - Save current frame as image
- **Press 'H'** - Toggle help overlay (shows all controls)
- **Press 'W'** - Reset window to default size
- **Press 'A'** - Toggle auto-fit window (match camera resolution)

#### Performance Modes (Press number keys)
- **Press '1'** - High Accuracy (slowest, most accurate)
- **Press '2'** - Balanced (recommended for most users)
- **Press '3'** - High Performance (faster, good accuracy)
- **Press '4'** - Ultra Fast (fastest, basic detection)

#### Feature Toggles
- **Press 'M'** - Toggle motion detection ON/OFF (skip static frames)
- **Press 'D'** - Toggle auto-save detections ON/OFF
- **Press 'R'** - Toggle video recording ON/OFF
- **Press 'F'** - Show full status (FPS, settings, etc.)

### Recording Video

**How to Record:**
1. Press **'R'** to start recording
   - Console shows: "Video recording: ON"
   - File path displayed: `detections/videos/recording_TIMESTAMP.avi`
2. Do your monitoring/detection work
3. Press **'R'** again to stop recording
   - Console shows: "Video recording: OFF"
   - Video file saved automatically

**Video Details:**
- **Location:** `detections/videos/` folder
- **Format:** AVI (XVID codec)
- **Filename:** `recording_YYYYMMDD_HHMMSS.avi`
- **Content:** Live feed with all detections, bounding boxes, labels, and overlays

### Saving Images

**Manual Save (Press 'S'):**
- Saves current frame immediately
- Location: `detections/images/manual_TIMESTAMP.jpg`

**Auto-Save Detections (Press 'D' to toggle):**
- Automatically saves frames when objects detected
- Location: `detections/images/detection_TIMESTAMP.jpg`
- Toggle ON/OFF as needed

### Window Management

**Auto-Fit Mode (Default - ON):**
- Window locked to camera resolution (e.g., 640x480)
- Provides clearest image (1:1 pixel mapping)
- Cannot be manually resized
- Press **'A'** to switch to manual mode

**Manual Resize Mode (OFF):**
- Window can be resized by dragging corners
- Default size: 1280x720
- Video scales to fit window
- Press **'A'** to switch to auto-fit mode

**Reset Window (Press 'W'):**
- Auto-fit mode: Resets to camera resolution
- Manual mode: Resets to 1280x720

### Understanding the Display

The video window shows:
- **Green boxes** - Detected objects with labels
- **Top-left panel** - Current status information:
  - FPS (frames per second)
  - Performance mode
  - Video source (camera or file)
  - Motion detection status
  - Recording status

### What Can It Detect?

Depending on your setup:
- **With YOLOv8 installed**: 80+ objects (people, cars, animals, etc.)
- **Without YOLOv8**: People only (using HOG detector)

See [`YOLO_DETECTION_GUIDE.md`](YOLO_DETECTION_GUIDE.md) for complete list of detectable objects.

### Configuration

Edit `config.json` to customize:
- Camera source (webcam, IP camera, video file)
- Detection confidence threshold
- Save locations for images and videos
- Performance settings

**Example configurations** are in the [`../examples/`](../examples/) folder:
- `high_performance_config.json` - For fast detection
- `ip_camera_config.json` - For network cameras
- `security_monitoring_config.json` - For 24/7 monitoring

### Troubleshooting

#### "Python not found" error
- Install Python 3.8 or higher from python.org
- During installation, check "Add Python to PATH"

#### "Long Path" error during installation
1. Open [`ENABLE_LONG_PATHS.md`](ENABLE_LONG_PATHS.md)
2. Follow the instructions to enable Windows Long Paths
3. Run `INSTALL.bat` again

#### Camera not opening
- Check if another application is using the camera
- Try changing `video_source` in `config.json` to `1` or `2`
- For IP cameras, verify the URL in config.json

#### Slow performance
- Press '3' or '4' for faster modes
- Press 'm' to enable motion detection
- Close other applications using the camera
- See [`PERFORMANCE_GUIDE.md`](PERFORMANCE_GUIDE.md) for detailed optimization

#### No objects detected
- Ensure good lighting
- Move closer to the camera
- Lower `detection_confidence` in config.json (try 0.3)
- Check if YOLOv8 is installed for detecting more than people

### Getting Help

1. **Quick Reference**: See [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) for all keyboard shortcuts
2. **Performance Issues**: See [`PERFORMANCE_GUIDE.md`](PERFORMANCE_GUIDE.md) for optimization tips
3. **Display Information**: See [`DISPLAY_INFO.md`](DISPLAY_INFO.md) for understanding the interface
4. **Object Detection**: See [`YOLO_DETECTION_GUIDE.md`](YOLO_DETECTION_GUIDE.md) for detection capabilities

### Advanced Users

For developers and advanced users:
- Run directly: `python main.py`
- Custom config: `python main.py --config examples/custom_config.json`
- See [`../README.md`](../README.md) for technical documentation

### Tips for Best Results

1. **Good Lighting**: Ensure the area is well-lit
2. **Camera Position**: Place camera at eye level for best detection
3. **Stable Mount**: Use a tripod or stable surface
4. **Performance Mode**: Start with "Balanced" mode (press '2')
5. **Motion Detection**: Enable for static camera setups (press 'm')

### File Locations

- **Detected Images**: `detections/images/`
- **Recorded Videos**: `detections/videos/`
- **Detection Logs**: `detections/logs/detections.json`

### System Requirements

- **Operating System**: Windows 10/11, Linux, macOS
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: Built-in webcam, USB camera, or IP camera
- **Disk Space**: 500MB for installation, more for recordings

### Privacy and Security

- All processing is done locally on your computer
- No data is sent to external servers
- Recordings are saved only to your local disk
- You have full control over all saved files

## 🗑️ Cleanup Tool - Managing Disk Space

As you use the application, detection files accumulate and can take up significant disk space. The Cleanup Tool helps you manage these files efficiently.

### What Gets Saved?
- **Detection Images** - Snapshots when objects are detected (`.jpg` files)
- **Recorded Videos** - Full video recordings with detections (`.mp4` files)
- **Detection Logs** - Metadata about detections (`.json` files)

### Running the Cleanup Tool

**Windows:**
1. Navigate to the `cleanup_tool` folder
2. Double-click `CLEANUP.bat`
3. The GUI window will open

**Linux/Mac:**
```bash
cd cleanup_tool
python3 cleanup_detections.py
```

### Using the Cleanup Tool

#### Step 1: Select Time Frame
Choose which files to delete based on age:
- **Older than 1 day** - Delete yesterday's files
- **Older than 3 days** - Keep last 3 days
- **Older than 7 days** - Keep last week (recommended)
- **Older than 30 days** - Keep last month
- **All files** - Delete everything (use with caution!)
- **Custom date range** - Specify exact dates (YYYY-MM-DD format)

#### Step 2: Select File Types
Check which types of files to delete:
- ☑ Detection Images (.jpg)
- ☑ Recorded Videos (.mp4)
- ☑ Detection Logs (.json)

Uncheck any types you want to keep.

#### Step 3: Scan Files
Click **"🔍 Scan Files"** to preview:
- Number of files that will be deleted
- Total disk space that will be freed
- Breakdown by file type

**No files are deleted during scanning** - it's safe to scan multiple times.

#### Step 4: Delete Files
Click **"🗑️ Delete Selected"** to:
1. See a confirmation dialog with details
2. Confirm the deletion (cannot be undone!)
3. Files are permanently deleted
4. Statistics automatically update

### Safety Features
- ✅ **Preview before delete** - Always see what will be deleted
- ✅ **Confirmation required** - Must confirm before deletion
- ✅ **Main log preserved** - The main `detections.json` is never deleted
- ✅ **Selective deletion** - Choose specific file types and time frames

### Tips for Regular Maintenance
1. **Weekly Cleanup** - Run every week with "Older than 7 days"
2. **Before Important Sessions** - Free up space before recording
3. **Backup First** - Copy important files before cleanup
4. **Test with Scan** - Always scan first to verify selection
5. **Keep Recent Files** - Don't delete files from last few days

### Example Scenarios

**Scenario 1: Regular Maintenance**
- Time Frame: "Older than 7 days"
- File Types: All checked
- Result: Keeps last week, deletes older files

**Scenario 2: Free Up Space Quickly**
- Time Frame: "Older than 30 days"
- File Types: Videos only
- Result: Deletes old videos (largest files), keeps images

**Scenario 3: Clean Specific Period**
- Time Frame: "Custom date range" (2024-01-01 to 2024-01-31)
- File Types: All checked
- Result: Deletes only files from January 2024

### Troubleshooting Cleanup Tool

**"No files found"**
- Check that `detections/` folder exists
- Verify files match the selected time frame
- Try "All files" to see if any files exist

**"Permission denied"**
- Close the main application first
- Run as administrator (Windows)
- Check file permissions

**"Tkinter not installed"**
- Windows: Reinstall Python with "tcl/tk and IDLE" option
- Linux: `sudo apt-get install python3-tk`
- macOS: `brew install python-tk`

For complete cleanup tool documentation, see [`cleanup_tool/README.md`](../cleanup_tool/README.md).

---

**Need more help?** Check the other documentation files or contact support.