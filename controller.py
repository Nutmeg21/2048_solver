import subprocess
import cv2
import numpy as np

# --- CONNECTION MANAGEMENT ---
def checkConnections():
    """Returns a list of connected device serials."""
    process = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.read().decode("utf-8")
    output = output.replace("\r", "").split("\n")
    rtrn = []
    for connection in output[1:]:
        if connection.strip() == "":
            continue
        parts = connection.split("\t")
        if len(parts) > 1 and parts[1] == "device":
            rtrn.append(parts[0])
    return rtrn

def connect(host: str):
    subprocess.run(["adb", "connect", host])

# --- INPUT ACTIONS ---
def tap(x: int, y: int):
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])

def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 50):
    """
    Basic raw swipe command.
    Duration is in milliseconds (faster is better for 2048).
    """
    subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

def swipe_direction(direction: str):
    """
    Executes a swipe based on a direction string.
    Coordinates are hardcoded to the center of a typical 1080x1920 screen,
    but ADB scales them automatically for most devices.
    """
    # Center X is roughly 500, Center Y is roughly 1000
    if direction == "up":
        # Drag from bottom (1300) to top (1000)
        swipe(500, 1300, 500, 1000)
    elif direction == "down":
        # Drag from top (1000) to bottom (1300)
        swipe(500, 1000, 500, 1300)
    elif direction == "left":
        # Drag from right (800) to left (200)
        swipe(800, 1000, 200, 1000)
    elif direction == "right":
        # Drag from left (200) to right (800)
        swipe(200, 1000, 800, 1000)

# --- SCREEN CAPTURE ---
def get_screen_stream():
    """Captures screen directly to memory."""
    cmd = ["adb", "exec-out", "screencap", "-p"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    screenshot_data, _ = process.communicate()

    if not screenshot_data:
        return None

    image_array = np.frombuffer(screenshot_data, np.uint8)
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)