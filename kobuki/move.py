import serial
import time

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
def move_forward(duration=0.5):
    send_command(MOVE_FORWARD, "Moving forward")
    time.sleep(duration)
    send_command(STOP)
    time.sleep(0.1)

def turn_right(duration=0.3):
    send_command(TURN_RIGHT, "Turning right")
    time.sleep(duration)
    send_command(STOP)
    time.sleep(0.1)

def stop():
    send_command(STOP, "Stopping")
    time.sleep(0.1)

def turn_left(duration=0.3):
    send_command(TURN_LEFT, "Turning left")
    time.sleep(duration)
    send_command(STOP)
    time.sleep(0.1)

def move_backward(duration=0.5):
    send_command(MOVE_BACKWARD, "Moving backward")
    time.sleep(duration)
    send_command(STOP)
    time.sleep(0.1)

# Test movement
def test_movement():
    print("Starting movement test...")
    
    # Test forward movement
    print("Testing move_forward (0.5s, ~5 cm)")
    move_forward(0.5)
    time.sleep(1)  # Pause to observe
    
    # Test right turn
    print("Testing turn_right (0.3s)")
    turn_right(0.3)
    time.sleep(1)
    
    # Test stop (should already be stopped, but explicit test)
    print("Testing stop")
    stop()
    time.sleep(1)
    
    # Test left turn
    print("Testing turn_left (0.3s)")
    turn_left(0.3)
    time.sleep(1)
    
    # Test backward movement
    print("Testing move_backward (0.5s, ~5 cm)")
    move_backward(0.5)
    time.sleep(1)
    
    print("Movement test complete!")

if __name__ == "__main__":
    try:
        test_movement()
    except KeyboardInterrupt:
        stop()
        ser.close()
        print("Test interrupted and stopped")
    finally:
        stop()
        ser.close()
        print("Serial connection closed")