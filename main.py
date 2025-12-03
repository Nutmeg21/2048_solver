import time
import controller  # Your new controller file
from screen_reader import Vision

# Constants
START_BUTTON = "assets/start.png"

def main():
    print("Checking connections...")
    devices = controller.checkConnections()
    if not devices:
        print("No device found! Please connect your phone.")
        return
    print(f"Connected to: {devices[0]}")

    vision = Vision()

    try:
        while True:
            # 1. Get screen (Using the fast memory stream from controller)
            screen = controller.get_screen_stream()
            
            if screen is None:
                print("Failed to get screen")
                time.sleep(1)
                continue

            # 2. Look for Start Button
            btn_pos = vision.find_template(screen, START_BUTTON)
            
            if btn_pos:
                print(f"Start button found at {btn_pos}. Tapping.")
                controller.tap(btn_pos[0], btn_pos[1])
                time.sleep(2) # Wait for app to react
            
            # 3. Example: Check pixel color at 100, 100
            color = vision.get_pixel_color(screen, 100, 100)
            # Logic here...

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    main()