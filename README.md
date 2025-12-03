# 2048 Solver
## Also doubles as KFC K-Town Combo Challenge Solver
---
# Android Automation Bot (ADB + OpenCV)

A lightweight Python framework for automating Android apps and games using **ADB (Android Debug Bridge)** and **Computer Vision**.

This project allows you to write scripts that "see" your phone screen using OpenCV and "touch" the screen using ADB, enabling the creation of game bots, testing scripts, or general automation tasks.

## 📁 Project Structure

* **`main.py`** (The Brain): Contains the main logic loop, decision making, and timing.
* **`controller.py`** (The Hands): Handles ADB connection, raw screen capture streaming, and input simulation (taps/swipes).
* **`screen_reader.py`** (The Eyes): Wraps OpenCV to handle image recognition and pixel analysis.
* **`assets/`**: Folder containing the reference images (templates) the bot looks for.

## 🚀 Prerequisites

### Hardware
* An Android Device (Phone, Tablet, or Emulator).
* A USB Data Cable.

### Software
* **Python 3.x**
* **ADB (Android Debug Bridge)**: Must be installed and added to your system PATH.
    * *Windows:* [Download Platform Tools](https://developer.android.com/tools/releases/platform-tools)
    * *Mac:* `brew install android-platform-tools`
    * *Linux:* `sudo apt install adb`

## 🛠️ Setup Guide

### 1. Phone Configuration
You must enable **USB Debugging** on your Android device:
1.  Go to **Settings** > **About Phone**.
2.  Tap **Build Number** 7 times to enable Developer Mode.
3.  Go to **Settings** > **System** > **Developer Options**.
4.  Enable **USB Debugging**.
5.  *(Optional)* Enable **Stay Awake** to keep the screen on while connected.

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone [https://github.com/YourUsername/your-repo-name.git](https://github.com/YourUsername/your-repo-name.git)
cd your-repo-name
pip install -r requirements.txt
```

### 3. Connect Device
1.  Plug your phone into the computer.
2.  Accept the **"Allow USB Debugging?"** popup on your phone screen (Check *"Always allow"*).
3.  Verify the connection:
    ```bash
    adb devices
    # Should show: <serial_number> device
    ```

## 📸 How to Create Assets

The bot relies on **Template Matching**. To teach the bot to click a button, you cannot simply download an image from Google; you must capture what your phone screen actually looks like.

1.  Open the app on your phone to the specific screen.
2.  Take a raw ADB screenshot (crucial for color accuracy):
    ```bash
    adb exec-out screencap -p > reference_screen.png
    ```
3.  Open `reference_screen.png` in an image editor.
4.  **Crop** the specific button or icon you want to interact with.
5.  Save the cropped image to the `assets/` folder (e.g., `assets/start_button.png`).
6.  Reference the filename in `main.py`.

## 🏃 Usage

Run the main script:

```bash
python main.py
```

To stop the bot, press `Ctrl+C` in the terminal.

## ⚠️ Common Issues

**Bot connects but can't find images**
* **Cause:** Images were likely taken using the phone's hardware buttons (Power+VolDown) or downloaded from the web.
* **Fix:** You **must** use `adb exec-out screencap -p` to take screenshots. This ensures the resolution and color formatting match exactly what the bot sees.

**`device unauthorized`**
* **Cause:** The computer is not trusted by the phone.
* **Fix:** Unplug the USB cable, plug it back in, and watch your phone screen for the "Allow USB Debugging" prompt.
