import serial
import time
import cv2
import numpy as np

# Serial port configuration
SERIAL_PORT = "/dev/ttyUSB0"  # Replace with your robot's serial port
BAUD_RATE = 115200

# Updated Kobuki commands
MOVE_FORWARD = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x64, 0x00, 0x00, 0x00, 0x00, 0x10, 0x0D])
TURN_LEFT = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x64, 0x00, 0x01, 0x00, 0x00, 0x10, 0x0D])  # Spin right
STOP = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x19])
TURN_RIGHT = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x64, 0x00, 0xFF, 0xFF, 0x00, 0x10, 0x0D])  # Spin left
MOVE_BACKWARD = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x9C, 0xFF, 0x00, 0x00, 0x00, 0x10, 0x0D])

# Open serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Kobuki on {SERIAL_PORT}")
except Exception as e:
    print(f"Failed to connect to Kobuki: {e}")
    exit(1)

# Function to send commands
def send_command(command, description=""):
    try:
        ser.write(command)
        if description:
            print(f"Sent command: {description}")
    except Exception as e:
        print(f"Failed to send command: {e}")

# Movement control functions
def move_forward(duration=3):
    send_command(MOVE_FORWARD, "Moving forward")
    time.sleep(duration)
    #send_command(STOP)
    time.sleep(0.1)

def turn_right(duration=0.2):
    send_command(TURN_RIGHT, "Turning right")
    time.sleep(duration)
    send_command(STOP)
    time.sleep(0.1)

def stop():
    send_command(STOP, "Stopping")
    time.sleep(0.1)

def turn_left(duration=0.2):
    send_command(TURN_LEFT, "Turning left")
    time.sleep(duration)
    send_command(STOP)
    time.sleep(0.1)

def move_backward(duration=3):
    send_command(MOVE_BACKWARD, "Moving backward")
    time.sleep(duration)
    #send_command(STOP)
    time.sleep(0.1)

# HSV color ranges
color_ranges = {
    "Yellow": [(20, 100, 70), (40, 255, 255)],
    "Red": [
        [(0, 120, 70), (10, 255, 255)],      # Lower range for red
        [(170, 120, 70), (180, 255, 255)]     # Upper range for red
    ],
    "Green": [(40, 70, 70), (80, 255, 255)],
    "Blue": [(100, 150, 70), (140, 255, 255)]
}

# Detect colored objects and classify as box (cube) or tile (rectangle)
def detect_objects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    boxes = []
    tiles = []

    for color, ranges in color_ranges.items():
        if color == "Red":
            lower1, upper1 = ranges[0]
            lower2, upper2 = ranges[1]
            mask1 = cv2.inRange(hsv, np.array(lower1), np.array(upper1))
            mask2 = cv2.inRange(hsv, np.array(lower2), np.array(upper2))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower, upper = ranges
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filter noise
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                
                # Classify based on aspect ratio
                if 0.9 <= aspect_ratio <= 1.1:  # Cube-like (box)
                    boxes.append((color, x, y, w, h))
                elif aspect_ratio > 1.5 and y > frame.shape[0] * 0.6:  # Wide rectangle near bottom (tile)
                    tiles.append((color, x, y, w, h))

    return boxes, tiles

# Center and approach an object
def center_and_approach(frame_width, target_color, objects, target_size):
    frame_center = frame_width // 2
    CENTER_TOLERANCE = 50
    target_object = None

    for color, x, y, w, h in objects:
        if color == target_color:
            target_object = (color, x, y, w, h)
            break

    if target_object:
        color, x, y, w, h = target_object
        object_center = x + w // 2

        # Center the object
        if abs(object_center - frame_center) > CENTER_TOLERANCE:
            if object_center < frame_center:
                turn_left(0.1)
            else:
                turn_right(0.1)
            return False

        # Approach if not close enough
        if w < target_size:
            move_forward(0.2)  # Small steps (2 cm)
            return False

        # Reached target
        stop()
        time.sleep(0.5)
        return True

    return False  # Object not found

# Main control logic
def control_robot():
    # Camera setup
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return

    # Constants
    FRAME_WIDTH = 640
    FLAP_TARGET_SIZE = 500  # Pixel width when box is within flaps
    TILE_TARGET_SIZE = 600  # Pixel width when aligned with tile
    SEARCH_TIMEOUT = 20     # Seconds before deferring a color
    MAX_PUSH_STEPS = 10     # Max steps to prevent infinite pushing

    # State machine states
    SEARCH_BOX = 0
    APPROACH_BOX = 1
    SEARCH_TILE = 2
    PUSH_TO_TILE = 3
    RETREAT = 4

    # Initialize variables
    colors_to_place = list(color_ranges.keys())
    deferred_colors = []
    placed_colors = []
    current_target = None
    state = SEARCH_BOX
    search_timer = time.time()
    full_scan_completed = False
    push_steps = 0  # Track steps during PUSH_TO_TILE

    try:
        while colors_to_place or deferred_colors:
            ret, frame = cap.read()
            if not ret:
                print("Camera disconnected")
                stop()
                break

            frame = cv2.resize(frame, (FRAME_WIDTH, 480))
            boxes, tiles = detect_objects(frame)

            # Visualizations
            cv2.line(frame, (FRAME_WIDTH//2, 0), (FRAME_WIDTH//2, 480), (0, 255, 0), 1)
            for color, x, y, w, h in boxes:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green for boxes
                cv2.putText(frame, f"Box: {color} ({w})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            for color, x, y, w, h in tiles:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red for tiles
                cv2.putText(frame, f"Tile: {color} ({w})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            # State machine
            if state == SEARCH_BOX:
                if not current_target:
                    if colors_to_place:
                        current_target = colors_to_place.pop(0)
                        search_timer = time.time()
                        full_scan_completed = False
                        print(f"Searching for box: {current_target}")
                    elif deferred_colors:
                        colors_to_place = deferred_colors[:]
                        deferred_colors.clear()
                        continue
                    else:
                        break

                if center_and_approach(FRAME_WIDTH, current_target, boxes, FLAP_TARGET_SIZE):
                    print(f"Box {current_target} within flaps")
                    move_forward(1)  # Small step (5 cm)
                    state = SEARCH_TILE
                elif time.time() - search_timer > SEARCH_TIMEOUT:
                    if not full_scan_completed:
                        turn_right(0.3)
                        if time.time() - search_timer > 2 * SEARCH_TIMEOUT:
                            full_scan_completed = True
                    else:
                        print(f"Box {current_target} not found, deferring")
                        deferred_colors.append(current_target)
                        current_target = None

            elif state == SEARCH_TILE:
                if center_and_approach(FRAME_WIDTH, current_target, tiles, TILE_TARGET_SIZE):
                    print(f"Tile {current_target} reached. Pushing box.")
                    state = PUSH_TO_TILE
                    push_steps = 0  # Reset push counter
                else:
                    turn_right(0.3)

            elif state == PUSH_TO_TILE:
                move_forward(0.5)  # Small step (5 cm)
                push_steps += 1
                
                # Check if tile is still visible
                _, tiles = detect_objects(frame)
                tile_found = any(color == current_target for color, _, _, _, _ in tiles)
                
                # Stop if tile is no longer visible or max steps reached
                if not tile_found or push_steps >= MAX_PUSH_STEPS:
                    print(f"Box {current_target} placed on tile")
                    placed_colors.append(current_target)
                    state = RETREAT
                
            elif state == RETREAT:
                move_backward(0.8)  # Single step back
                time.sleep(0.5)
                current_target = None
                state = SEARCH_BOX
                print("Retreating complete. Scanning for next box.")

            # Display status
            status = f"Target: {current_target} | State: {state}"
            cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"Placed: {', '.join(placed_colors)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"Deferred: {', '.join(deferred_colors)}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Kobuki Controller", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error: {e}")
        stop()
    finally:
        stop()
        cap.release()
        cv2.destroyAllWindows()
        ser.close()
        print("Robot controller shutdown")

if __name__ == "__main__":
    control_robot()