#from my_supervisor import maze

"""
wall types and values
    up    = 8
    right = 4
    down  = 2
    left  = 1
all coordinates must be given as tuples (x,y)

"""

maze_size = 10

color_coords = [(7,7,0),(5,0,2),(7,3,2),(8,4,2),(0,3,2)]  #red,yellow,pink,brown,green
walls = []
maze_vals = []


queue = []
neighbours = []

for x in range (maze_size):
    maze_vals.append([])
    walls.append([])
    for y in range(maze_size):
        maze_vals[x].append(-1)
        walls[x].append(0)

def setborder():
    for i in range(maze_size):
        walls[maze_size-1][i] += 8      #1000 in bin
        walls[0][i] += 2                #0010 in bin
    for i in range(maze_size):
        walls[i][0] += 1                #0001 in bin
        walls[i][maze_size-1] += 4      #0100 in bin



def checkwalls(cell):
    wall_string = bin(walls[cell[1]][cell[0]])[2::].zfill(4)
    result = []
    for x in wall_string:
        result.append(int(x))
    return result


def maze_numbering(destination):
    
    maze_vals[destination[1]][destination[0]] = 0
    queue.append(destination)

    while(len(queue) > 0):
        cur_cell = queue.pop(0)
        cur_cell_value = maze_vals[cur_cell[1]][cur_cell[0]]
        wall_pos = checkwalls((cur_cell))

        adj_coords = [(cur_cell[0],cur_cell[1]+1),
                    (cur_cell[0]+1,cur_cell[1]),
                    (cur_cell[0],cur_cell[1]-1),
                    (cur_cell[0]-1,cur_cell[1])]
        
        for index,(x,y) in enumerate(adj_coords ,start = 0):
            if(x<maze_size and x>-1 and y<maze_size and y>-1 and maze_vals[y][x] == -1):
                #this is an unexplored cell
                if(wall_pos[index] == 0):
                    #no walls in this direction
                    queue.append((x,y))
                    maze_vals[y][x] = cur_cell_value + 1

    return

    
def reroute(cell):
    queue.clear()
    queue.append(cell)

    while(len(queue) > 0):
        neighbours.clear()
        cur_cell = queue.pop(0)
        cur_cell_value = maze_vals[cur_cell[1]][cur_cell[0]]
        wall_pos = checkwalls((cur_cell))

        adj_coords = [(cur_cell[0],cur_cell[1]+1),
                    (cur_cell[0]+1,cur_cell[1]),
                    (cur_cell[0],cur_cell[1]-1),
                    (cur_cell[0]-1,cur_cell[1])]
        
        for index,(x,y) in enumerate(adj_coords ,start = 0):
                if(x<maze_size and x>-1 and y<maze_size and y>-1):
                    #this is inside the maze
                    if(wall_pos[index] == 0):
                        #no walls in this direction
                        neighbours.append((x,y))
        min_neighbour_val = 10000
        for (x,y) in neighbours:
            if(min_neighbour_val > maze_vals[y][x]):
                min_neighbour_val = maze_vals[y][x]
        if(cur_cell_value <= min_neighbour_val):
            maze_vals[cur_cell[1]][cur_cell[0]] = min_neighbour_val + 1
            for i in neighbours:
                queue.append(i)

def addwall(cell,val):
    walls[cell[1]][cell[0]] = walls[cell[1]][cell[0]] | val
    mywalls = checkwalls(cell)
    if(mywalls[0] == 1):
        adjcell = (cell[0],cell[1]+1)   #top cell
        if(adjcell[0]<maze_size and adjcell[0]>-1 and adjcell[1]<maze_size and adjcell[1]>-1):
            walls[adjcell[1]][adjcell[0]] = walls[adjcell[1]][adjcell[0]] | 2
    if(mywalls[1] == 1):
        adjcell = (cell[0]+1,cell[1])   #right cell
        if(adjcell[0]<maze_size and adjcell[0]>-1 and adjcell[1]<maze_size and adjcell[1]>-1):
            walls[adjcell[1]][adjcell[0]] = walls[adjcell[1]][adjcell[0]] | 1
    if(mywalls[2] == 1):
        adjcell = (cell[0],cell[1]-1)   #bottom cell
        if(adjcell[0]<maze_size and adjcell[0]>-1 and adjcell[1]<maze_size and adjcell[1]>-1):
            walls[adjcell[1]][adjcell[0]] = walls[adjcell[1]][adjcell[0]] | 8
    if(mywalls[3] == 1):
        adjcell = (cell[0]-1,cell[1])   #left cell
        if(adjcell[0]<maze_size and adjcell[0]>-1 and adjcell[1]<maze_size and adjcell[1]>-1):
            walls[adjcell[1]][adjcell[0]] = walls[adjcell[1]][adjcell[0]] | 4


def printmaze():
    for y in range(maze_size-1, -1,-1):
        for x in range(maze_size):
            mywalls = checkwalls((x,y))
            if(mywalls[0] == 1):
                print(" _  ",end="")
            else:
                print("    ",end="")
        print()
        for x in range(maze_size):
            mywalls = checkwalls((x,y))
            if(mywalls[3] == 1):
                print("|",end="")
            else:
                print(" ",end="")
            print(maze_vals[y][x],end = " ")
            if(mywalls[1] == 1):
                print("|",end="")
            else:
                print(" ",end="")
        print()
        for x in range(maze_size):
            mywalls = checkwalls((x,y))
            if(mywalls[2] == 1):
                print(" _  ",end="")
            else:
                print("    ",end="")
        print()
    print("=========================================================")


def find_dir(cur_cell):
    wall_pos = checkwalls((cur_cell))
    adj_coords = [(cur_cell[0],cur_cell[1]+1),
                    (cur_cell[0]+1,cur_cell[1]),
                    (cur_cell[0],cur_cell[1]-1),
                    (cur_cell[0]-1,cur_cell[1])]
    
    cur_cell_value = maze_vals[cur_cell[1]][cur_cell[0]]

    for index,(x,y) in enumerate(adj_coords ,start = 0):
            if(x<maze_size and x>-1 and y<maze_size and y>-1):
                #this is inside the maze
                if(wall_pos[index] == 0):
                    #no walls in this direction
                    adjcell_val = maze_vals[y][x]
                    if(adjcell_val < cur_cell_value):
                        direction = index
    return(direction)
    #match direction:
    #    case 0:
    #        return 'up'
    #    case 1:
    #        return 'right'
    #    case 2:
    #        return 'down'
    #    case 3:
    #        return 'left'

def setsize(num):
    global maze_size
    maze_size = num


#setsize(5)
#print(maze_size)
#setborder()
#maze_numbering((1,1))
#printmaze()

"""
use printmaze() to print the current configuration of the maze
use addwall((cell),val) to add a wall when the robot detects it. cell is the (x,y) of the cell the robot is on. the val is the 
decimal value corresponding to the walls on all 4 sides
in the beginning use maze_numbering(destiation) to give where the robot must go. the destination is the place where the color
is placed aka the coordinats in the color_coords list
during traverse, if the robot discovers a new wall we need to re correct the numbering and for that use reroute(cell) after 
adding the discoverd walls. Here the cell is the (x,y) of the robot
"""
#addwall((1,2),6)
#addwall((2,2),3)
#reroute((2,2))
#printmaze()
#print(find_dir((4,4)))
