import time
import random
import controller
from screen_reader import ScreenReader

# --- CONFIGURATION ---
# The path to the small image you cropped in Step 1
ASSET_START_BUTTON = "assets/start_button.png"

MOVES = ["up", "down", "left", "right"]

GRID_CONFIG = {
    'start_x': 252,   # Center X of the top-left tile
    'start_y': 998,   # Center Y of the top-left tile
    'step': 191       # Distance between tile centers
}

TILE_ASSETS = {
    0   : "assets/tile_0.png",
    2   : "assets/tile_2.png",
    4   : "assets/tile_4.png",
    8   : "assets/tile_8.png",
    16  : "assets/tile_16.png",
    32  : "assets/tile_32.png",
    64  : "assets/tile_64.png",
    128 : "assets/tile_128.png",
    256 : "assets/tile_256.png",
    512 : "assets/tile_512.png",
    1024: "assets/tile_1024.png",
    2048: "assets/tile_2048.png"
}

def main():
    print("Bot started...")
    
    # Check if phone is connected
    devices = controller.checkConnections()
    if not devices:
        print("No device found! Connect your phone.")
        return
    print(f"Connected to {devices[0]}")

    vision = ScreenReader()

    try:
        while True:
            # 1. CAPTURE: Get the current screen (Vision)
            # We use the stream method because it's faster than saving files
            screen = controller.get_screen_stream()
            
            if screen is None:
                print("Failed to capture screen. Retrying...")
                time.sleep(1)
                continue

            # 2. ANALYZE: Look for the Start Button
            # The '0.8' is confidence. 80% match required.
            button_pos = vision.find_template(screen, ASSET_START_BUTTON, threshold=0.8)
            
            if button_pos:
                # button_pos is a tuple: (x, y) coordinates of the center of the button
                print(f"I see the Start Button at {button_pos}! Tapping it now.")
                
                # 3. ACTION: Physical Tap (Hands)
                controller.tap(button_pos[0], button_pos[1])
                
                # Wait a bit so we don't spam-click it while the animation plays
                time.sleep(2) 
                
                # In the future: Switch to "Game Solver" logic here
                print("Game started! Waiting for next instructions...")
            
            else:
                #print("I don't see the Start Button. Scanning...")

                print("Reading board...")
                board = vision.get_board_state(screen, GRID_CONFIG, TILE_ASSETS)
                
                # Print board nicely to console
                print("\nCurrent Board:")
                for row in board:
                    print(row)

                time.sleep(4)
    
                swipe()

            # Add a small delay to save CPU power
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nBot stopped by user.")

def swipe():
    random_move = random.choice(MOVES)
    print(f"Swiping {random_move}")
    controller.swipe_direction(random_move)
    

if __name__ == "__main__":
    main()