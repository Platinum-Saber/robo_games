from PIL import Image
import numpy as np

# Load the maze image
image_path = 'image.png'
maze_image = Image.open(image_path)
 
# Convert the image to grayscale
gray_maze = maze_image.convert('L')

# Resize for matrix clarity (downscale if necessary)
resized_maze = gray_maze.resize((50, 50))  # Assuming 50x50 grid for simplicity

# Convert to numpy array
maze_array = np.array(resized_maze)

# Threshold the array to create a binary representation
threshold = 128
binary_maze = (maze_array < threshold).astype(int)  # Walls = 1, Paths = 0

for row in binary_maze:
    print(row)