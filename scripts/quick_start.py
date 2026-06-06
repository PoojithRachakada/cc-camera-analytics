"""
Quick Start Script for CC Camera Analytics
This script provides an easy way to test and run the camera analytics system
"""

import os
import sys
import json

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("  CC CAMERA REAL-TIME ANALYTICS - QUICK START")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    missing = []
    
    try:
        import cv2
        print("✓ OpenCV installed")
    except ImportError:
        missing.append("opencv-python")
        print("✗ OpenCV not found")
    
    try:
        import numpy
        print("✓ NumPy installed")
    except ImportError:
        missing.append("numpy")
        print("✗ NumPy not found")
    
    if missing:
        print("\n⚠️  Missing dependencies detected!")
        print("\nTo install missing packages, run:")
        print(f"  pip install {' '.join(missing)}")
        print("\nOr install all requirements:")
        print("  pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies installed!\n")
    return True

def setup_config():
    """Interactive configuration setup"""
    print("=" * 60)
    print("CONFIGURATION SETUP")
    print("=" * 60)
    print()
    
    config = {}
    
    # Camera source
    print("Camera Source Options:")
    print("  1. Webcam (default)")
    print("  2. USB Camera")
    print("  3. IP Camera (RTSP)")
    print("  4. Video File")
    
    choice = input("\nSelect camera source (1-4) [1]: ").strip() or "1"
    
    if choice == "1":
        config["camera_source"] = 0
        print("✓ Using default webcam")
    elif choice == "2":
        index = input("Enter camera index (0, 1, 2...) [1]: ").strip() or "1"
        config["camera_source"] = int(index)
        print(f"✓ Using USB camera at index {index}")
    elif choice == "3":
        rtsp = input("Enter RTSP URL (e.g., rtsp://user:pass@192.168.1.100:554/stream): ").strip()
        if rtsp:
            config["camera_source"] = rtsp
            print("✓ Using IP camera")
        else:
            config["camera_source"] = 0
            print("⚠️  No URL provided, using default webcam")
    elif choice == "4":
        video_path = input("Enter video file path: ").strip()
        if video_path and os.path.exists(video_path):
            config["camera_source"] = video_path
            print("✓ Using video file")
        else:
            config["camera_source"] = 0
            print("⚠️  File not found, using default webcam")
    else:
        config["camera_source"] = 0
        print("✓ Using default webcam")
    
    print()
    
    # Detection settings
    print("Detection Settings:")
    confidence = input("Detection confidence threshold (0.1-0.9) [0.5]: ").strip() or "0.5"
    config["detection_confidence"] = float(confidence)
    
    # Resolution
    print("\nVideo Resolution:")
    print("  1. 640x480 (Fast, recommended)")
    print("  2. 1280x720 (HD)")
    print("  3. 1920x1080 (Full HD)")
    
    res_choice = input("\nSelect resolution (1-3) [1]: ").strip() or "1"
    
    if res_choice == "2":
        config["frame_width"] = 1280
        config["frame_height"] = 720
    elif res_choice == "3":
        config["frame_width"] = 1920
        config["frame_height"] = 1080
    else:
        config["frame_width"] = 640
        config["frame_height"] = 480
    
    print()
    
    # Save detections
    save = input("Save detected objects to disk? (y/n) [y]: ").strip().lower() or "y"
    config["save_detections"] = save == "y"
    
    # Record video
    record = input("Record video to file? (y/n) [n]: ").strip().lower() or "n"
    config["record_video"] = record == "y"
    
    # Other settings
    config["nms_threshold"] = 0.4
    config["output_dir"] = "detections"
    config["show_fps"] = True
    config["detection_classes"] = ["person", "car", "dog", "cat", "bicycle", "motorcycle"]
    config["alert_on_detection"] = True
    
    # Save config
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✓ Configuration saved to config.json")
    print()

def show_menu():
    """Show main menu"""
    print("=" * 60)
    print("MAIN MENU")
    print("=" * 60)
    print()
    print("  1. Run with existing configuration")
    print("  2. Setup new configuration")
    print("  3. View current configuration")
    print("  4. Install dependencies")
    print("  5. Exit")
    print()

def view_config():
    """Display current configuration"""
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
        
        print("\n" + "=" * 60)
        print("CURRENT CONFIGURATION")
        print("=" * 60)
        print()
        print(json.dumps(config, indent=2))
        print()
    else:
        print("\n⚠️  No configuration file found. Please setup configuration first.")
        print()

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    print("Running: pip install -r requirements.txt")
    print()
    
    os.system("pip install -r requirements.txt")
    
    print("\n✓ Installation complete!")
    input("\nPress Enter to continue...")

def run_analytics():
    """Run the main analytics program"""
    print("\n" + "=" * 60)
    print("STARTING CAMERA ANALYTICS")
    print("=" * 60)
    print()
    print("Controls:")
    print("  q - Quit")
    print("  s - Save current frame")
    print("  p - Pause/Resume")
    print()
    print("Starting in 3 seconds...")
    print()
    
    import time
    time.sleep(3)
    
    # Import and run main program
    try:
        from main import main
        main()
    except Exception as e:
        print(f"\n❌ Error running analytics: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    print_banner()
    
    # Check dependencies first
    deps_ok = check_dependencies()
    
    while True:
        show_menu()
        choice = input("Select option (1-5): ").strip()
        
        if choice == "1":
            if not deps_ok:
                print("\n⚠️  Please install dependencies first (option 4)")
                input("\nPress Enter to continue...")
                continue
            
            if not os.path.exists("config.json"):
                print("\n⚠️  No configuration found. Setting up now...")
                setup_config()
            
            run_analytics()
        
        elif choice == "2":
            setup_config()
        
        elif choice == "3":
            view_config()
            input("Press Enter to continue...")
        
        elif choice == "4":
            install_dependencies()
            deps_ok = check_dependencies()
        
        elif choice == "5":
            print("\nGoodbye! 👋")
            sys.exit(0)
        
        else:
            print("\n⚠️  Invalid option. Please select 1-5.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 👋")
        sys.exit(0)

# Made with Bob
