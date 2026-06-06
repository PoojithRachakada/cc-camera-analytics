# Scripts

This folder contains utility scripts and batch files for the CC Camera Analytics application.

## 🚀 Batch Files (Windows)

### START_CAMERA_ANALYTICS.bat
Main launcher script that:
- Checks for Python installation
- Verifies dependencies are installed
- Launches the camera analytics application
- Provides helpful error messages

**Usage**: Called by `START.bat` in the root directory

### INSTALL_DEPENDENCIES.bat
Dependency installer that:
- Installs OpenCV for camera and image processing
- Installs NumPy for numerical operations
- Installs Ultralytics for YOLOv8 object detection
- Provides installation progress and error handling

**Usage**: Called by `INSTALL.bat` in the root directory

### install_yolo.bat
Specialized script for installing YOLOv8:
- Attempts to install Ultralytics package
- Provides guidance if Long Path error occurs
- References ENABLE_LONG_PATHS.md for fixes

**Usage**: Run manually if YOLOv8 installation fails

## 🐍 Python Scripts

### quick_start.py
Quick start script for testing the application:
- Minimal configuration
- Fast setup for development
- Useful for debugging

**Usage**: 
```bash
python scripts/quick_start.py
```

## 📝 Notes

- All batch files are designed for Windows
- Linux/Mac users should use Python commands directly
- Scripts assume they are run from the project root directory
- Error messages guide users to relevant documentation

## 🔗 Related Files

- **Root Launchers**: [`../START.bat`](../START.bat), [`../INSTALL.bat`](../INSTALL.bat)
- **Documentation**: [`../docs/`](../docs/)
- **Main Application**: [`../main.py`](../main.py)

---

For non-technical users, use the simple launchers in the root directory:
- Double-click `INSTALL.bat` to install
- Double-click `START.bat` to run