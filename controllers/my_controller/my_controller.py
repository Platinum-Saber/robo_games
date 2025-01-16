"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import math

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
# timestep = 64

sonarNames = ['sonarL_bwd', 'sonarL_fwd', 'sonarR_fwd', 'sonarR_bwd', 'sonar']
sonars = []
for sonarName in sonarNames:
    sonar = robot.getDevice(sonarName)
    sonar.enable(timestep)
    sonars.append(sonar)
    
ir1 = robot.getDevice('irsense')
ir1.enable(timestep)

bwdL = robot.getDevice('bwdL')
bwdR = robot.getDevice('bwdR')
fwdL = robot.getDevice('fwdL')
fwdR = robot.getDevice('fwdR')

bwdL.setPosition(float('Inf'))
bwdR.setPosition(float('Inf'))
fwdL.setPosition(float('Inf'))
fwdR.setPosition(float('Inf'))

bwdL.setVelocity(0.0)
bwdR.setVelocity(0.0)
fwdL.setVelocity(0.0)
fwdR.setVelocity(0.0)

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

print("HELLO")

# Main loop:
prevError = 0
errorInteg = 0
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    leftWallError = (sonars[1].getValue() - sonars[0].getValue()) / 5000
    rightWallError = (sonars[2].getValue() - sonars[3].getValue()) / 5000
    alignError = (sonars[1].getValue() - sonars[2].getValue()) / 5000
    # if (abs(leftWallError) < 100):
        # leftWallError = 0
    # if (abs(rightWallError) < 100):
        # rightWallError = 0
    # if (abs(alignError) < 300):
        # alignError = 0
    # alignError = (alignError ** 2) * (alignError / abs(alignError))
    
    error = (-0.8 * leftWallError) + (0.8 * rightWallError) + (-4 * alignError)
    
    derivative = error - prevError
    errorInteg += error
    prevError = error
    
    pid = (10 * error) + (0 * derivative) + (0 * errorInteg)
    
    frontWallError = (sonars[4].getValue() - 90) / 3000 
    baseSpeed = 5 # frontWallError * 3
    
    # A positive error must cause it to turn right.
    rightSpeed = baseSpeed - pid
    leftSpeed = baseSpeed + pid
    
    if (abs(rightSpeed) > 10):
        rightSpeed = 10 * (rightSpeed / abs(rightSpeed))
    if (abs(leftSpeed) > 10):
        leftSpeed = 10 * (leftSpeed / abs(leftSpeed))
        
    bwdL.setVelocity(-leftSpeed)
    bwdR.setVelocity(-rightSpeed)
    fwdL.setVelocity(-leftSpeed)
    fwdR.setVelocity(-rightSpeed)
    