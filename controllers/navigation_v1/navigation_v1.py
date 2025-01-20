from drive import *
from floodfill import *
from camera import * 


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
camera_1 = robot.getDevice('camera')
camera_1.enable(timestep) 

#for colour in color_coords:
maze_numbering((7,2))
printmaze()
while(maze_vals[robot_coords[1]][robot_coords[0]] != 0):
    next_dir = find_dir((robot_coords[0],robot_coords[1]))
    turn_calc = robot_coords[2] - next_dir
    if(turn_calc == 0):
        result = move(f)
    elif(turn_calc == 1):
        move(l)
        result = move(f)
    if(turn_calc == -1):
        move(r)
        result = move(f)
    elif(abs(turn_calc) == 2):
        move(b)
    
    if(result != 0):
        move(b,result)
        result = 0
    
    printmaze()
    getColor(camera_1)
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