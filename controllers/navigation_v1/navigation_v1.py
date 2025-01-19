from drive import *
from floodfill import *


setsize(10)
setborder()

#addwall((0,0),4)
#addwall((0,1),8)
#addwall((1,1),12)
#addwall((2,0),8)
#addwall((3,0),8)
#addwall((4,0),8)
#addwall((5,0),8)
#addwall((6,0),4)
#addwall((6,1),4)

#for colour in color_coords:
maze_numbering((7,2))
printmaze()
while(maze_vals[robot_coords[1]][robot_coords[0]] != 0):
    next_dir = find_dir((robot_coords[0],robot_coords[1]))
    turn_calc = robot_coords[2] - next_dir
    if(turn_calc == 0):
        move(f)
    elif(turn_calc == 1):
        move(l)
    if(turn_calc == -1):
        move(r)
    elif(abs(turn_calc) == 2):
        move(b)
    printmaze()
    print(robot_coords)


# 
#
#
#
#move(f)
#move(r)
#move(f)
#move(f)
#move(f)
#move(l)
#move(f)
#move(f)
#move(f)
#move(f)
#move(f)
#print(robot_coords)