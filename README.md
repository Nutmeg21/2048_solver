# 2048 AI Solver For Android
## Also doubles as KFC K-Town Combo Challenge Solver

An intelligent Python bot that uses **Computer Vision (OpenCV)** to read the 2048 game board on your Android phone and **AI Algorithms** to determine the optimal move, executing swipes automatically via **ADB**.

This project separates the "Eyes" (Screen Reading), "Brain" (AI Logic), and "Hands" (ADB Actions) to solve the game efficiently.

## Project Structure

* **`main.py`** (The Brain): Coordinates the loop: Read Board -> Run AI Algorithm -> Execute Swipe.
* **`controller.py`** (The Hands): Handles ADB connection, high-speed screen capture, and sending physical swipe gestures.
* **`screen_reader.py`** (The Eyes): Uses OpenCV to recognize the 4x4 grid and identify the number on each tile.
* **`assets/`**: Contains reference images of the tiles (2, 4, 8, 16...) for template matching.

## Prerequisites

### Hardware
* An Android Device (Phone, Tablet, or Emulator) with the 2048 game installed.
* A USB Data Cable.

### Software
* **Python 3.x**
* **ADB (Android Debug Bridge)**: Must be installed and added to your system PATH.
    * *Windows:* [Download Platform Tools](https://developer.android.com/tools/releases/platform-tools)
    * *Mac:* `brew install android-platform-tools`
    * *Linux:* `sudo apt install adb`

## Setup Guide

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
git clone [https://github.com/YourUsername/2048-ai-solver.git](https://github.com/YourUsername/2048-ai-solver.git)
cd 2048-ai-solver
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

## 📸 How to Create Tile Assets

For the AI to "see" the board, it needs reference images for the tiles.

1.  Open the 2048 app on your phone.
2.  Take a raw ADB screenshot (crucial for color/pixel accuracy):
    ```bash
    adb exec-out screencap -p > board_reference.png
    ```
3.  Open `board_reference.png` in an image editor.
4.  **Crop** distinct images for each tile number (2, 4, 8, 16, etc.) and the empty grid background.
5.  Save them to the `assets/` folder (e.g., `assets/tile_2.png`, `assets/tile_4.png`).

## How To Use

Run the main script:

```bash
python main.py
```

The bot will automatically:
1.  Detect the current state of the board.
2.  Calculate the best move using the AI algorithm.
3.  Swipe the screen.
4.  Repeat until game over or 2048 is reached.

To stop the bot, press `Ctrl+C` in the terminal.

## Common Issues

**Bot makes random moves / Can't read board**
* **Cause:** The asset images might not match the current screen resolution or theme.
* **Fix:** Ensure you created assets using `adb exec-out screencap` and not by downloading generic images from the internet.

**`device unauthorized`**
* **Cause:** The computer is not trusted by the phone.
* **Fix:** Unplug the USB cable, plug it back in, and watch your phone screen for the "Allow USB Debugging" prompt.
