from controller import Robot
from controller import Camera

robot = Robot()
timestep = int(robot.getBasicTimeStep())
camera = robot.getDevice('camera')
camera.enable(timestep)

def getColor(image, x, y):
    colors = {
        "Red" : {
            "R" : 255,
            "G" : 0,
            "B" : 0
        },
        "Brown" : {
            # "R" : 165,
            # "G" : 105,
            # "B" : 30  
            "R" : 200,
            "G" : 150,
            "B" : 50
        },
        "Green" : {
            "R" : 0,
            "G" : 255,
            "B" : 0
        },
        "Yellow" : {
            "R" : 255,
            "G" : 255,
            "B" : 0
        },
        "Pink" : {
            "R" : 255,
            "G" : 0,
            "B" : 255
        },
        "White" : {
            "R" : 255,
            "G" : 255,
            "B" : 255
        },
        "Black" : {
            "R" : 0,
            "G" : 0,
            "B" : 0
        }
    }

    # Retrieve the camera image
    image = camera.getImage()
    # Process the image data
    # Example: Get the RGB value of a specific pixel
    width = camera.getWidth()
    height = camera.getHeight()
    red, green, blue = 0, 0, 0

    for i in range(-4, 5):
        for j in range(-4, 5):
            red += camera.imageGetRed(image, width, i+width//2, j+height//2)
            #print(f"red_pixel is {camera.imageGetRed(image, width, i+width//2, j+height//2)}")
            green += camera.imageGetGreen(image, width, i+width//2, j+height//2)
            #print(f"green_pixel is {camera.imageGetGreen(image, width, i+width//2, j+height//2)}")
            blue += camera.imageGetBlue(image, width, i+width//2, j+height//2)
            #print(f"blue_pixel is {camera.imageGetBlue(image, width, i+width//2, j+height//2)}")

    red_avg = red/81
    green_avg = green/81
    blue_avg = blue/81

    for key, value in colors.items():
        if abs(red_avg - value["R"]) < 40  and abs(green_avg - value["G"]) < 40 and abs(blue_avg - value["B"]) < 40:
            print(f"Color is {key}")
            return key
