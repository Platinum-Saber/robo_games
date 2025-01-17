#from my_supervisor import maze

maze_size = 3

maze = [
    "o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o",
    "|                                               |               |",
    "o   o---o---o---o---o---o---o   o---o   o   o   o   o   o   o   o",
    "|   |                   |   |   |       |   |   |   |   |   |   |",
    "o   o---o   o   o   o   o   o   o---o   o   o   o---o   o   o   o",
    "|   |   |   |   |   |   |   |   |       |   |           |   |   |",
    "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o---o   o",
    "|   |   |   |   |   |   |   |                               |   |",
    "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
    "|   |       |   |   |   |   |   |                           |   |",
    "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
    "|   |   |   |               |   |                           |   |",
    "o   o   o   o   o   o   o   o   o   o---o---o   o---o---o   o   o",
    "|   |   |   |   |   |   |   |   |                           |   |",
    "o   o---o   o   o   o   o   o---o---o---o---o---o---o---o---o   o",
    "|               |   |   |   |       |                       |   |",
    "o   o---o   o   o   o   o   o   o   o---o---o---o---o---o   o   o",
    "|   |   |   |   |   |   |   |       |                           |",
    "o   o   o   o   o   o   o   o   o---o---o---o---o---o---o---o   o",
    "|   |   |   |   |   |   |   |   |                           |   |",
    "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
    "|   |   |   |               |   |                           |   |",
    "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
    "|   |       |   |   |   |   |   |                               |",
    "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
    "|   |   |   |   |   |   |       |                           |   |",
    "o   o   o   o   o   o   o   o   o   o---o---o   o---o---o---o   o",
    "|   |   |   |   |   |   |   |           |   |           |   |   |",
    "o   o---o   o   o   o   o   o   o   o---o   o   o---o   o   o   o",
    "|   |                   |   |   |       |   |   |   |   |   |   |",
    "o   o   o---o---o---o---o---o---o---o---o   o---o   o   o   o   o",
    "|   |                                                           |",
    "o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o",
    "o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o"
]

color_coords = [(7,7,0),(5,0,2),(7,3,2),(8,4,2),(0,3,2)]  #red,yellow,pink,brown,green
walls = []
maze_vals = []

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



robotx,roboty = 0,0
queue = []

def maze_numbering_temp(destination):
    changes_done = False
    if maze_vals[destination[1]][destination[0]] == -1:
        maze_vals[destination[1]][destination[0]] = 0
    
    adj_coords = [(destination[0],destination[1]+1),
                  (destination[0]+1,destination[1]),
                  (destination[0],destination[1]-1),
                  (destination[0]-1,destination[1])]
    for x,y in adj_coords:
        print(x,y)
        #print(maze_vals[x][y])
        if(x<maze_size and x>-1 and y<maze_size and y>-1 and maze_vals[y][x] == -1):
            maze_vals[y][x] = maze_vals[destination[1]][destination[0]] + 1
            print(maze_vals[x][y])
            changes_done = True
            maze_numbering((x,y))

    return

def checkwalls(cell):
    wall_string = bin(walls[cell[1]][cell[0]])[2::].zfill(4)
    result = []
    for x in wall_string:
        result.append(int(x))
    return result


def maze_numbering(destination):
    
    maze_vals[destination[1]][destination[0]] = 0
    cur_cell = destination

    while(True):
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
        if(len(queue) == 0):
            return
        else:
            cur_cell = queue.pop(0)
    
    
    
    

setborder()
maze_numbering((0,1))
print(maze_vals)