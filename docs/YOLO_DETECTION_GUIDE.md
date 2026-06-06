# YOLOv8 Object Detection Guide

## Overview

The CC Camera Analytics system now supports YOLOv8 for detecting 80+ different object types, not just people!

## What Can Be Detected?

YOLOv8 can detect these object categories:

### People & Animals
- person, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, bird

### Vehicles
- bicycle, car, motorcycle, airplane, bus, train, truck, boat

### Indoor Objects
- chair, couch, bed, dining table, toilet, tv, laptop, mouse, keyboard, cell phone
- bottle, wine glass, cup, fork, knife, spoon, bowl
- book, clock, vase, scissors, teddy bear, hair drier, toothbrush

### Outdoor Objects
- traffic light, fire hydrant, stop sign, parking meter, bench
- backpack, umbrella, handbag, tie, suitcase

### Sports & Recreation
- frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove
- skateboard, surfboard, tennis racket

### Food
- banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

### Appliances
- microwave, oven, toaster, sink, refrigerator

### And More!
- potted plant, and many other common objects

## Features

### 1. Persistent Detection Boxes
- Detection boxes stay visible until the object leaves the frame
- Boxes update when motion is detected
- Smooth tracking of objects

### 2. All Objects Detection
- Set `"detection_classes": []` in config.json to detect ALL objects
- Or specify only what you want: `["person", "car", "dog"]`

### 3. Confidence Threshold
- Adjust `detection_confidence` in config.json (0.0 to 1.0)
- Lower = more detections (may include false positives)
- Higher = fewer, more confident detections
- Recommended: 0.5 for balanced results

## Configuration

### Detect Everything
```json
{
  "detection_classes": [],
  "detection_confidence": 0.5
}
```

### Detect Specific Objects Only
```json
{
  "detection_classes": ["person", "car", "dog", "cat", "bicycle"],
  "detection_confidence": 0.5
}
```

### High Sensitivity (More Detections)
```json
{
  "detection_classes": [],
  "detection_confidence": 0.3
}
```

### High Precision (Fewer False Positives)
```json
{
  "detection_classes": [],
  "detection_confidence": 0.7
}
```

## Performance Impact

### YOLOv8n (Nano) - Default
- **Speed**: Very Fast (30-60 FPS)
- **Accuracy**: Good
- **Best for**: Real-time applications, webcams
- **Model**: yolov8n.pt (automatically downloaded)

### Performance Tips

1. **For Maximum Speed**:
   ```json
   {
     "skip_frames": 3,
     "reduce_resolution": true,
     "detection_confidence": 0.6
   }
   ```

2. **For Best Accuracy**:
   ```json
   {
     "skip_frames": 1,
     "reduce_resolution": false,
     "detection_confidence": 0.5
   }
   ```

3. **For Specific Objects Only**:
   ```json
   {
     "detection_classes": ["person", "car"],
     "detection_confidence": 0.5
   }
   ```

## How Detection Persistence Works

1. **Object Detected**: Box appears around object
2. **Frame Skipping**: Box stays visible even on skipped frames
3. **Motion Detection**: Box updates when motion detected
4. **Object Leaves**: Box disappears when object no longer detected

This ensures smooth, continuous tracking without flickering boxes.

## Installation

YOLOv8 is automatically installed with:
```bash
pip install ultralytics
```

On first run, it will download the yolov8n.pt model (~6MB).

## Fallback Behavior

If YOLOv8 is not available, the system automatically falls back to:
1. MobileNet-SSD (if models are available)
2. HOG detector (person detection only)

## Usage Examples

### Example 1: Home Security (People & Vehicles)
```json
{
  "detection_classes": ["person", "car", "bicycle", "motorcycle"],
  "detection_confidence": 0.6,
  "alert_on_detection": true
}
```

### Example 2: Pet Monitoring
```json
{
  "detection_classes": ["dog", "cat", "bird"],
  "detection_confidence": 0.5,
  "alert_on_detection": true
}
```

### Example 3: Traffic Monitoring
```json
{
  "detection_classes": ["car", "truck", "bus", "motorcycle", "bicycle"],
  "detection_confidence": 0.5,
  "skip_frames": 2
}
```

### Example 4: Retail/Store Monitoring
```json
{
  "detection_classes": ["person", "handbag", "backpack", "suitcase"],
  "detection_confidence": 0.6
}
```

### Example 5: Kitchen/Dining Monitoring
```json
{
  "detection_classes": ["person", "bottle", "cup", "bowl", "fork", "knife"],
  "detection_confidence": 0.5
}
```

## Troubleshooting

### No Objects Detected
- Lower `detection_confidence` to 0.3-0.4
- Ensure objects are clearly visible
- Check lighting conditions
- Verify `detection_classes` is empty [] or includes the objects

### Too Many False Detections
- Increase `detection_confidence` to 0.6-0.7
- Specify only needed objects in `detection_classes`
- Improve lighting conditions

### Slow Performance
- Increase `skip_frames` to 3 or 4
- Enable `reduce_resolution`
- Limit `detection_classes` to fewer objects

### Boxes Flickering
- This is now fixed! Boxes persist across frames
- If still occurring, reduce `skip_frames`

## Benefits of YOLOv8

✅ **80+ Object Types** - Detect almost anything
✅ **Fast Performance** - Real-time detection
✅ **High Accuracy** - State-of-the-art model
✅ **Easy to Use** - Automatic model download
✅ **Persistent Boxes** - Smooth tracking
✅ **Configurable** - Detect only what you need

## Comparison

| Feature | HOG | MobileNet-SSD | YOLOv8 |
|---------|-----|---------------|--------|
| Objects | Person only | 20 types | 80+ types |
| Speed | Fast | Medium | Very Fast |
| Accuracy | Good | Good | Excellent |
| Setup | Built-in | Manual | Automatic |
| **Recommended** | ❌ | ⚠️ | ✅ |

---

**YOLOv8 is now the default and recommended detector for the best experience!**