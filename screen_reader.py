import cv2
import numpy as np
import subprocess
import sys

class ScreenReader:
    def __init__(self, device_id=None):
        """
        Initializes the ScreenReader.
        :param device_id: Optional ADB device ID if multiple devices are connected.
        """
        self.device_id = device_id

    def capture_screen(self):
        """
        Captures the current screen of the Android device.
        
        Returns:
            numpy.ndarray: The screen image in BGR format (OpenCV standard),
                           or None if capture failed.
        """
        # Build the ADB command
        cmd = ["adb"]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        
        # 'exec-out' streams the binary output to stdout, skipping file I/O
        cmd.extend(["exec-out", "screencap", "-p"])

        try:
            # Execute command and capture raw binary output
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            screenshot_data, stderr = process.communicate()

            if not screenshot_data:
                print("Error: Failed to capture screen. Check ADB connection.")
                if stderr:
                    print(f"ADB Error: {stderr.decode()}")
                return None

            # Convert raw binary data to a numpy array
            image_array = np.frombuffer(screenshot_data, np.uint8)
            
            # Decode the numpy array into an OpenCV image
            screen_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            return screen_img

        except Exception as e:
            print(f"Exception during screen capture: {e}")
            return None

    def find_template(self, screen_img, template_path, threshold=0.8):
        """
        Locates a smaller image (template) inside the larger screen image.
        
        Args:
            screen_img: The main screen image (from capture_screen).
            template_path: Path to the .png file of the button/icon to find.
            threshold: Confidence level (0.0 to 1.0). Higher = stricter match.
            
        Returns:
            tuple: (x, y) coordinates of the center of the match, or None if not found.
        """
        if screen_img is None:
            return None

        # Load the template image
        # cv2.IMREAD_COLOR loads it in BGR format
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        
        if template is None:
            print(f"Error: Could not load template file: {template_path}")
            return None

        # Get dimensions of the template
        h, w = template.shape[:2]

        # Perform Template Matching
        result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        
        # Find the best match position
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if the best match is good enough
        if max_val >= threshold:
            # max_loc is the top-left corner. Calculate the center.
            center_x = int(max_loc[0] + w / 2)
            center_y = int(max_loc[1] + h / 2)
            return (center_x, center_y)
        
        return None

    def get_pixel_color(self, screen_img, x, y):
        """
        Gets the BGR color of a specific pixel.
        
        Returns:
            tuple: (Blue, Green, Red) values (0-255).
        """
        if screen_img is None:
            return None
            
        try:
            # OpenCV images are accessed as array[row, col] -> [y, x]
            # Returns [Blue, Green, Red]
            return screen_img[y, x]
        except IndexError:
            print(f"Error: Coordinates ({x}, {y}) are out of bounds.")
            return None

# Quick test if run directly
if __name__ == "__main__":
    reader = ScreenReader()
    print("Capturing screen...")
    img = reader.capture_screen()
    
    if img is not None:
        print(f"Screen captured! Resolution: {img.shape[1]}x{img.shape[0]}")
        # Save it to verify it works
        cv2.imwrite("debug_screenshot.png", img)
        print("Saved to debug_screenshot.png")
    else:
        print("Capture failed.")