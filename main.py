"""
Real-Time CC Camera Analytics System
Supports object detection, tracking, and real-time monitoring
Enhanced with performance optimizations for faster detection
Now with YOLOv8 support for detecting all objects
"""

import cv2
import numpy as np
from datetime import datetime
import json
import os
from pathlib import Path
import threading
import queue
from collections import defaultdict
import time
from concurrent.futures import ThreadPoolExecutor

# Try to import YOLO
try:
    from ultralytics import YOLO  # type: ignore
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    YOLO = None  # type: ignore
    print("YOLOv8 not available. Install with: pip install ultralytics")

class CCCameraAnalytics:
    """
    Real-time camera analytics system with object detection and tracking
    Enhanced with performance optimizations
    """
    
    def __init__(self, config_path='config.json'):
        """Initialize the camera analytics system"""
        self.config = self.load_config(config_path)
        self.cap = None
        self.running = False
        self.frame_queue = queue.Queue(maxsize=2)  # Reduced queue size for lower latency
        self.detection_queue = queue.Queue(maxsize=2)
        self.detection_results = []
        self.object_counts = defaultdict(int)
        self.fps = 0
        self.frame_count = 0
        self.last_detection_time = time.time()
        
        # Performance optimization settings
        self.skip_frames = self.config.get('skip_frames', 2)  # Process every Nth frame
        self.use_motion_detection = self.config.get('use_motion_detection', True)
        self.motion_threshold = self.config.get('motion_threshold', 25)
        self.previous_frame = None
        self.last_detections = []
        self.show_help_overlay = False
        self.auto_fit_window = True  # Auto-fit window to camera resolution
        
        # Performance modes
        self.current_mode = "balanced"
        self.performance_modes = {
            "high_accuracy": {
                "skip_frames": 1,
                "use_motion_detection": False,
                "reduce_resolution": False,
                "name": "High Accuracy"
            },
            "balanced": {
                "skip_frames": 2,
                "use_motion_detection": True,
                "reduce_resolution": False,
                "name": "Balanced"
            },
            "high_performance": {
                "skip_frames": 3,
                "use_motion_detection": True,
                "reduce_resolution": True,
                "name": "High Performance"
            },
            "ultra_fast": {
                "skip_frames": 4,
                "use_motion_detection": True,
                "reduce_resolution": True,
                "name": "Ultra Fast"
            }
        }
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Initialize detector
        self.initialize_detector()
        
        # Create output directories
        self.setup_directories()
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Default configuration with performance optimizations
            return {
                "camera_source": 0,  # 0 for webcam, or RTSP URL for IP camera
                "detection_confidence": 0.5,
                "nms_threshold": 0.4,
                "frame_width": 640,
                "frame_height": 480,
                "save_detections": True,
                "output_dir": "detections",
                "show_fps": True,
                "detection_classes": ["person", "car", "dog", "cat", "bicycle", "motorcycle"],
                "alert_on_detection": True,
                "record_video": False,
                "skip_frames": 2,  # Process every 2nd frame for faster detection
                "use_motion_detection": True,  # Skip frames with no motion
                "motion_threshold": 25,  # Motion sensitivity (lower = more sensitive)
                "async_save": True,  # Save detections asynchronously
                "reduce_resolution": False,  # Reduce frame size for detection
                "detection_scale": 0.5  # Scale factor for detection (0.5 = half size)
            }
    
    def initialize_detector(self):
        """Initialize object detector - try YOLO first, then fallback to others"""
        print("Initializing object detector...")
        
        # Try to load YOLO first (best for all objects)
        self.yolo_model = None
        if YOLO_AVAILABLE and YOLO is not None:
            try:
                print("Loading YOLOv8 model...")
                self.yolo_model = YOLO('yolov8n.pt')  # type: ignore # nano model for speed
                print("YOLOv8 model loaded successfully - can detect 80+ object types!")
                return
            except Exception as e:
                print(f"Could not load YOLO model: {e}")
                print("Falling back to other detectors...")
        
        # COCO class names
        self.class_names = [
            'background', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
            'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
            'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
            'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
            'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
            'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
            'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
        
        # Use OpenCV's built-in HOG detector for person detection as fallback
        self.hog = cv2.HOGDescriptor()
        try:
            self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  # type: ignore
        except AttributeError:
            # Fallback for older OpenCV versions
            self.hog.setSVMDetector(cv2.HOGDescriptor.getDefaultPeopleDetector())  # type: ignore
        
        # Try to load pre-trained models (optional)
        self.net = None
        try:
            # Try to load MobileNet-SSD (you'll need to download these files)
            model_path = "models/MobileNetSSD_deploy.caffemodel"
            config_path = "models/MobileNetSSD_deploy.prototxt"
            
            if os.path.exists(model_path) and os.path.exists(config_path):
                self.net = cv2.dnn.readNetFromCaffe(config_path, model_path)
                print("MobileNet-SSD model loaded successfully")
            else:
                print("MobileNet-SSD model not found. Using HOG detector for person detection.")
                print("To enable full object detection, download MobileNet-SSD model files.")
        except Exception as e:
            print(f"Could not load DNN model: {e}")
            print("Using HOG detector for person detection only.")
    
    def setup_directories(self):
        """Create necessary output directories"""
        output_dir = self.config.get('output_dir', 'detections')
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        Path(f"{output_dir}/images").mkdir(parents=True, exist_ok=True)
        Path(f"{output_dir}/videos").mkdir(parents=True, exist_ok=True)
        Path(f"{output_dir}/logs").mkdir(parents=True, exist_ok=True)
    
    def connect_camera(self):
        """Connect to the camera source"""
        camera_source = self.config.get('camera_source', 0)
        print(f"Connecting to camera: {camera_source}")
        
        self.cap = cv2.VideoCapture(camera_source)
        
        if not self.cap.isOpened():
            raise Exception(f"Failed to open camera: {camera_source}")
        
        # Set camera properties
        width = self.config.get('frame_width', 640)
        height = self.config.get('frame_height', 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Set buffer size to 1 for lower latency
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        print("Camera connected successfully")
        return True
    
    def detect_objects_hog(self, frame):
        """Detect people using HOG detector (optimized)"""
        detections = []
        
        # Optionally reduce frame size for faster detection
        if self.config.get('reduce_resolution', False):
            scale = self.config.get('detection_scale', 0.5)
            small_frame = cv2.resize(frame, None, fx=scale, fy=scale)
        else:
            small_frame = frame
            scale = 1.0
        
        # Detect people with more sensitive parameters for better detection
        try:
            boxes, weights = self.hog.detectMultiScale(
                small_frame,
                winStride=(8, 8),    # More sensitive for better detection
                padding=(8, 8),
                scale=1.05           # More sensitive for better detection
            )
        except Exception as e:
            # Fallback to simpler parameters
            print(f"Detection warning: {e}")
            boxes, weights = self.hog.detectMultiScale(small_frame)
        
        for i, (x, y, w, h) in enumerate(boxes):
            if weights[i] > 0.5:  # Confidence threshold
                # Scale back to original coordinates
                detections.append({
                    'class': 'person',
                    'confidence': float(weights[i]),
                    'bbox': [int(x/scale), int(y/scale), int(w/scale), int(h/scale)]
                })
        
        return detections
    
    def detect_objects_yolo(self, frame):
        """Detect objects using YOLO model"""
        detections = []
        
        if self.yolo_model is None:
            return self.detect_objects_dnn(frame)
        
        try:
            # Run YOLO detection
            results = self.yolo_model(frame, verbose=False, conf=self.config.get('detection_confidence', 0.5))
            
            # Process results
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    
                    # Filter by detection classes if specified
                    detection_classes = self.config.get('detection_classes', [])
                    if detection_classes and class_name not in detection_classes:
                        continue
                    
                    detections.append({
                        'class': class_name,
                        'confidence': confidence,
                        'bbox': [int(x1), int(y1), int(x2-x1), int(y2-y1)]
                    })
        except Exception as e:
            print(f"YOLO detection error: {e}")
            return self.detect_objects_dnn(frame)
        
        return detections
    
    def detect_objects_dnn(self, frame):
        """Detect objects using DNN model (optimized)"""
        detections = []
        
        if self.net is None:
            return self.detect_objects_yolo(frame) if self.yolo_model else self.detect_objects_hog(frame)
        
        h, w = frame.shape[:2]
        
        # Optionally reduce frame size for faster detection
        if self.config.get('reduce_resolution', False):
            scale = self.config.get('detection_scale', 0.5)
            detection_frame = cv2.resize(frame, None, fx=scale, fy=scale)
        else:
            detection_frame = frame
            scale = 1.0
        
        # Create blob with smaller input size for speed
        blob = cv2.dnn.blobFromImage(detection_frame, 0.007843, (300, 300), 127.5)
        
        self.net.setInput(blob)
        detection_output = self.net.forward()
        
        confidence_threshold = self.config.get('detection_confidence', 0.5)
        
        for i in range(detection_output.shape[2]):
            confidence = detection_output[0, 0, i, 2]
            
            if confidence > confidence_threshold:
                class_id = int(detection_output[0, 0, i, 1])
                
                if class_id < len(self.class_names):
                    class_name = self.class_names[class_id]
                    
                    # Filter by detection classes if specified
                    detection_classes = self.config.get('detection_classes', [])
                    if detection_classes and class_name not in detection_classes:
                        continue
                    
                    # Scale coordinates back to original frame size
                    x1 = int(detection_output[0, 0, i, 3] * w / scale)
                    y1 = int(detection_output[0, 0, i, 4] * h / scale)
                    x2 = int(detection_output[0, 0, i, 5] * w / scale)
                    y2 = int(detection_output[0, 0, i, 6] * h / scale)
                    
                    detections.append({
                        'class': class_name,
                        'confidence': float(confidence),
                        'bbox': [x1, y1, x2 - x1, y2 - y1]
                    })
        
        return detections
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on frame"""
        for det in detections:
            x, y, w, h = det['bbox']
            class_name = det['class']
            confidence = det['confidence']
            
            # Draw bounding box
            color = (0, 255, 0)  # Green
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(frame, (x, y - label_size[1] - 10), (x + label_size[0], y), color, -1)
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return frame
    
    def save_detection(self, frame, detections):
        """Save detection image and log (optimized with async option)"""
        if not self.config.get('save_detections', True):
            return
        
        # Use async saving if enabled
        if self.config.get('async_save', True):
            self.executor.submit(self._save_detection_async, frame.copy(), detections)
        else:
            self._save_detection_sync(frame, detections)
    
    def _save_detection_sync(self, frame, detections):
        """Synchronous save (blocking)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        output_dir = self.config.get('output_dir', 'detections')
        
        # Save image with lower quality for speed
        image_path = f"{output_dir}/images/detection_{timestamp}.jpg"
        cv2.imwrite(image_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        
        # Save log (simplified - append only, no full reload)
        log_path = f"{output_dir}/logs/detections.json"
        log_entry = {
            'timestamp': timestamp,
            'detections': detections,
            'image_path': image_path
        }
        
        # Append to log file efficiently
        try:
            # Check if file exists and has content
            if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
                # Read existing logs
                with open(log_path, 'r') as f:
                    try:
                        logs = json.load(f)
                    except:
                        logs = []
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_path, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"Error saving log: {e}")
    
    def _save_detection_async(self, frame, detections):
        """Asynchronous save (non-blocking)"""
        self._save_detection_sync(frame, detections)
    
    def detect_motion(self, frame):
        """Detect if there's significant motion in the frame"""
        if self.previous_frame is None:
            self.previous_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return True
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate frame difference
        frame_diff = cv2.absdiff(self.previous_frame, gray)
        
        # Threshold the difference
        _, thresh = cv2.threshold(frame_diff, self.motion_threshold, 255, cv2.THRESH_BINARY)
        
        # Calculate percentage of changed pixels
        motion_pixels = np.sum(thresh) / 255
        total_pixels = thresh.shape[0] * thresh.shape[1]
        motion_percentage = (motion_pixels / total_pixels) * 100
        
        # Update previous frame
        self.previous_frame = gray
        
        # Return True if motion detected (more than 0.5% of pixels changed)
        return motion_percentage > 0.5
    
    def process_frame(self, frame, force_detection=False):
        """Process a single frame (optimized with frame skipping and motion detection)"""
        self.frame_count += 1
        
        # Skip frames for performance (unless forced)
        if not force_detection and self.frame_count % self.skip_frames != 0:
            # Use last detections for skipped frames (keeps boxes visible)
            detections = self.last_detections
        else:
            # Check for motion if enabled
            if self.use_motion_detection and not force_detection:
                has_motion = self.detect_motion(frame)
                if not has_motion:
                    # No motion, use last detections (keeps boxes visible)
                    detections = self.last_detections
                else:
                    # Motion detected, run detection
                    # Try YOLO first, then DNN, then HOG
                    if self.yolo_model:
                        detections = self.detect_objects_yolo(frame)
                    else:
                        detections = self.detect_objects_dnn(frame)
                    self.last_detections = detections
            else:
                # Always detect
                if self.yolo_model:
                    detections = self.detect_objects_yolo(frame)
                else:
                    detections = self.detect_objects_dnn(frame)
                self.last_detections = detections
        
        # Update object counts
        self.object_counts.clear()
        for det in detections:
            self.object_counts[det['class']] += 1
        
        # Draw detections
        annotated_frame = self.draw_detections(frame.copy(), detections)
        
        # Get frame dimensions
        h, w = annotated_frame.shape[:2]
        
        # Add performance mode and video source info
        mode_name = self.performance_modes[self.current_mode]["name"]
        camera_source = self.config.get('camera_source', 0)
        source_text = f"Source: {camera_source}" if isinstance(camera_source, str) else f"Camera {camera_source}"
        
        # Add info panel background (larger)
        cv2.rectangle(annotated_frame, (5, 5), (450, 180), (0, 0, 0), -1)
        cv2.rectangle(annotated_frame, (5, 5), (450, 180), (0, 255, 0), 3)
        
        # Add FPS counter
        if self.config.get('show_fps', True):
            cv2.putText(annotated_frame, f"FPS: {self.fps:.1f}", (15, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Add mode info
        cv2.putText(annotated_frame, f"Mode: {mode_name}", (15, 65),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Add video source
        cv2.putText(annotated_frame, source_text, (15, 95),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add motion detection status
        motion_status = "Motion: ON" if self.use_motion_detection else "Motion: OFF"
        motion_color = (0, 255, 0) if self.use_motion_detection else (0, 0, 255)
        cv2.putText(annotated_frame, motion_status, (15, 125),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, motion_color, 2)
        
        # Add save status
        save_status = "Save: ON" if self.config.get('save_detections', True) else "Save: OFF"
        save_color = (0, 255, 0) if self.config.get('save_detections', True) else (0, 0, 255)
        cv2.putText(annotated_frame, save_status, (15, 155),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, save_color, 2)
        
        # Add instruction at bottom
        if not self.show_help_overlay:
            instruction = "CLICK THIS WINDOW, then press keys (h=help, f=status, q=quit)"
            cv2.rectangle(annotated_frame, (5, h-40), (w-5, h-5), (0, 0, 0), -1)
            cv2.rectangle(annotated_frame, (5, h-40), (w-5, h-5), (255, 0, 0), 2)
            cv2.putText(annotated_frame, instruction, (10, h-15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show help overlay if requested
        if self.show_help_overlay:
            self.draw_help_overlay(annotated_frame)
        
        # Add object counts (if any)
        if self.object_counts:
            y_offset = 210
            cv2.putText(annotated_frame, "DETECTIONS:", (15, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_offset += 30
            for obj_class, count in self.object_counts.items():
                text = f"  {obj_class}: {count}"
                cv2.putText(annotated_frame, text, (15, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                y_offset += 30
        else:
            # Show "No detections" message
            cv2.putText(annotated_frame, "No objects detected", (15, 210),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 2)
            cv2.putText(annotated_frame, "(Move in front of camera)", (15, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
        
        # Save detection if objects found (throttled to avoid excessive saves)
        current_time = time.time()
        if detections and self.config.get('alert_on_detection', True):
            # Only save if at least 1 second has passed since last save
            if current_time - self.last_detection_time > 1.0:
                self.save_detection(annotated_frame, detections)
                self.last_detection_time = current_time
        
        return annotated_frame, detections
    
    def switch_mode(self, mode_key):
        """Switch to a different performance mode"""
        if mode_key in self.performance_modes:
            mode = self.performance_modes[mode_key]
            self.current_mode = mode_key
            self.skip_frames = mode["skip_frames"]
            self.use_motion_detection = mode["use_motion_detection"]
            self.config["reduce_resolution"] = mode["reduce_resolution"]
            print(f"\n[OK] Switched to {mode['name']} mode")
            print(f"  - Skip frames: {self.skip_frames}")
            print(f"  - Motion detection: {self.use_motion_detection}")
            print(f"  - Reduce resolution: {mode['reduce_resolution']}")
    
    def toggle_motion_detection(self):
        """Toggle motion detection on/off"""
        self.use_motion_detection = not self.use_motion_detection
        status = "ON" if self.use_motion_detection else "OFF"
        print(f"\n[OK] Motion detection: {status}")
    
    def toggle_save_detections(self):
        """Toggle saving detections on/off"""
        self.config["save_detections"] = not self.config.get("save_detections", True)
        status = "ON" if self.config["save_detections"] else "OFF"
        print(f"\n[OK] Save detections: {status}")
    
    def print_controls(self):
        """Print available keyboard controls"""
        print("\n" + "=" * 60)
        print("KEYBOARD CONTROLS")
        print("=" * 60)
        print("Basic Controls:")
        print("  q - Quit application")
        print("  p - Pause/Resume")
        print("  s - Save current frame")
        print("  h - Toggle help overlay")
        print("  w - Reset window size")
        print("  a - Toggle auto-fit window (match camera resolution)")
        print("\nPerformance Modes:")
        print("  1 - High Accuracy mode (slowest, best quality)")
        print("  2 - Balanced mode (default)")
        print("  3 - High Performance mode (fast)")
        print("  4 - Ultra Fast mode (fastest, lower quality)")
        print("\nToggles:")
        print("  m - Toggle motion detection ON/OFF")
        print("  d - Toggle save detections ON/OFF")
        print("  r - Toggle video recording ON/OFF")
        print("  f - Show FPS and current settings")
        print("=" * 60 + "\n")
    
    def draw_help_overlay(self, frame):
        """Draw responsive help overlay on the video frame"""
        h, w = frame.shape[:2]
        
        # Determine layout based on frame width
        # If wide enough (>900px), show on right side; otherwise center
        if w > 900:
            # Right-side panel layout
            panel_width = 380
            x1 = w - panel_width - 20
            x2 = w - 20
            y1 = 20
            y2 = h - 20
            text_x = x1 + 20
            title_x = x1 + 80
        else:
            # Centered overlay layout
            margin = int(w * 0.08)  # 8% margin
            x1 = margin
            x2 = w - margin
            y1 = 20
            y2 = h - 20
            text_x = x1 + 25
            title_x = w//2 - 120
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
        
        # Draw border
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
        
        # Title
        title_y = y1 + 45
        cv2.putText(frame, "KEYBOARD CONTROLS", (title_x, title_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Controls list - ALL controls included
        controls = [
            ("Basic Controls:", (255, 255, 0)),
            ("  Q - Quit application", (255, 255, 255)),
            ("  P - Pause/Resume video", (255, 255, 255)),
            ("  S - Save current frame", (255, 255, 255)),
            ("  H - Toggle this help", (255, 255, 255)),
            ("  W - Reset window size", (255, 255, 255)),
            ("  A - Auto-fit window", (255, 255, 255)),
            ("", (0, 0, 0)),
            ("Performance Modes:", (255, 255, 0)),
            ("  1 - High Accuracy", (255, 255, 255)),
            ("  2 - Balanced (default)", (255, 255, 255)),
            ("  3 - High Performance", (255, 255, 255)),
            ("  4 - Ultra Fast", (255, 255, 255)),
            ("", (0, 0, 0)),
            ("Feature Toggles:", (255, 255, 0)),
            ("  M - Motion detection", (255, 255, 255)),
            ("  D - Save detections", (255, 255, 255)),
            ("  R - Record video", (255, 255, 255)),
            ("  F - Show full status", (255, 255, 255)),
        ]
        
        y = title_y + 45
        line_height = 27
        
        for text, color in controls:
            if text:  # Skip empty lines
                # Adjust font size based on panel width
                font_scale = 0.47 if w > 900 else 0.48
                cv2.putText(frame, text, (text_x, y),
                           cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 1)
            y += line_height
        
        # Footer with auto-fit status
        footer_y = y2 - 25
        autofit_status = "ON" if self.auto_fit_window else "OFF"
        footer_text = f"Auto-fit: {autofit_status} | Press H to close"
        if w > 900:
            footer_x = text_x
        else:
            footer_x = x1 + 20
        cv2.putText(frame, footer_text, (footer_x, footer_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
    
    def print_status(self):
        """Print current system status"""
        mode_name = self.performance_modes[self.current_mode]["name"]
        print("\n" + "=" * 60)
        print("CURRENT STATUS")
        print("=" * 60)
        print(f"Performance Mode: {mode_name}")
        print(f"FPS: {self.fps:.1f}")
        print(f"Skip Frames: {self.skip_frames}")
        print(f"Motion Detection: {'ON' if self.use_motion_detection else 'OFF'}")
        print(f"Save Detections: {'ON' if self.config.get('save_detections', True) else 'OFF'}")
        print(f"Record Video: {'ON' if self.config.get('record_video', False) else 'OFF'}")
        print(f"Auto-fit Window: {'ON' if self.auto_fit_window else 'OFF'}")
        print(f"Resolution: {self.config.get('frame_width', 640)}x{self.config.get('frame_height', 480)}")
        print("=" * 60 + "\n")
    
    def start(self):
        """Start the camera analytics system"""
        if not self.connect_camera():
            return
        
        self.running = True
        print("\nCamera Analytics System Started (Performance Optimized)")
        print("\n" + "!" * 60)
        print("IMPORTANT: Click on the video window to use keyboard controls!")
        print("!" * 60)
        self.print_controls()
        
        # Get actual camera resolution
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) if self.cap else 640
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) if self.cap else 480
        
        # Create window with appropriate mode
        window_name = 'CC Camera Analytics (Optimized)'
        if self.auto_fit_window:
            # Auto-fit: Use AUTOSIZE to prevent manual resizing and match camera resolution
            cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
            print(f"[OK] Auto-fit enabled: Window locked to camera resolution {actual_width}x{actual_height}")
        else:
            # Manual mode: Use NORMAL to allow resizing
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 1280, 720)
            print("[OK] Manual resize mode: Window set to 1280x720 (resizable)")
        
        frame_count = 0
        start_time = time.time()
        paused = False
        
        video_writer = None
        if self.config.get('record_video', False):
            output_dir = self.config.get('output_dir', 'detections')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = f"{output_dir}/videos/recording_{timestamp}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # type: ignore
            fps = 20
            frame_size = (self.config.get('frame_width', 640), self.config.get('frame_height', 480))
            video_writer = cv2.VideoWriter(video_path, fourcc, fps, frame_size)
        
        annotated_frame = None
        try:
            while self.running:
                if not paused:
                    if self.cap is not None:
                        ret, frame = self.cap.read()
                    else:
                        ret = False
                        frame = None
                    
                    if not ret or frame is None:
                        print("Failed to read frame from camera")
                        break
                    
                    # Process frame
                    annotated_frame, detections = self.process_frame(frame)
                    
                    # Calculate FPS
                    frame_count += 1
                    if frame_count % 30 == 0:
                        end_time = time.time()
                        self.fps = 30 / (end_time - start_time)
                        start_time = time.time()
                    
                    # Record video if enabled
                    if video_writer is not None:
                        video_writer.write(annotated_frame)
                    
                    # Display frame
                    cv2.imshow(window_name, annotated_frame)
                    
                    # Check if window was closed by user (clicking X button)
                    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                        print("\nWindow closed by user")
                        break
                    
                    # Bring window to front on first frame
                    if frame_count == 1:
                        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
                        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 0)
                    
                    # Print detection summary
                    if detections:
                        summary = ", ".join([f"{k}: {v}" for k, v in self.object_counts.items()])
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected: {summary}")
                
                # Handle keyboard input (reduced wait time for better responsiveness)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\nStopping camera analytics...")
                    break
                elif key == ord('s'):
                    if annotated_frame is not None:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_dir = self.config.get('output_dir', 'detections')
                        save_path = f"{output_dir}/images/manual_{timestamp}.jpg"
                        cv2.imwrite(save_path, annotated_frame)
                        print(f"[OK] Frame saved: {save_path}")
                    else:
                        print("No frame available to save")
                elif key == ord('p'):
                    paused = not paused
                    print(f"\n[OK] {'Paused' if paused else 'Resumed'}")
                elif key == ord('h'):
                    self.show_help_overlay = not self.show_help_overlay
                    if not self.show_help_overlay:
                        self.print_controls()  # Also print to terminal when closing
                elif key == ord('1'):
                    self.switch_mode("high_accuracy")
                elif key == ord('2'):
                    self.switch_mode("balanced")
                elif key == ord('3'):
                    self.switch_mode("high_performance")
                elif key == ord('4'):
                    self.switch_mode("ultra_fast")
                elif key == ord('m'):
                    self.toggle_motion_detection()
                elif key == ord('d'):
                    self.toggle_save_detections()
                elif key == ord('r'):
                    self.config["record_video"] = not self.config.get("record_video", False)
                    status = "ON" if self.config["record_video"] else "OFF"
                    print(f"\n[OK] Video recording: {status}")
                    if self.config["record_video"] and video_writer is None:
                        output_dir = self.config.get('output_dir', 'detections')
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        video_path = f"{output_dir}/videos/recording_{timestamp}.avi"
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # type: ignore
                        fps = 20
                        frame_size = (self.config.get('frame_width', 640), self.config.get('frame_height', 480))
                        video_writer = cv2.VideoWriter(video_path, fourcc, fps, frame_size)
                        print(f"  Recording to: {video_path}")
                    elif not self.config["record_video"] and video_writer is not None:
                        video_writer.release()
                        video_writer = None
                        print("  Recording stopped")
                elif key == ord('f'):
                    self.print_status()
                elif key == ord('w'):
                    # Reset window based on auto-fit mode
                    if self.auto_fit_window:
                        if self.cap is not None:
                            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            cv2.resizeWindow(window_name, actual_width, actual_height)
                            print(f"\n[OK] Window reset to camera resolution: {actual_width}x{actual_height}")
                    else:
                        cv2.resizeWindow(window_name, 1280, 720)
                        print("\n[OK] Window reset to 1280x720")
                elif key == ord('a'):
                    # Toggle auto-fit window mode - requires window recreation
                    self.auto_fit_window = not self.auto_fit_window
                    status = "ON" if self.auto_fit_window else "OFF"
                    print(f"\n[OK] Auto-fit window: {status}")
                    
                    # Destroy and recreate window with new mode
                    cv2.destroyWindow(window_name)
                    
                    if self.auto_fit_window and self.cap is not None:
                        # Auto-fit: AUTOSIZE mode (locked to camera resolution)
                        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
                        print(f"  Window locked to camera resolution: {actual_width}x{actual_height}")
                    else:
                        # Manual mode: NORMAL mode (resizable)
                        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                        cv2.resizeWindow(window_name, 1280, 720)
                        print("  Window set to 1280x720 (resizable)")
        
        finally:
            # Cleanup
            if video_writer is not None:
                video_writer.release()
            
            if self.cap is not None:
                self.cap.release()
            
            cv2.destroyAllWindows()
            print("\nCamera analytics stopped")
    
    def stop(self):
        """Stop the camera analytics system"""
        self.running = False
        # Shutdown thread pool
        self.executor.shutdown(wait=False)


def main():
    """Main entry point"""
    print("=" * 50)
    print("CC Camera Real-Time Analytics System")
    print("Performance Optimized Version")
    print("=" * 50)
    
    # Check if config file exists
    config_path = 'config.json'
    if not os.path.exists(config_path):
        print(f"\nConfig file not found. Creating default config: {config_path}")
        default_config = {
            "camera_source": 0,
            "detection_confidence": 0.5,
            "nms_threshold": 0.4,
            "frame_width": 640,
            "frame_height": 480,
            "save_detections": True,
            "output_dir": "detections",
            "show_fps": True,
            "detection_classes": ["person", "car", "dog", "cat", "bicycle", "motorcycle"],
            "alert_on_detection": True,
            "record_video": False,
            "skip_frames": 2,
            "use_motion_detection": True,
            "motion_threshold": 25,
            "async_save": True,
            "reduce_resolution": False,
            "detection_scale": 0.5
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        print("Default config created. You can edit it to customize settings.")
    
    # Initialize and start analytics
    try:
        analytics = CCCameraAnalytics(config_path)
        analytics.start()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

# Made with Bob
