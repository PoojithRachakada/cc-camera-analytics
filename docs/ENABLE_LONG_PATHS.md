# Enable Windows Long Paths to Install YOLOv8

## Why This Is Needed

YOLOv8 installation failed with this error:
```
OSError: [Errno 2] No such file or directory
HINT: This error might have occurred since this system does not have Windows Long Path support enabled.
```

To detect bottles, phones, cars, and 80+ objects (not just people), you need to enable Windows Long Paths first.

## Solution: Enable Long Paths in Windows

### Method 1: Using Registry Editor (Recommended)

1. **Press** `Windows + R`
2. **Type** `regedit` and press Enter
3. **Navigate to:**
   ```
   HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
   ```
4. **Find** `LongPathsEnabled` (or create it if it doesn't exist)
5. **Double-click** it and set value to `1`
6. **Click** OK
7. **Restart** your computer

### Method 2: Using Group Policy Editor

1. **Press** `Windows + R`
2. **Type** `gpedit.msc` and press Enter
3. **Navigate to:**
   ```
   Computer Configuration > Administrative Templates > System > Filesystem
   ```
4. **Find** "Enable Win32 long paths"
5. **Double-click** and set to **Enabled**
6. **Click** OK
7. **Restart** your computer

### Method 3: Using PowerShell (Admin Required)

1. **Right-click** Start menu
2. **Select** "Windows PowerShell (Admin)" or "Terminal (Admin)"
3. **Run this command:**
   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```
4. **Restart** your computer

## After Enabling Long Paths

1. **Restart your computer** (important!)
2. **Open terminal** in the project folder
3. **Run:**
   ```bash
   pip install ultralytics
   ```
4. **Wait** for installation to complete (~5-10 minutes)
5. **Run the app:**
   ```bash
   python main.py
   ```

## What You'll Get After Installation

### Before (Current - HOG Detector)
- ❌ Only detects: **person**
- ❌ Cannot detect bottles, phones, cars, etc.

### After (YOLOv8)
- ✅ Detects **80+ object types:**
  - **People & Animals**: person, dog, cat, horse, bird
  - **Vehicles**: car, truck, bus, motorcycle, bicycle
  - **Objects**: bottle, phone, laptop, cup, book
  - **Food**: pizza, banana, apple, sandwich
  - **And 70+ more!**

## Verification

After installation, when you run `python main.py`, you should see:
```
Loading YOLOv8 model...
YOLOv8 model loaded successfully - can detect 80+ object types!
```

Instead of:
```
YOLOv8 not available. Install with: pip install ultralytics
```

## Alternative: Use Pre-built Models

If you cannot enable Long Paths, you can download MobileNet-SSD models manually:

1. **Download these files:**
   - [MobileNetSSD_deploy.prototxt](https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.prototxt)
   - [MobileNetSSD_deploy.caffemodel](https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel)

2. **Create folder:**
   ```
   cc_camera_analytics/models/
   ```

3. **Place files** in the models folder

4. **Run app:**
   ```bash
   python main.py
   ```

This will detect 20 object types (better than 1, but not as good as YOLOv8's 80+).

## Need Help?

If you're still having issues:
1. Make sure you restarted your computer after enabling Long Paths
2. Try running PowerShell/Command Prompt as Administrator
3. Check if you have enough disk space (~2GB needed for YOLOv8)

---

**Once Long Paths are enabled and YOLOv8 is installed, you'll be able to detect bottles, phones, and 80+ other objects!**