import serial
import time

# Define the serial port and baud rate
SERIAL_PORT = "/dev/ttyUSB0"  # Replace with the correct serial port
BAUD_RATE = 115200

# Kobuki commands
MOVE_FORWARD = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x64, 0x00, 0x00, 0x00, 0x00, 0x10, 0x0D])  # Move forward
TURN_RIGHT = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x00, 0x00, 0x64, 0x00, 0x00, 0x6E, 0x19])
STOP = bytes([0xAA, 0x55, 0x06, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x19])  # Stop

# Open the serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Kobuki on {SERIAL_PORT}")
except Exception as e:
    print(f"Failed to connect to Kobuki: {e}")
    exit(1)

# Function to send a command to the Kobuki
def send_command(command, description):
    try:
        ser.write(command)
        print(f"Sent command: {description}")
    except Exception as e:
        print(f"Failed to send command: {e}")

# Move forward
send_command(MOVE_FORWARD, "Moving forward")
time.sleep(5)  # Move forward for 5 seconds

# Turn right
send_command(TURN_RIGHT, "Turning right")
time.sleep(2)  # Turn right for 2 seconds

# Stop the robot
send_command(STOP, "Stopping")

# Close the serial connection
ser.close()
print("Serial connection closed")