import cv2
import numpy as np

# HSV color ranges (initial values from your code)
color_ranges = {
    "Red": [
        [(0, 120, 70), (10, 255, 255)],      # Lower range for red
        [(170, 120, 70), (180, 255, 255)]     # Upper range for red
    ],
    "Green": [(40, 70, 70), (80, 255, 255)],
    "Blue": [(100, 150, 70), (140, 255, 255)],
    "Yellow": [(20, 100, 70), (40, 255, 255)],
}

# Detect colored objects
def detect_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detected_objects = []

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
                detected_objects.append((color, x, y, w, h))

    return detected_objects

# Test color detection
def test_color_calibration():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return

    FRAME_WIDTH = 640
    print("Starting color calibration test...")
    print("Place colored objects (Red, Green, Blue, Yellow) in front of the camera.")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        frame = cv2.resize(frame, (FRAME_WIDTH, 480))
        objects = detect_colors(frame)

        # Visualize detected objects
        for color, x, y, w, h in objects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.putText(frame, f"{color} ({w}x{h})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            print(f"Detected {color} at ({x}, {y}), size: {w}x{h}")

        cv2.imshow("Color Calibration", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Color calibration test complete!")

if __name__ == "__main__":
    test_color_calibration()