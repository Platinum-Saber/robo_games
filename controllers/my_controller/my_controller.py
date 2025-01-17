from controller import Robot
import math

robot = Robot()

timestep = int(robot.getBasicTimeStep())

sonarNames = ['sonarL_bwd', 'sonarL_fwd', 'sonarR_fwd', 'sonarR_bwd', 'sonar']
sonars = []
for sonarName in sonarNames:
    sonar = robot.getDevice(sonarName)
    sonar.enable(timestep)
    sonars.append(sonar)
    
wheelNames = ['bwdL', 'fwdL', 'fwdR', 'bwdR']
wheels = []
for wheelName in wheelNames:
    wheels.append(robot.getDevice(wheelName))
    wheels[-1].setPosition(float('Inf'))
    wheels[-1].setVelocity(0)

encoder = robot.getDevice('bwdL_encoder')
encoder.enable(100)

prevError = 0
errorInteg = 0
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    leftWallError = (sonars[1].getValue() - sonars[0].getValue()) / 5000
    rightWallError = (sonars[2].getValue() - sonars[3].getValue()) / 5000
    alignError = (sonars[1].getValue() - sonars[2].getValue()) / 5000
    
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
        
    wheels[0].setVelocity(-leftSpeed)
    wheels[2].setVelocity(-rightSpeed)
    wheels[1].setVelocity(-leftSpeed)
    wheels[3].setVelocity(-rightSpeed)
    