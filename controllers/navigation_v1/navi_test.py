#from drive import *
from floodfill import *

setsize(10)
setborder()

#addwall((0,0),4)
#addwall((0,2),4)
#addwall((1,1),4)
#addwall((1,1),8)
#addwall((2,0),8)
#addwall((3,0),8)
#addwall((4,0),8)
#addwall((5,0),8)
#addwall((6,0),4)
#addwall((6,1),4)
#addwall((6,2),8)

maze_numbering((8,2))   
printmaze()

robot_coords = [0,0,0]

temp_wall = [[7, 3, 10, 10, 10, 10, 6, 3, 2, 6], [1, 12, 3, 2, 2, 2, 4, 1, 0, 4], [5, 3, 0, 0, 0, 0, 8, 0, 0, 4], [1, 0, 0, 0, 0, 0, 2, 0, 0, 4], [1, 0, 0, 0, 0, 0, 0, 0, 0, 4], [1, 0, 0, 0, 0, 0, 0, 0, 0, 4], [1, 0, 0, 0, 0, 0, 0, 0, 0, 4], [1, 0, 0, 0, 0, 0, 0, 0, 0, 4], [1, 0, 0, 0, 0, 0, 0, 0, 0, 4], [9, 8, 8, 8, 8, 8, 8, 8, 8, 12]]

def update_xy(dir):
    if(dir == 'f'):
        match robot_coords[2]:
            case 0:
                robot_coords[1] += 1
            case 1:
                robot_coords[0] += 1
            case 2:
                robot_coords[1] -= 1
            case 3:
                robot_coords[0] -= 1
    elif(dir == 'b'):
        match robot_coords[2]:
            case 0:
                robot_coords[1] -= 1
            case 1:
                robot_coords[0] -= 1
            case 2:
                robot_coords[1] += 1
            case 3:
                robot_coords[0] += 1

def checkifwall(pose):
    if bin(temp_wall[pose[1]][pose[0]])[2::].zfill(4)[pose[2]] == '1':
        print('wall detected')
        addwall((pose[0],pose[1]),1<<(3-pose[2]))
        #printmaze()
        reroute((pose[0],pose[1]))
        return True
    return False


while(maze_vals[robot_coords[1]][robot_coords[0]] != 0):
    next_dir = find_dir((robot_coords[0],robot_coords[1]))
    turn_calc = robot_coords[2] - next_dir
    if(turn_calc == 0):
        if checkifwall((robot_coords[0],robot_coords[1],robot_coords[2])):
            continue
        else:
            print("forward")
            update_xy('f')
    elif(turn_calc == 1):
        print('left')
        robot_coords[2] = (robot_coords[2] + 3) % 4
        print("forward")
        update_xy('f')
    if(turn_calc == -1):
        print('right')
        robot_coords[2] = (robot_coords[2] + 1) % 4
        print("forward")
        update_xy('f')
    elif(abs(turn_calc) == 2):
        print('back')
        update_xy('b')

printmaze()
    
    #if(result != 0):
    #    move(b,result)
    #    result = 0