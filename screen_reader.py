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
        Locates a template image inside the screen image.
        Returns (x, y) center coordinates or None.
        """
        if screen_img is None:
            return None

        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"Error: Could not load template file: {template_path}")
            return None

        h, w = template.shape[:2]
        result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            center_x = int(max_loc[0] + w / 2)
            center_y = int(max_loc[1] + h / 2)
            return (center_x, center_y)
        
        return None

    def get_board_state(self, screen_img, grid_config, assets):
        """
        Slices the screen into 16 tiles and identifies the number in each.
        
        Args:
            screen_img: The full screen image.
            grid_config: Dictionary with 'start_x', 'start_y', 'step'.
            assets: Dictionary mapping numbers to their image paths (e.g., {2: "assets/2.png"}).
            
        Returns:
            A 4x4 list of lists representing the board (0 for empty).
        """
        if screen_img is None:
            return [[0]*4 for _ in range(4)]

        board = []
        
        # Dimensions for cropping a single tile (approximate, slightly smaller than full tile to avoid borders)
        # You might need to adjust this size based on your resolution
        CROP_SIZE = 80 
        OFFSET = CROP_SIZE // 2 # To center the crop

        start_x = grid_config['start_x']
        start_y = grid_config['start_y']
        step = grid_config['step']

        for row in range(4):
            row_data = []
            for col in range(4):
                # Calculate the center of the current tile
                center_x = start_x + (col * step)
                center_y = start_y + (row * step)
                
                # Crop a small square around the center
                y1 = int(center_y - OFFSET)
                y2 = int(center_y + OFFSET)
                x1 = int(center_x - OFFSET)
                x2 = int(center_x + OFFSET)
                
                # Safety check to ensure we don't crop outside image
                if y1 < 0 or x1 < 0:
                    row_data.append(0)
                    continue

                tile_img = screen_img[y1:y2, x1:x2]
                
                # Identify the number
                detected_num = 0
                best_match = 0
                
                # Check this tile against all known number assets
                for num, path in assets.items():
                    # We reuse find_template logic but on the tiny tile image
                    # We use a lower threshold because we are matching "close enough"
                    tmpl = cv2.imread(path, cv2.IMREAD_COLOR)
                    if tmpl is None: continue
                    
                    # Resize template if necessary or just match
                    # Ideally, your assets are already cropped to size.
                    res = cv2.matchTemplate(tile_img, tmpl, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(res)
                    
                    if max_val > 0.8 and max_val > best_match:
                        best_match = max_val
                        detected_num = num
                
                row_data.append(detected_num)
            board.append(row_data)
        
        return board

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