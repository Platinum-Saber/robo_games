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
openMaze.append([1] + [0, 0] * mazeSize)
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
    
    if (openMaze[openMazeY][openMazeX - 1] == 0) and (manhattanDistanceMatrix[currentY][currentX - 1] == currentManhattanDistance - 1):
        return ((currentX - 1, currentY))
    if (openMaze[openMazeY][openMazeX + 1] == 0) and (manhattanDistanceMatrix[currentY][currentX + 1] == currentManhattanDistance - 1):
        return ((currentX + 1, currentY))
    if (openMaze[openMazeY - 1][openMazeX] == 0) and (manhattanDistanceMatrix[currentY - 1][currentX] == currentManhattanDistance - 1):
        return ((currentX, currentY - 1))
    if (openMaze[openMazeY + 1][openMazeX] == 0) and (manhattanDistanceMatrix[currentY + 1][currentX] == currentManhattanDistance - 1):
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

def turn(fromDirection, toDirection):
    if fromDirection == toDirection:
        print ("NO TURN NEEDED")
    elif toDirection == (fromDirection + 1) % 4:
        print ("TURN RIGHT ONCE")
    elif toDirection == (fromDirection - 1) % 4:
        print ("TURN LEFT ONCE")
    elif toDirection == (fromDirection + 2) % 4:
        print ("TURN RIGHT/LEFT TWICE")
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

fromCell = (0, 9)
destination = (3, 4)
direction = N

while True:
    currentX, currentY = fromCell
    openMaze[2 * currentY + 1][2 * currentX + 1] = 9
    if (fromCell == destination):
        print ("REACHED.")
        break
    toCell = nextCell(fromCell, destination)
    print ("NOW IN", fromCell, "TRYING TO GO TO", toCell)
    toDirection = getCellDirection(fromCell, toCell)
    # print ("TRYING TO GO TO", toCell, ", toDirection", toDirection)
    turn(direction, toDirection)
    direction = toDirection
    
    distanceMoved = 0
    
    while distanceMoved < 0.25:
        print ("MOVING FORWARD")
        # keep updating distance with encoders
        
        wallCoords = getWallCoords(fromCell, direction)
        # the following simulates reading IR sensors
        irSensorReading = actualMaze[wallCoords[1][1]][wallCoords[1][0]]
        
        if irSensorReading != " ": # there is a wall.
            # update openMaze
            print ("WALL FOUND")
            openMaze[wallCoords[0][1]][wallCoords[0][0]] = 1
            # reverse. basically move backwards the same distance that would have been moved forward at this point.
            print ("REVERSED")
            # do not update fromcell because are still there.
            break
        else:
            # this is only needed to simulate the encoder readings here. otherwise this would be updated within the loop and is not necessary
            distanceMoved = 0.26
    else:
        # we successfully moved to the next cell
        fromCell = toCell
        print ("MOVED TO ", toCell)
