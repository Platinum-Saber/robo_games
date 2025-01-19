"""encoder_drive controller."""

"""use move(dir) to move the robot. the parameter to be passed is the direction which can be f,r,l,b
f = 'forward'
r = 'right'
l = 'left'
b = 'back'
"""

from controller import Robot
from math import *
from floodfill import *

# create the Robot instance.
robot = Robot()

timestep = int(robot.getBasicTimeStep())
max_speed = 1

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)

left_positionSensor = robot.getDevice('left wheel sensor')
left_positionSensor.enable(timestep)
right_positionSensor = robot.getDevice('right wheel sensor')
right_positionSensor.enable(timestep)

ps_values = [0,0]
dist_values = [0,0]


wheel_radius = 20.5/1000
wheel_circum = 2*pi*wheel_radius
encoder_unit = wheel_radius

dist_between_wheels = 52/1000

robot_pose = [0,0,0] #x,y,theta
last_ps_values = [0,0]

robot_coords = [0,0,0] #x,y,direction

dt = timestep/1000
f = 'forward'
r = 'right'
l = 'left'
b = 'back'

turnright_ang = 1.755
movecell_dist = 0.256
sidecorrection_dist = movecell_dist - 0.075

#initialize IR
device_names = ['ps0','ps1','ps2','ps3','ps4','ps5','ps6','ps7',]
IR_array = []
for device in device_names:
    IR_array.append(robot.getDevice(device))
    IR_array[-1].enable(timestep)

IR_vals = [0,0,0,0,0,0,0,0]

def read_IR():
    for i in range(8):
        IR_vals[i] = IR_array[i].getValue()

def delay(duration):

    steps = int(duration / (timestep / 1000))  # Calculate number of steps
    for _ in range(steps):
        robot.step(timestep)


def update_xy(dir):
    if(dir == f):
        match robot_coords[2]:
            case 0:
                robot_coords[1] += 1
            case 1:
                robot_coords[0] += 1
            case 2:
                robot_coords[1] -= 1
            case 3:
                robot_coords[0] -= 1
    elif(dir == b):
        match robot_coords[2]:
            case 0:
                robot_coords[1] -= 1
            case 1:
                robot_coords[0] -= 1
            case 2:
                robot_coords[1] += 1
            case 3:
                robot_coords[0] += 1


def move(dir, linear_dist = movecell_dist, turn_ang = turnright_ang):
    print(f"Direction: {dir}")

    global robot_pose

    while robot.step(timestep) != -1:
        ps_values[0] = left_positionSensor.getValue()
        ps_values[1] = right_positionSensor.getValue()
    
        #print('---------------------------')
        #print('position sensor vals: {} {}'.format(ps_values[0],ps_values[1]))
    
        for i in range(2):
            diff = ps_values[i] - last_ps_values[i]
            #print('diff and i and ps {} {} {} {}'.format(diff,i,ps_values[i],last_ps_values[i]))
            if(diff < 0.001 and diff > 0):
                diff = 0
                ps_values[i] = last_ps_values[i]
            elif(diff<-2):
                diff = 0
            
            dist_values[i] = diff * encoder_unit
        
        #print('dist vals: {} {}'.format(dist_values[0],dist_values[1]))
        
        v = ((dist_values[0] + dist_values[1])/2.0)/dt
        w = ((dist_values[0] - dist_values[1])/dt)/dist_between_wheels
    
        robot_pose[2] += w * dt
    
        vx = v*cos(robot_pose[2])
        vy = v*sin(robot_pose[2])
    
        robot_pose[0] += vx*dt
        robot_pose[1] += vy*dt
        
        if(dir == 'forward'):
            read_IR()
            if((IR_vals[0]+IR_vals[7])/2 < 130):
                if(robot_pose[0] < linear_dist):
                    left_motor.setVelocity(max_speed)
                    right_motor.setVelocity(max_speed)
                else:
                    left_motor.setVelocity(0)
                    right_motor.setVelocity(0)
                    robot_pose = [0,0,0]
                    #print('resetting')
                    #print(robot_pose)
                    #delay(2)
                    update_xy(f)
                    return 0
            else:
                left_motor.setVelocity(0)
                right_motor.setVelocity(0)
                moveback_dist = abs(robot_pose[0])
                robot_pose = [0,0,0]
                addwall((robot_coords[0],robot_coords[1]),1<<(3-robot_coords[2]))
                reroute((robot_coords[0],robot_coords[1]))
                return moveback_dist
        elif(dir == 'right'):
    
            if(robot_pose[2] < turn_ang):
                left_motor.setVelocity(max_speed)
                right_motor.setVelocity(-max_speed)
            else:
                left_motor.setVelocity(0)
                right_motor.setVelocity(0)
                robot_pose = [0,0,0]
                #print('resetting')
                #print(robot_pose)
                #delay(2)
                #update coords
                robot_coords[2] = (robot_coords[2] + 1) % 4
                return
        elif(dir == 'left'):
    
            if(robot_pose[2] > (-turn_ang)):
                left_motor.setVelocity(-max_speed)
                right_motor.setVelocity(max_speed)
            else:
                left_motor.setVelocity(0)
                right_motor.setVelocity(0)
                robot_pose = [0,0,0]
                #print('resetting')
                #print(robot_pose)
                #delay(2)
                #update coords
                robot_coords[2] = (robot_coords[2] + 3) % 4
                return
        elif(dir == 'back'):
            print('going back')
            if(robot_pose[0] > -linear_dist):
                left_motor.setVelocity(-max_speed)
                right_motor.setVelocity(-max_speed)
            else:
                left_motor.setVelocity(0)
                right_motor.setVelocity(0)
                robot_pose = [0,0,0]
                #print('resetting')
                #print(robot_pose)
                #delay(2)
                if(linear_dist == movecell_dist):
                    update_xy(b)
                print("done")
                return
        
        for i in range(2):
            last_ps_values[i] = ps_values[i]
        
        #print('robot pose: {}'.format(robot_pose))
        #print(dist_values)
        
      

    
    
    

#f()
#f()
#r()






# Enter here exit cleanup code.
