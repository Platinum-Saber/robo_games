import math
from controller import Robot
from controller import Camera

suhan = Robot()

timestep = int(suhan.getBasicTimeStep())

camera = Camera('camera')
camera.enable(timestep)

R = G = B = (0, 0, 0)

def delay(seconds):
    startTime = suhan.getTime()
    while suhan.getTime() - startTime < seconds:
        suhan.step(timestep)

def getUnitVector(vector):
    magnitude = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2) + math.pow(vector[2], 2))
    return (vector[0] / magnitude, vector[1] / magnitude, vector[2] / magnitude)

def estimateColor2(rawColorVector):
    redEstimate = rawColorVector[0] * R[0] + rawColorVector[1] * R[1] + rawColorVector[2] * R[2]
    greenEstimate = rawColorVector[0] * G[0] + rawColorVector[1] * G[1] + rawColorVector[2] * G[2]
    blueEstimate = rawColorVector[0] * B[0] + rawColorVector[1] * B[1] + rawColorVector[2] * B[2]
    
    return (redEstimate, greenEstimate, blueEstimate)

def estimateColor1(rawColorVector):
    redDifference = (rawColorVector[0] - R[0], rawColorVector[1] - R[1], rawColorVector[2] - R[2])
    greenDifference = (rawColorVector[0] - G[0], rawColorVector[1] - G[1], rawColorVector[2] - G[2])
    blueDifference = (rawColorVector[0] - B[0], rawColorVector[1] - B[1], rawColorVector[2] - B[2])
    
    redDistance = math.sqrt(math.pow(redDifference[0], 2) + math.pow(redDifference[1], 2) + math.pow(redDifference[2], 2))
    greenDistance = math.sqrt(math.pow(greenDifference[0], 2) + math.pow(greenDifference[1], 2) + math.pow(greenDifference[2], 2))
    blueDistance = math.sqrt(math.pow(blueDifference[0], 2) + math.pow(blueDifference[1], 2) + math.pow(blueDifference[2], 2))

    redEstimate = 255 - redDistance
    greenEstimate = 255 - greenDistance
    blueEstimate = 255 - blueDistance

    return (redEstimate, greenEstimate, blueEstimate)

def calibrateColor():
    print ("PLACE ON RED")
    delay(3)
    print ("STARTING CALIBRATION OF RED")
    R = getAverage()
    print (R)
    print ("DONE CALIBRATING RED")

    delay(2)

    print ("PLACE ON GREEN")
    delay(3)
    print ("STARTING CALIBRATION OF GREEN")
    G = getAverage()
    print (G)
    print ("DONE CALIBRATING GREEN")

    delay(2)

    print ("PLACE ON BLUE")
    delay(3)
    print ("STARTING CALIBRATION OF BLUE")
    B = getAverage()
    print (B)
    print ("DONE CALIBRATING BLUE")

def getAverage():
    r = g = b = 0

    image = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()

    centerX = width // 2
    centerY = height // 2
    
    for x in range(-4, 5):
        for y in range(-4, 5):
            r += camera.imageGetRed(image, width, centerX + x, centerY + y)
            g += camera.imageGetGreen(image, width, centerX + x, centerY + y)
            b += camera.imageGetBlue(image, width, centerX + x, centerY + y)

    return (r / 81, g / 81, b / 81)

calibrateColor()

while (suhan.step(timestep) != -1):
    pass