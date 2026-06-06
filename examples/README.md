# Configuration Examples

This directory contains example configuration files for different use cases.

## Available Examples

### 1. IP Camera Configuration
**File:** [`ip_camera_config.json`](ip_camera_config.json)

**Use Case:** Monitoring with an IP camera via RTSP stream

**Features:**
- HD resolution (1280x720)
- Detects vehicles and people
- Saves detections
- Higher confidence threshold for fewer false positives

**Usage:**
```bash
python main.py examples/ip_camera_config.json
```

**Note:** Update the RTSP URL with your camera's credentials and IP address.

---

### 2. High Performance Configuration
**File:** [`high_performance_config.json`](high_performance_config.json)

**Use Case:** Maximum FPS for real-time monitoring

**Features:**
- Lower resolution (640x480) for speed
- Only detects people
- No file saving for maximum performance
- Higher confidence threshold

**Usage:**
```bash
python main.py examples/high_performance_config.json
```

**Best For:**
- Live monitoring without recording
- Systems with limited CPU/GPU
- Real-time person detection

---

### 3. Security Monitoring Configuration
**File:** [`security_monitoring_config.json`](security_monitoring_config.json)

**Use Case:** Comprehensive home/office security monitoring

**Features:**
- HD resolution (1280x720)
- Detects people, vehicles, pets, and suspicious items
- Saves all detections
- Records video
- Lower confidence threshold for better detection

**Usage:**
```bash
python main.py examples/security_monitoring_config.json
```

**Best For:**
- 24/7 security monitoring
- Evidence collection
- Comprehensive surveillance

---

## How to Use These Examples

### Method 1: Copy and Modify

1. Copy an example to the main directory:
   ```bash
   cp examples/ip_camera_config.json config.json
   ```

2. Edit the configuration:
   ```bash
   # Edit with your preferred editor
   notepad config.json  # Windows
   nano config.json     # Linux/Mac
   ```

3. Run the program:
   ```bash
   python main.py
   ```

### Method 2: Run Directly

Run with a specific example configuration:

```bash
python main.py examples/ip_camera_config.json
```

### Method 3: Use Quick Start

1. Run quick start:
   ```bash
   python quick_start.py
   ```

2. Select option 2 (Setup new configuration)

3. Follow the interactive prompts

---

## Creating Your Own Configuration

### Basic Template

```json
{
  "camera_source": 0,
  "detection_confidence": 0.5,
  "nms_threshold": 0.4,
  "frame_width": 640,
  "frame_height": 480,
  "save_detections": true,
  "output_dir": "detections",
  "show_fps": true,
  "detection_classes": [],
  "alert_on_detection": true,
  "record_video": false
}
```

### Configuration Parameters

| Parameter | Type | Description | Example Values |
|-----------|------|-------------|----------------|
| `camera_source` | int/string | Camera input | `0`, `"rtsp://..."`, `"video.mp4"` |
| `detection_confidence` | float | Min confidence (0.0-1.0) | `0.5`, `0.7` |
| `nms_threshold` | float | Non-max suppression | `0.4` |
| `frame_width` | int | Video width | `640`, `1280`, `1920` |
| `frame_height` | int | Video height | `480`, `720`, `1080` |
| `save_detections` | bool | Save detection images | `true`, `false` |
| `output_dir` | string | Output directory | `"detections"` |
| `show_fps` | bool | Show FPS counter | `true`, `false` |
| `detection_classes` | array | Objects to detect | `["person", "car"]` or `[]` for all |
| `alert_on_detection` | bool | Save alerts | `true`, `false` |
| `record_video` | bool | Record video | `true`, `false` |

### Detectable Object Classes

```json
"detection_classes": [
  "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
  "truck", "boat", "traffic light", "fire hydrant", "stop sign",
  "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
  "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
  "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
  "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
  "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
  "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
  "couch", "potted plant", "bed", "dining table", "toilet", "tv",
  "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
  "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
  "scissors", "teddy bear", "hair drier", "toothbrush"
]
```

---

## Use Case Recommendations

### Home Security
```json
{
  "detection_classes": ["person", "car", "dog", "cat"],
  "detection_confidence": 0.5,
  "save_detections": true,
  "record_video": true
}
```

### Traffic Monitoring
```json
{
  "detection_classes": ["car", "motorcycle", "bicycle", "bus", "truck"],
  "detection_confidence": 0.6,
  "frame_width": 1280,
  "frame_height": 720
}
```

### Pet Monitoring
```json
{
  "detection_classes": ["dog", "cat", "bird"],
  "detection_confidence": 0.4,
  "save_detections": true
}
```

### Office Monitoring
```json
{
  "detection_classes": ["person", "laptop", "cell phone", "backpack"],
  "detection_confidence": 0.5,
  "save_detections": true
}
```

### Parking Lot Monitoring
```json
{
  "detection_classes": ["car", "motorcycle", "bicycle", "truck", "person"],
  "detection_confidence": 0.6,
  "frame_width": 1920,
  "frame_height": 1080
}
```

---

## Performance Optimization Tips

### For Higher FPS
- Reduce resolution: `640x480` or `320x240`
- Increase confidence: `0.7` or higher
- Limit detection classes: Only what you need
- Disable saving: `"save_detections": false`
- Disable recording: `"record_video": false`

### For Better Accuracy
- Increase resolution: `1280x720` or `1920x1080`
- Lower confidence: `0.3` or `0.4`
- Detect all classes: `"detection_classes": []`
- Ensure good lighting

### For Storage Efficiency
- Disable recording: `"record_video": false`
- Only save on detection: `"alert_on_detection": true`
- Higher confidence: Fewer false positives
- Limit detection classes

---

## Testing Your Configuration

1. **Start with default settings**
2. **Test camera connection**
3. **Adjust confidence threshold**
4. **Fine-tune resolution**
5. **Select detection classes**
6. **Enable/disable features as needed**

---

## Troubleshooting

### Configuration Not Loading
- Check JSON syntax (commas, brackets, quotes)
- Verify file path is correct
- Use a JSON validator

### Poor Detection Performance
- Lower confidence threshold
- Improve lighting
- Adjust camera angle
- Check object is in detection classes

### Low FPS
- Reduce resolution
- Increase confidence threshold
- Limit detection classes
- Close other applications

---

For more information, see:
- [Main README](../README.md)
- [Setup Guide](../SETUP_GUIDE.md)
- [Main Program](../main.py)