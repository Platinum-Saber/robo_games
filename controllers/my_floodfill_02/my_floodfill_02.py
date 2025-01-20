import math
from camera import *
from controller import Robot
from controller import Camera

# start = (input("Enter the starting cell X coord: "), input("Enter the starting cell Y coord: "))
start = (4, 5)
red_cell = (7, 3)
yellow_cell = (5, 9)
pink_cell = (7, 7)
brown_cell = (8, 6)
green_cell = (2, 6)

dest_coords = [start, red_cell, yellow_cell, pink_cell, brown_cell, green_cell]



# class PIDController:
#     def __init__(self, K_P, K_I, K_D):
#         self.K_P = K_P
#         self.K_I = K_I
#         self.K_D = K_D

#         self._prevError = 0
#         self._errorIntegral = 0
    
#     def getPIDValue(self, error):
#         derivative = error - self._prevError
#         integral = self._errorIntegral + error

#         PID = self.K_P * error + self.K_I * integral + self.K_D * derivative

#         self._prevError = error
#         self._errorIntegral = integral

#         return PID

#     def updateConstants(self, K_P, K_I, K_D):
#         self.K_P = K_P
#         self.K_I = K_I
#         self.K_D = K_D

#     def reset():
#         self._prevError = 0
#         self._errorIntegral = 0

actualMaze = []

with open("../maze.txt", "r") as actualMazeFile:
    for line in actualMazeFile:
        actualMaze.append(line.rstrip("\n"))

mazeSize = 10

openMaze = []

openMaze.append([1] + [1, 1] * mazeSize)
for i in range(mazeSize - 1):
    openMaze.append([1] + [0, 0] * (mazeSize - 1) + [0, 1])
    openMaze.append([1] + [0, 1] * mazeSize)
openMaze.append([1] + [0, 0] * (mazeSize - 1) + [0, 1])
# openMaze.append([1] + [0, 0] * mazeSize)
openMaze.append([1] + [1, 1] * mazeSize)

def floodfill(destination):
    destinationX, destinationY = destination
    queue = [destination]
    manhattanDistanceMatrix = [[-1 for i in range(mazeSize)] for j in range(mazeSize)]
    manhattanDistanceMatrix[destinationY][destinationX] = 0
    
    while len(queue) > 0:
        currentX, currentY = queue.pop(0)
        currentManhattanDistance = manhattanDistanceMatrix[currentY][currentX]
        
        openMazeX, openMazeY = 2 * currentX + 1, 2 * currentY + 1
        
        if (currentX > 0) and (openMaze[openMazeY][openMazeX - 1] == 0) and (manhattanDistanceMatrix[currentY][currentX - 1] == -1):
            queue.append((currentX - 1, currentY))
            manhattanDistanceMatrix[currentY][currentX - 1] = currentManhattanDistance + 1
        if (currentX < mazeSize - 1) and (openMaze[openMazeY][openMazeX + 1] == 0) and (manhattanDistanceMatrix[currentY][currentX + 1] == -1):
            queue.append((currentX + 1, currentY))
            manhattanDistanceMatrix[currentY][currentX + 1] = currentManhattanDistance + 1
        if (currentY > 0) and (openMaze[openMazeY - 1][openMazeX] == 0) and (manhattanDistanceMatrix[currentY - 1][currentX] == -1):
            queue.append((currentX, currentY - 1))
            manhattanDistanceMatrix[currentY - 1][currentX] = currentManhattanDistance + 1
        if (currentY < mazeSize - 1) and (openMaze[openMazeY + 1][openMazeX] == 0) and (manhattanDistanceMatrix[currentY + 1][currentX] == -1):
            queue.append((currentX, currentY + 1))
            manhattanDistanceMatrix[currentY + 1][currentX] = currentManhattanDistance + 1
            
    return manhattanDistanceMatrix

def nextCell(currentCell, destination):
    # printMatrix(openMaze)
    currentX, currentY = currentCell
    openMazeX, openMazeY = 2 * currentX + 1, 2 * currentY + 1
    
    manhattanDistanceMatrix = floodfill(destination)
    currentManhattanDistance = manhattanDistanceMatrix[currentY][currentX]
    print ("CURRENT MANHATTAN DISTANCE", currentManhattanDistance)
    print("*******************************************")
    
    if (openMaze[openMazeY][openMazeX - 1] == 0) and (currentX > 0) and (manhattanDistanceMatrix[currentY][currentX - 1] == currentManhattanDistance - 1):
        return ((currentX - 1, currentY))
    if (openMaze[openMazeY][openMazeX + 1] == 0) and (currentX < mazeSize - 1) and (manhattanDistanceMatrix[currentY][currentX + 1] == currentManhattanDistance - 1):
        return ((currentX + 1, currentY))
    if (openMaze[openMazeY - 1][openMazeX] == 0) and (currentY > 0) and (manhattanDistanceMatrix[currentY - 1][currentX] == currentManhattanDistance - 1):
        return ((currentX, currentY - 1))
    if (openMaze[openMazeY + 1][openMazeX] == 0) and (currentY < mazeSize - 1)  and (manhattanDistanceMatrix[currentY + 1][currentX] == currentManhattanDistance - 1):
        return ((currentX, currentY + 1))

def printMatrix(matrix):
    for row in matrix:
        line = ""
        for num in row:
            line += str(num).ljust(2) + " "
        print (line)

N = 0
E = 1
S = 2
W = 3

suhan = Robot()

timestep = int(suhan.getBasicTimeStep())

leftWheel = suhan.getDevice("left wheel motor")
rightWheel = suhan.getDevice("right wheel motor")

leftWheel.setPosition(float('Inf'))
rightWheel.setPosition(float('Inf'))
leftWheel.setVelocity(0)
rightWheel.setVelocity(0)

leftEncoder = suhan.getDevice("left wheel sensor")
rightEncoder = suhan.getDevice("right wheel sensor")

leftEncoder.enable(timestep)
rightEncoder.enable(timestep)

leftDistanceSensor = suhan.getDevice("ps7")
rightDistanceSensor = suhan.getDevice("ps0")
leftDistanceSensor.enable(timestep)
rightDistanceSensor.enable(timestep)

imu = suhan.getDevice("inertial unit")
imu.enable(timestep)

axleLength = 52 # mm
wheelRadius = 20.5 # mm
maxSpeed = 6.28
forwardSpeed = 1
turnSpeed = 0.5

# turnPIDController = PIDController(1, 0, 0)

def setSpeeds(left, right):
    if left > 0:
        left = min(maxSpeed, left)
    else:
        left = max(-maxSpeed, left)
    if right > 0:
        right = min(maxSpeed, right)
    else:
        right = max(-maxSpeed, right)
    
    leftWheel.setVelocity(left)
    rightWheel.setVelocity(right)

def turn(fromDirection, toDirection):
    wheelTurnAngle = 0

    if fromDirection == toDirection:
        print ("NO TURN NEEDED")
        return
    elif toDirection == (fromDirection + 1) % 4:
        print ("TURN RIGHT ONCE")
        setSpeeds(turnSpeed, -turnSpeed)
        wheelTurnAngle = 1.77 # (math.pi / 2) # * (axleLength / (2 * wheelRadius))
    elif toDirection == (fromDirection - 1) % 4:
        print ("TURN LEFT ONCE")
        setSpeeds(-turnSpeed, turnSpeed)
        wheelTurnAngle = -1.77 # -(math.pi / 2) # * (axleLength / (2 * wheelRadius))
    elif toDirection == (fromDirection + 2) % 4:
        print ("TURN RIGHT/LEFT TWICE")
        setSpeeds(turnSpeed, -turnSpeed)
        wheelTurnAngle = 1.77 * 2 # * (axleLength / (2 * wheelRadius))

    pose[2] = 0
    while math.pow(pose[2] - wheelTurnAngle, 2) > 0.0001:
        stepAndUpdatePose()
        #print (pose[2] - wheelTurnAngle)
    setSpeeds(0, 0)
    # print ("NOW VEHICLE IS FACING THE SAME DIRECTION AS THE REQUIRED DIRECTION. CAN JUST MOVE FORWARD TO GO TO REQUIRED LOCATION.")

def getCellDirection(currentCell, nextCell):
    currentX, currentY = currentCell
    nextX, nextY = nextCell
    
    if (nextX == currentX - 1) and (nextY == currentY):
        return W
    elif (nextX == currentX + 1) and (nextY == currentY):
        return E
    elif (nextY == currentY - 1) and (nextX == currentX):
        return N
    elif (nextY == currentY + 1) and (nextX == currentX):
        return S
        
def getWallCoords(currentCell, direction):
    currentX, currentY = currentCell
    openMazeX, openMazeY = 2 * currentX + 1, 2 * currentY + 1
    actualMazeX, actualMazeY = 4 * currentX + 2, 2 * currentY + 1
    
    if direction == N:
        return [(openMazeX, openMazeY - 1), (actualMazeX, actualMazeY - 1)]
    elif direction == E:
        return [(openMazeX + 1, openMazeY), (actualMazeX + 2, actualMazeY)]
    elif direction == S:
        return [(openMazeX, openMazeY + 1), (actualMazeX, actualMazeY + 1)]
    elif direction == W:
        return [(openMazeX - 1, openMazeY), (actualMazeX - 2, actualMazeY)]


direction = N

pose = [0, 0, 0]

def stepAndUpdatePose():
    dt = timestep / 1000 # seconds
    
    leftEncoderStartAngle = leftEncoder.getValue()
    rightEncoderStartAngle = rightEncoder.getValue()
    
    returnValue = suhan.step(timestep)

    leftEncoderEndAngle = leftEncoder.getValue()
    rightEncoderEndAngle = rightEncoder.getValue()

    leftWheelTurnAngle = leftEncoderEndAngle - leftEncoderStartAngle
    rightWheelTurnAngle = rightEncoderEndAngle - rightEncoderStartAngle
    
    leftWheelAngularVelocity = leftWheelTurnAngle / dt
    rightWheelAngularVelocity = rightWheelTurnAngle / dt

    leftWheelLinearVelocity = wheelRadius * leftWheelAngularVelocity ## mm/s
    rightWheelLinearVelocity = wheelRadius * rightWheelAngularVelocity

    robotLinearVelocity = (leftWheelLinearVelocity + rightWheelLinearVelocity) / 2 # mm/s
    robotAngularVelocity = (leftWheelLinearVelocity - rightWheelLinearVelocity) / axleLength ## rad/s

    robotTurnAngle = robotAngularVelocity * dt

    pose[0] += robotLinearVelocity * dt * math.cos(robotTurnAngle)
    pose[1] += robotLinearVelocity * dt * math.sin(robotTurnAngle)
    pose[2] += robotTurnAngle

    return returnValue

linear_dist = 256

camera_1 = suhan.getDevice('camera')
camera_1.enable(timestep)


for dest in range(len(dest_coords)-1):
    fromCell = dest_coords[dest]
    destination = dest_coords[dest+1]
    
    while stepAndUpdatePose() != -1:
        currentX, currentY = fromCell
        getColor(camera_1)
        actualMazeX, actualMazeY = 4 * currentX + 2, 2 * currentY + 1
        string = actualMaze[actualMazeY]
        actualMaze[actualMazeY] = string[:actualMazeX] + "X" + string[actualMazeX + 1:]
        if (fromCell == destination):
            print ("REACHED.")
            for row in actualMaze:
                print (row)
            printMatrix(openMaze)
            print("====================================")
            setSpeeds(0, 0)
            stepAndUpdatePose()
            break
        toCell = nextCell(fromCell, destination)
        print ("NOW IN", fromCell, "TRYING TO GO TO", toCell)
        toDirection = getCellDirection(fromCell, toCell)
        turn(direction, toDirection)
        direction = toDirection

        # print(imu.getRollPitchYaw())

        distanceMoved = 0
        startAngle = leftEncoder.getValue()
        setSpeeds(forwardSpeed, forwardSpeed)

        pose = [0, 0, 0]
        
        while pose[0] < linear_dist: # mm
            #print (pose)
            # print ("MOVING FORWARD")
            # keep updating distance with encoders
            distanceMoved = (leftEncoder.getValue() - startAngle) * wheelRadius
         
            
            wallCoords = getWallCoords(fromCell, direction)
            # the following simulates reading IR sensors

            irSensorReading = leftDistanceSensor.getValue()
            
            if irSensorReading > 120: # there is a wall.
                # update openMaze
                print ("WALL FOUND")
                openMaze[wallCoords[0][1]][wallCoords[0][0]] = 1
                for row in actualMaze:
                    print (row)
                printMatrix(openMaze)
                print("====================================")
                # reverse. basically move backwards the same distance that would have been moved forward at this point.
                setSpeeds(-forwardSpeed, -forwardSpeed)
                while pose[0] >= 0.001:
                    stepAndUpdatePose()
                setSpeeds(0, 0)
                print ("REVERSED")
                # do not update fromcell because are still there.
                break
            
            stepAndUpdatePose()

        else:
            # we successfully moved to the next cell
            fromCell = toCell
            print ("MOVED TO ", toCell)

# Greens-new 0.625, 1.125, 0.05
# Greens-old 0.1275, 0.875, 0.05