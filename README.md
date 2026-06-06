# CC Camera Analytics

High-performance real-time object detection system. Detects people, vehicles, animals, and 80+ objects with optimized performance (2-4x faster).

## 🚀 Quick Start

### For End Users (Easiest - No Python Needed)

1. **Get the Executable**
   - Download `CC_Camera_Analytics.exe` from your developer
   - Or build it yourself: Double-click `BUILD_EXE.bat`

2. **Run**
   - Double-click the `.exe` file
   - Wait 10-20 seconds for first launch
   - Press 'h' for help

### For Developers (Python Required)

1. **Install**: Double-click `INSTALL.bat`
2. **Run**: Double-click `START.bat`
3. **Press 'h'** for help

## 📁 Project Structure

```
cc_camera_analytics/
├── START.bat              # Run with Python
├── INSTALL.bat            # Install dependencies
├── BUILD_EXE.bat          # Create standalone .exe
├── main.py                # Main application
├── config.json            # Configuration
├── requirements.txt       # Dependencies
├── README.md              # This file
│
├── docs/                  # All documentation
│   ├── USER_GUIDE.md      # Complete user guide
│   ├── QUICK_REFERENCE.md # Keyboard shortcuts
│   ├── PERFORMANCE_GUIDE.md
│   ├── YOLO_DETECTION_GUIDE.md
│   ├── DISPLAY_INFO.md
│   └── ENABLE_LONG_PATHS.md
│
├── cleanup_tool/          # 🗑️ Cleanup utility
│   ├── cleanup_detections.py  # GUI cleanup app
│   ├── CLEANUP.bat        # Windows launcher
│   └── README.md          # Cleanup tool guide
│
├── scripts/               # Utility scripts
├── examples/              # Example configs
└── detections/            # Output files (auto-created)
```

## ⚡ Performance Modes

| Mode | Speed | Best For |
|------|-------|----------|
| High Accuracy (1) | Slowest | Critical applications |
| Balanced (2) | Medium | ⭐ Recommended |
| High Performance (3) | Fast | Real-time monitoring |
| Ultra Fast (4) | Fastest | High-speed scenarios |

Press 1-4 to switch modes while running.

## 🎮 Keyboard Controls

### Basic Controls
| Key | Action |
|-----|--------|
| H | Show/hide help overlay |
| Q | Quit application |
| P | Pause/Resume |
| S | Save current frame |
| W | Reset window size |
| A | Toggle auto-fit window |

### Performance Modes
| Key | Mode |
|-----|------|
| 1 | High Accuracy |
| 2 | Balanced (default) |
| 3 | High Performance |
| 4 | Ultra Fast |

### Feature Toggles
| Key | Action |
|-----|--------|
| M | Toggle motion detection |
| D | Toggle auto-save detections |
| R | Start/stop video recording |
| F | Show full status |

See [`docs/QUICK_REFERENCE.md`](docs/QUICK_REFERENCE.md) for complete guide.

## 🎯 Detection Capabilities

- **With YOLOv8**: 80+ objects (people, cars, bikes, animals, etc.)
- **Without YOLOv8**: People only (HOG detector)

See [`docs/YOLO_DETECTION_GUIDE.md`](docs/YOLO_DETECTION_GUIDE.md) for complete list.

## 📖 Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Complete user manual
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - All keyboard shortcuts
- **[Video Sources](docs/VIDEO_SOURCES.md)** - Configure camera/video sources
- **[Performance Guide](docs/PERFORMANCE_GUIDE.md)** - Optimization tips
- **[YOLO Guide](docs/YOLO_DETECTION_GUIDE.md)** - Object detection details
- **[Display Info](docs/DISPLAY_INFO.md)** - Interface guide
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - File organization

## 🔧 Configuration

Edit `config.json` to customize:

### Video Sources
```json
// Webcam
"camera_source": 0

// IP Camera (RTSP)
"camera_source": "rtsp://admin:password@192.168.1.100:554/stream1"

// Video File
"camera_source": "videos/sample.mp4"

// HTTP Stream
"camera_source": "http://192.168.1.100:8080/video"
```

### Other Settings
- Detection confidence threshold
- Performance mode defaults
- Auto-save options
- Output directories

See [`docs/VIDEO_SOURCES.md`](docs/VIDEO_SOURCES.md) for complete video source guide.

Example configs in [`examples/`](examples/) folder.

## 🛠️ Advanced Usage

```bash
# Run with default config
python main.py

# Run with custom config
python main.py --config examples/high_performance_config.json

# Install dependencies
pip install -r requirements.txt
```

## 📋 System Requirements

- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.8+ (for development)
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: Webcam, USB, or IP camera

## ✨ Features

- ⚡ **2-4x Performance Boost** - Optimized frame processing
- 🎯 **80+ Object Detection** - People, vehicles, animals, and more
- 📹 **Multiple Video Sources** - Webcam, IP camera, video files
- 🎥 **Video Recording** - Save sessions with detections
- 📸 **Auto-Save Detections** - Capture detected objects automatically
- 🖼️ **Smart Window Management** - Auto-fit or manual resize
- 🎮 **Real-time Controls** - Switch modes without restart
- 📊 **Performance Modes** - 4 optimized presets
- 🔍 **Motion Detection** - Skip static frames for efficiency
- 💾 **Async I/O** - Non-blocking file operations
- 🗑️ **Cleanup Tool** - Manage disk space by deleting old files

## 🗑️ Cleanup Tool

Manage accumulated detection files to free up disk space:

```bash
# Windows
cd cleanup_tool
CLEANUP.bat

# Linux/Mac
cd cleanup_tool
python3 cleanup_detections.py
```

**Features:**
- Delete files by time frame (1, 3, 7, 30 days, or custom range)
- Select file types (images, videos, logs)
- Preview before deletion
- Safe with confirmation dialogs

See [`cleanup_tool/README.md`](cleanup_tool/README.md) for complete guide.

##  Troubleshooting

**Python not found**: Install Python 3.8+ from python.org

**Long Path error**: See [`docs/ENABLE_LONG_PATHS.md`](docs/ENABLE_LONG_PATHS.md)

**Camera not opening**:
- Try different camera indices (0, 1, 2)
- Check `camera_source` in config.json
- See [`docs/VIDEO_SOURCES.md`](docs/VIDEO_SOURCES.md)

**Slow performance**: Press '3' or '4' for faster modes

**Window issues**: Press 'A' for auto-fit, 'W' to reset

See [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) for detailed troubleshooting.

## 📝 License

Provided as-is for educational and commercial use.

---

**Made with ❤️ for real-time computer vision**