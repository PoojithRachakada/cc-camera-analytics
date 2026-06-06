# CC Camera Analytics - On-Screen Display Information

## Enhanced Video Display

The video window now shows comprehensive real-time information in an overlay panel:

```
┌─────────────────────────────────────────────────────────────┐
│  ╔═══════════════════════════════════╗                      │
│  ║ FPS: 28.5                         ║                      │
│  ║ Mode: Balanced                    ║                      │
│  ║ Source: Camera 0                  ║  [Video Feed]        │
│  ║ Motion: ON                        ║                      │
│  ║ Save: ON                          ║                      │
│  ╚═══════════════════════════════════╝                      │
│                                                              │
│  person: 2                                                   │
│  car: 1                                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Information Panel Details

### Top Info Panel (Green Border)
Located at the top-left corner with a semi-transparent black background:

1. **FPS Counter** (Green)
   - Shows real-time frames per second
   - Updates every 30 frames
   - Example: `FPS: 28.5`

2. **Performance Mode** (Yellow)
   - Current active mode
   - Changes when you press 1-4
   - Examples:
     - `Mode: High Accuracy`
     - `Mode: Balanced`
     - `Mode: High Performance`
     - `Mode: Ultra Fast`

3. **Video Source** (White)
   - Shows camera/video source
   - Examples:
     - `Source: Camera 0` (webcam)
     - `Source: Camera 1` (USB camera)
     - `Source: rtsp://192.168.1.100:554/stream` (IP camera)
     - `Source: video.mp4` (video file)

4. **Motion Detection Status** (White)
   - Shows if motion detection is active
   - `Motion: ON` or `Motion: OFF`
   - Toggle with `m` key

5. **Save Status** (White)
   - Shows if auto-save is enabled
   - `Save: ON` or `Save: OFF`
   - Toggle with `d` key

### Object Detection Counts (Cyan)
Below the info panel:
- Lists each detected object type with count
- Updates in real-time
- Example:
  ```
  person: 2
  car: 1
  dog: 1
  ```

## Display Examples by Source Type

### Webcam Display
```
╔═══════════════════════════════════╗
║ FPS: 30.2                         ║
║ Mode: Balanced                    ║
║ Source: Camera 0                  ║
║ Motion: ON                        ║
║ Save: ON                          ║
╚═══════════════════════════════════╝
```

### IP Camera Display
```
╔═══════════════════════════════════╗
║ FPS: 25.8                         ║
║ Mode: High Performance            ║
║ Source: rtsp://192.168.1.100:554 ║
║ Motion: ON                        ║
║ Save: ON                          ║
╚═══════════════════════════════════╝
```

### Video File Display
```
╔═══════════════════════════════════╗
║ FPS: 28.5                         ║
║ Mode: High Accuracy               ║
║ Source: traffic_video.mp4         ║
║ Motion: OFF                       ║
║ Save: ON                          ║
╚═══════════════════════════════════╝
```

### USB Camera Display
```
╔═══════════════════════════════════╗
║ FPS: 27.3                         ║
║ Mode: Ultra Fast                  ║
║ Source: Camera 1                  ║
║ Motion: ON                        ║
║ Save: OFF                         ║
╚═══════════════════════════════════╝
```

## Color Coding

| Element | Color | Purpose |
|---------|-------|---------|
| Panel Border | Green | Easy visibility |
| FPS Counter | Green | Performance indicator |
| Mode Name | Yellow | Current mode highlight |
| Source Info | White | Source identification |
| Status Info | White | Settings status |
| Object Counts | Cyan | Detection results |
| Bounding Boxes | Green | Detected objects |

## Dynamic Updates

The display updates automatically when you:

1. **Switch Modes** (Press 1-4)
   - Mode name changes immediately
   - FPS adjusts to new mode

2. **Toggle Motion Detection** (Press m)
   - Status changes: `Motion: ON` ↔ `Motion: OFF`

3. **Toggle Save** (Press d)
   - Status changes: `Save: ON` ↔ `Save: OFF`

4. **Change Camera Source** (Edit config.json)
   - Source text updates on restart

## Benefits of Enhanced Display

✅ **At-a-Glance Status** - See all important info without console
✅ **Performance Monitoring** - Real-time FPS tracking
✅ **Mode Awareness** - Always know current performance mode
✅ **Source Verification** - Confirm correct camera/video source
✅ **Settings Visibility** - See active toggles instantly
✅ **Detection Feedback** - Live object counts

## Customization

To modify the display, edit the `process_frame()` method in [`main.py`](main.py:394):

- Change panel position: Modify rectangle coordinates
- Adjust colors: Change RGB values in `cv2.putText()`
- Resize text: Modify font scale parameter
- Add more info: Add additional `cv2.putText()` calls

## Tips

1. **Panel Position**: Top-left keeps it visible but non-intrusive
2. **Semi-transparent Background**: Black background with border improves readability
3. **Color Coding**: Different colors help distinguish information types
4. **Compact Layout**: All essential info in small space
5. **Real-time Updates**: No lag between changes and display

## Troubleshooting Display Issues

**Panel not visible?**
- Check if window is large enough
- Verify frame resolution in config.json

**Text overlapping?**
- Increase y_offset values
- Reduce font scale

**Colors hard to read?**
- Adjust background opacity
- Change text colors in code

**FPS counter not updating?**
- Check if show_fps is true in config
- Verify camera is providing frames

---

The enhanced display provides complete situational awareness while monitoring your camera feed!