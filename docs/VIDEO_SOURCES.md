# Video Source Configuration Guide

## Overview

CC Camera Analytics supports multiple video sources:
- **Webcam/USB Camera** (default)
- **IP Camera (RTSP/HTTP streams)**
- **Video Files** (MP4, AVI, etc.)
- **Multiple cameras** (by index)

## Changing Video Source

### Method: Edit config.json

1. Open `config.json` in the main folder
2. Find the `"camera_source"` line
3. Change the value based on your source type
4. Save the file
5. Restart the application

---

## Source Types

### 1. Webcam/USB Camera (Default)

**Built-in Webcam:**
```json
{
  "camera_source": 0
}
```

**External USB Camera:**
```json
{
  "camera_source": 1
}
```

**Multiple Cameras:**
- `0` = First camera (usually built-in)
- `1` = Second camera (usually USB)
- `2` = Third camera
- etc.

**How to find your camera index:**
1. Try `0` first (most common)
2. If that doesn't work, try `1`, then `2`, etc.
3. The app will show an error if the camera isn't found

---

### 2. IP Camera (RTSP Stream)

**Format:**
```json
{
  "camera_source": "rtsp://username:password@ip_address:port/stream"
}
```

**Examples:**

**Basic RTSP:**
```json
{
  "camera_source": "rtsp://192.168.1.100:554/stream1"
}
```

**With Authentication:**
```json
{
  "camera_source": "rtsp://admin:password123@192.168.1.100:554/stream1"
}
```

**Common IP Camera Paths:**
- Hikvision: `rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101`
- Dahua: `rtsp://admin:password@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0`
- Axis: `rtsp://admin:password@192.168.1.100:554/axis-media/media.amp`
- Generic: `rtsp://admin:password@192.168.1.100:554/stream1`

**Tips:**
- Check your camera's manual for the correct RTSP URL
- Default ports: 554 (RTSP), 8554 (alternative)
- Test the URL in VLC Media Player first

---

### 3. HTTP/MJPEG Stream

**Format:**
```json
{
  "camera_source": "http://ip_address:port/video"
}
```

**Examples:**

**Basic HTTP Stream:**
```json
{
  "camera_source": "http://192.168.1.100:8080/video"
}
```

**With Authentication:**
```json
{
  "camera_source": "http://admin:password@192.168.1.100:8080/video"
}
```

**Common Paths:**
- IP Webcam (Android): `http://192.168.1.100:8080/video`
- DroidCam: `http://192.168.1.100:4747/video`
- Generic MJPEG: `http://192.168.1.100/mjpeg`

---

### 4. Video File

**Format:**
```json
{
  "camera_source": "path/to/video.mp4"
}
```

**Examples:**

**Relative Path:**
```json
{
  "camera_source": "videos/sample.mp4"
}
```

**Absolute Path (Windows):**
```json
{
  "camera_source": "C:/Users/YourName/Videos/sample.mp4"
}
```

**Absolute Path (Linux/Mac):**
```json
{
  "camera_source": "/home/username/videos/sample.mp4"
}
```

**Supported Formats:**
- MP4 (`.mp4`)
- AVI (`.avi`)
- MOV (`.mov`)
- MKV (`.mkv`)
- WMV (`.wmv`)
- FLV (`.flv`)

**Note:** Use forward slashes `/` even on Windows, or double backslashes `\\`

---

## Complete Examples

### Example 1: Webcam Configuration
```json
{
  "camera_source": 0,
  "frame_width": 640,
  "frame_height": 480,
  "detection_confidence": 0.5
}
```

### Example 2: IP Camera Configuration
```json
{
  "camera_source": "rtsp://admin:camera123@192.168.1.100:554/stream1",
  "frame_width": 1280,
  "frame_height": 720,
  "detection_confidence": 0.6
}
```

### Example 3: Video File Configuration
```json
{
  "camera_source": "videos/traffic.mp4",
  "frame_width": 1920,
  "frame_height": 1080,
  "detection_confidence": 0.5,
  "record_video": false
}
```

### Example 4: HTTP Stream Configuration
```json
{
  "camera_source": "http://192.168.1.100:8080/video",
  "frame_width": 640,
  "frame_height": 480,
  "detection_confidence": 0.5
}
```

---

## Troubleshooting

### Camera Not Found
**Error:** "Failed to connect to camera"

**Solutions:**
1. **Webcam:** Try different indices (0, 1, 2)
2. **IP Camera:** 
   - Verify IP address and port
   - Check username/password
   - Test URL in VLC Media Player
   - Ensure camera is on same network
3. **Video File:**
   - Check file path is correct
   - Verify file exists
   - Use forward slashes in path

### Poor Video Quality
**Solutions:**
1. Increase `frame_width` and `frame_height`
2. For IP cameras, use main stream instead of sub-stream
3. Check camera settings for quality/bitrate

### Lag/Delay
**Solutions:**
1. Use sub-stream for IP cameras (lower resolution)
2. Switch to faster performance mode (press 3 or 4)
3. Enable motion detection (press M)
4. Reduce `frame_width` and `frame_height`

### Connection Timeout
**For IP Cameras:**
1. Check network connectivity
2. Verify firewall settings
3. Try different stream path
4. Reduce resolution in camera settings

---

## Quick Start Examples

### Use Built-in Webcam
```bash
# config.json
"camera_source": 0

# Run
START.bat
```

### Use IP Camera
```bash
# config.json
"camera_source": "rtsp://admin:pass@192.168.1.100:554/stream1"

# Run
START.bat
```

### Analyze Video File
```bash
# config.json
"camera_source": "videos/sample.mp4"

# Run
START.bat
```

---

## Testing Your Configuration

1. **Edit config.json** with your source
2. **Save the file**
3. **Run START.bat**
4. **Check console output:**
   - Success: "Camera connected successfully"
   - Failure: "Failed to connect to camera"
5. **If failed:** Try different source or check troubleshooting

---

## Advanced: Multiple Configurations

Create separate config files for different sources:

**config_webcam.json:**
```json
{
  "camera_source": 0
}
```

**config_ipcam.json:**
```json
{
  "camera_source": "rtsp://192.168.1.100:554/stream1"
}
```

**config_video.json:**
```json
{
  "camera_source": "videos/sample.mp4"
}
```

**Run with specific config:**
```bash
python main.py --config config_ipcam.json
```

---

## Need Help?

1. Check camera manual for RTSP/HTTP URL
2. Test stream in VLC Media Player first
3. Verify network connectivity for IP cameras
4. Check file path for video files
5. Try webcam index 0, 1, 2 for USB cameras

**Common Issues:**
- Wrong username/password → Check camera settings
- Wrong IP address → Use camera's IP scanner app
- Wrong port → Check camera documentation
- File not found → Use absolute path

---

**Quick Reference:**
- Webcam: `0` or `1`
- IP Camera: `"rtsp://user:pass@ip:port/path"`
- Video File: `"path/to/video.mp4"`
- HTTP Stream: `"http://ip:port/video"`