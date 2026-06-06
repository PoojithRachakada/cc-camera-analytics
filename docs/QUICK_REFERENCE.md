# CC Camera Analytics - Quick Reference Guide

## 🎮 Keyboard Controls

### Basic Controls
| Key | Action | Description |
|-----|--------|-------------|
| `Q` | Quit | Exit the application |
| `P` | Pause/Resume | Pause or resume video processing |
| `S` | Save Frame | Manually save current frame as image |
| `H` | Help Overlay | Toggle on-screen help menu |
| `W` | Reset Window | Reset window to default size |
| `A` | Auto-fit Window | Toggle auto-fit (match camera resolution) |

### Performance Modes
| Key | Mode | FPS | Latency | Best For |
|-----|------|-----|---------|----------|
| `1` | High Accuracy | 8-15 | 100-200ms | Detailed analysis, small objects |
| `2` | Balanced | 20-30 | 50-100ms | General use (default) |
| `3` | High Performance | 30-45 | 30-50ms | Fast-moving objects |
| `4` | Ultra Fast | 40-60+ | 20-40ms | Maximum speed, large objects |

### Feature Toggles
| Key | Toggle | Description |
|-----|--------|-------------|
| `M` | Motion Detection | Enable/disable motion-based frame skipping |
| `D` | Save Detections | Enable/disable automatic saving of detections |
| `R` | Video Recording | Start/stop video recording (saves to detections/videos/) |
| `F` | Show Status | Display current FPS and all settings |

## 🚀 Performance Modes Explained

### Mode 1: High Accuracy
```
Skip Frames: 1 (process every frame)
Motion Detection: OFF
Resolution Scaling: OFF
```
**Use when:** You need maximum detection accuracy, detecting small objects, or analyzing slow-moving scenes.

### Mode 2: Balanced (Default)
```
Skip Frames: 2 (process every 2nd frame)
Motion Detection: ON
Resolution Scaling: OFF
```
**Use when:** General surveillance, home security, or balanced performance needs.

### Mode 3: High Performance
```
Skip Frames: 3 (process every 3rd frame)
Motion Detection: ON
Resolution Scaling: ON (50%)
```
**Use when:** Monitoring fast-moving objects, traffic, or need higher FPS.

### Mode 4: Ultra Fast
```
Skip Frames: 4 (process every 4th frame)
Motion Detection: ON
Resolution Scaling: ON (50%)
```
**Use when:** Maximum speed is critical, large objects only, or resource-constrained systems.

## 💡 Usage Examples

### Example 1: Start with High Performance
```bash
python main.py
# Press '3' to switch to High Performance mode
```

### Example 2: Toggle Features During Runtime
```bash
python main.py
# Press 'm' to disable motion detection
# Press 'd' to stop saving detections
# Press 'r' to start recording video
# Press 'f' to check current status
```

### Example 3: Quick Mode Switching
```bash
python main.py
# Start in Balanced mode (default)
# Press '4' for Ultra Fast when action starts
# Press '1' for High Accuracy when you need detail
# Press '2' to return to Balanced
```

## 📊 Performance Comparison

| Feature | Mode 1 | Mode 2 | Mode 3 | Mode 4 |
|---------|--------|--------|--------|--------|
| Frame Processing | 100% | 50% | 33% | 25% |
| CPU Usage | High | Medium | Low | Very Low |
| Detection Accuracy | Highest | High | Good | Moderate |
| Response Time | Slower | Fast | Faster | Fastest |
| Battery Impact | High | Medium | Low | Very Low |

## 🎯 Recommended Settings by Use Case

### Home Security
- **Mode:** Balanced (2)
- **Motion Detection:** ON
- **Save Detections:** ON
- **Recording:** OFF (enable when needed)

### Traffic Monitoring
- **Mode:** High Performance (3)
- **Motion Detection:** ON
- **Save Detections:** ON
- **Recording:** ON

### Wildlife Observation
- **Mode:** High Accuracy (1)
- **Motion Detection:** OFF
- **Save Detections:** ON
- **Recording:** Optional

### Parking Lot Surveillance
- **Mode:** Balanced (2)
- **Motion Detection:** ON
- **Save Detections:** ON
- **Recording:** Optional

### Indoor Pet Monitoring
- **Mode:** High Performance (3)
- **Motion Detection:** ON
- **Save Detections:** ON
- **Recording:** OFF

## 🔧 Troubleshooting Quick Fixes

### Problem: Too slow, missing fast objects
**Solution:** Press `3` or `4` for faster modes

### Problem: Missing small objects
**Solution:** Press `1` for High Accuracy mode

### Problem: Too many false detections
**Solution:** Press `m` to disable motion detection

### Problem: Disk filling up
**Solution:** Press `d` to disable auto-save

### Problem: Need to review footage
**Solution:** Press `r` to start recording

### Problem: Forgot controls
**Solution:** Press `h` to show help

## 📝 Status Information

Press `F` at any time to see:
- Current performance mode
- Real-time FPS
- Frame skip setting
- Motion detection status
- Save detections status
- Video recording status
- Auto-fit window status
- Current resolution

## 🎥 Video Recording

### How to Record
1. Press `R` to start recording
   - Console shows: "Video recording: ON"
   - File path displayed
2. Do your monitoring work
3. Press `R` again to stop
   - Video saved automatically

### Recording Details
- **Location:** `detections/videos/`
- **Format:** AVI (XVID codec)
- **Filename:** `recording_YYYYMMDD_HHMMSS.avi`
- **Content:** Live feed with all detections and overlays

### Image Saving

**Manual Save (Press 'S'):**
- Saves current frame immediately
- Location: `detections/images/manual_TIMESTAMP.jpg`

**Auto-Save (Press 'D' to toggle):**
- Automatically saves when objects detected
- Location: `detections/images/detection_TIMESTAMP.jpg`

## 🖼️ Window Management

### Auto-Fit Mode (Default - ON)
- Window locked to camera resolution
- Clearest image quality (1:1 pixels)
- Cannot be manually resized
- Press `A` to switch to manual mode

### Manual Resize Mode (OFF)
- Drag corners to resize window
- Default size: 1280x720
- Video scales to fit
- Press `A` to switch to auto-fit

### Reset Window (Press 'W')
- Auto-fit: Resets to camera resolution
- Manual: Resets to 1280x720

## 📹 Changing Video Source

Edit `config.json` to change video source:

### Webcam/USB Camera
```json
{
  "camera_source": 0
}
```
- `0` = First camera (built-in)
- `1` = Second camera (USB)
- `2` = Third camera, etc.

### IP Camera (RTSP)
```json
{
  "camera_source": "rtsp://admin:password@192.168.1.100:554/stream1"
}
```

### Video File
```json
{
  "camera_source": "videos/sample.mp4"
}
```

### HTTP Stream
```json
{
  "camera_source": "http://192.168.1.100:8080/video"
}
```

**See `docs/VIDEO_SOURCES.md` for complete guide**

## 🎬 Workflow Examples

### Workflow 1: Daily Monitoring
1. Start application: `python main.py`
2. Let it run in Balanced mode (default)
3. Press `f` periodically to check FPS
4. Press `3` if you need more speed
5. Press `q` to quit when done

### Workflow 2: Event Recording
1. Start application: `python main.py`
2. Wait for event to occur
3. Press `r` to start recording
4. Press `1` for best quality during event
5. Press `r` again to stop recording
6. Press `2` to return to normal mode

### Workflow 3: Performance Testing
1. Start application: `python main.py`
2. Press `f` to see baseline FPS
3. Press `1`, `2`, `3`, `4` to test each mode
4. Press `f` after each to compare FPS
5. Choose the mode that works best

## 🔄 Mode Switching Tips

- **Switch modes anytime** - No need to restart
- **Changes take effect immediately** - Next frame uses new settings
- **No data loss** - Switching modes doesn't affect saved data
- **Experiment freely** - Find what works best for your scenario
- **Use `f` key** - Check impact of mode changes on FPS

## 📱 Remote Operation Tips

If accessing remotely via VNC/RDP:
1. Use keyboard shortcuts for quick adjustments
2. Press `f` to monitor performance without GUI
3. Use `d` to reduce network bandwidth (disable saves)
4. Use higher modes (3-4) to reduce CPU load

## 🎓 Learning Path

**Beginner:** Start with mode 2 (Balanced), learn basic controls (q, p, s)

**Intermediate:** Experiment with modes 1-4, use toggles (m, d, r)

**Advanced:** Optimize for specific use case, fine-tune via config.json

---

**Quick Start:** Run `python main.py`, press `h` for help, press `f` for status!