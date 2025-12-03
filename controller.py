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

def disconnect(host: str = "all"):
    if host == "all":
        subprocess.run(["adb", "disconnect"])
    else:
        subprocess.run(["adb", "disconnect", host])

# --- INPUT ACTIONS ---
def tap(x: int, y: int):
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])

def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300):
    subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

def keyEvent(key: str, longpress: bool = False):
    if longpress:
        subprocess.run(["adb", "shell", "input", "keyevent", "--longpress", key])
    else:
        subprocess.run(["adb", "shell", "input", "keyevent", key])

# --- SCREEN CAPTURE ---
def screenshot_to_file(outputpath: str):
    """Saves screen to a file (Slower, good for debugging)"""
    with open(outputpath, 'wb') as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)
    return outputpath

def get_screen_stream():
    """
    Captures screen directly to memory as an OpenCV image.
    Much faster than saving to file.
    """
    cmd = ["adb", "exec-out", "screencap", "-p"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    screenshot_data, _ = process.communicate()

    if not screenshot_data:
        return None

    # Convert binary data to numpy array
    image_array = np.frombuffer(screenshot_data, np.uint8)
    
    # Decode to OpenCV image (BGR format)
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)