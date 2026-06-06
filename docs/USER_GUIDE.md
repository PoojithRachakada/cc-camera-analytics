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

---

**Need more help?** Check the other documentation files or contact support.