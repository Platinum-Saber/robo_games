from controller import Supervisor

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

root = robot.getRoot()
child_field = root.getField('children')

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

wallString = """maze_wall {{
    rotation 0 0 1 {}
    translation {} {} 0.05
}}"""

for i in range(0, len(maze)-1, 2):
    scale = 1
    even = i
    odd = i+1
    oddRow = maze[odd]
    evenRow = maze[even]
    
    for j in range(2, len(evenRow), 4):
        wall_num = (j-2)/4
        if maze[even][j] == "-":
            ## move one space with wall
            x = 0.25 * wall_num + 0.125
            y = 0.25 * even/2 + 0.005
            child_field.importMFNodeFromString(-1, wallString.format(0, x*scale, y*scale))

    for j in range(0, len(oddRow), 4):
        wall_num = j/4
        if maze[odd][j] == "|":
            ## move one space with wall
            x = 0.25 * wall_num + 0.005
            y = 0.25 * even/2 + 0.125
            child_field.importMFNodeFromString(-1, wallString.format(1.57,x*scale, y*scale))

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    pass
# Enter here exit cleanup code.
