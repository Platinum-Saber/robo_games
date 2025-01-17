# from controller import Supervisor

# robot = Supervisor()
# timestep = int(robot.getBasicTimeStep())

# root = robot.getRoot()
# child_field = root.getField('children')

# maze = [
#     "o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o",
#     "|                                               |               |",
#     "o   o---o---o---o---o---o---o   o---o   o   o   o   o   o   o   o",
#     "|   |                   |   |   |       |   |   |   |   |   |   |",
#     "o   o---o   o   o   o   o   o   o---o   o   o   o---o   o   o   o",
#     "|   |   |   |   |   |   |   |   |       |   |           |   |   |",
#     "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o---o   o",
#     "|   |   |   |   |   |   |   |                               |   |",
#     "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
#     "|   |       |   |   |   |   |   |                           |   |",
#     "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
#     "|   |   |   |               |   |                           |   |",
#     "o   o   o   o   o   o   o   o   o   o---o---o   o---o---o   o   o",
#     "|   |   |   |   |   |   |   |   |                           |   |",
#     "o   o---o   o   o   o   o   o---o---o---o---o---o---o---o---o   o",
#     "|               |   |   |   |       |                       |   |",
#     "o   o---o   o   o   o   o   o   o   o---o---o---o---o---o   o   o",
#     "|   |   |   |   |   |   |   |       |                           |",
#     "o   o   o   o   o   o   o   o   o---o---o---o---o---o---o---o   o",
#     "|   |   |   |   |   |   |   |   |                           |   |",
#     "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
#     "|   |   |   |               |   |                           |   |",
#     "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
#     "|   |       |   |   |   |   |   |                               |",
#     "o   o   o   o   o   o   o   o   o---o---o---o   o---o---o   o   o",
#     "|   |   |   |   |   |   |       |                           |   |",
#     "o   o   o   o   o   o   o   o   o   o---o---o   o---o---o---o   o",
#     "|   |   |   |   |   |   |   |           |   |           |   |   |",
#     "o   o---o   o   o   o   o   o   o   o---o   o   o---o   o   o   o",
#     "|   |                   |   |   |       |   |   |   |   |   |   |",
#     "o   o   o---o---o---o---o---o---o---o---o   o---o   o   o   o   o",
#     "|   |                                                           |",
#     "o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o",
#     "o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o"
# ]

# wallString = """maze_wall {{
#     rotation 0 0 1 {}
#     translation {} {} 0.05
# }}"""

# for i in range(0, len(maze)-1, 2):
#     scale = 1
#     even = i
#     odd = i+1
#     oddRow = maze[odd]
#     evenRow = maze[even]
    
#     for j in range(2, len(evenRow), 4):
#         wall_num = (j-2)/4
#         if maze[even][j] == "-":
#             ## move one space with wall
#             x = 0.25 * wall_num + 0.125
#             y = 0.25 * even/2 + 0.005
#             child_field.importMFNodeFromString(-1, wallString.format(0, x*scale, y*scale))

#     for j in range(0, len(oddRow), 4):
#         wall_num = j/4
#         if maze[odd][j] == "|":
#             ## move one space with wall
#             x = 0.25 * wall_num + 0.005
#             y = 0.25 * even/2 + 0.125
#             child_field.importMFNodeFromString(-1, wallString.format(1.57,x*scale, y*scale))

# # Main loop:
# # - perform simulation steps until Webots is stopping the controller
# while robot.step(timestep) != -1:
#     pass
# # Enter here exit cleanup code.
from controller import Supervisor

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

root = robot.getRoot()
child_field = root.getField('children')
maze = [
    "o---o---o---o---o---o---o---o---o---o---o",
    "|   |                       |           |",
    "o   o   o---o---o---o---o   o   o---o   o",
    "|       |       |           |   |       |",
    "o   o---o   o   o   o---o   o   o   o---o",
    "|   |   |   |       |           |       |",
    "o   o   o   o---o---o---o---o--Ro   o---o",
    "|   |       |       |           |       |",
    "o   o---o   o   o   o   o---o   o   o   o",
    "|   |       |   |       |       |   |   |",
    "o   o   o   o   o---o---o   o   o   o   o",
    "|   |   |   |   |           |       |   |",
    "o   o   o---o   o   o---o---o   o--Oo---o",
    "|   |   |       |       |   |           |",
    "o-G-o   o   o---o---o---o   oP--o---o   o",
    "|       |               |               |",
    "o   o---o---o---o---o   o---o---o   o---o",
    "|       |       |   |   |       |   |   |",
    "o---o   o   o   o   o   o   o   o   o   o",
    "|           |       |   |   |           |",
    "o---o---o---o---o---oY--o---o---o---o---o",
    "o---o---o---o---o---oY--o---o---o---o---o"
]

colors = {
    "R": (1, 0, 0),
    "O": (0.5, 0.5, 0.5),
    "G": (0, 1, 0),
    "P": (1, 0, 1),
    "Y": (1, 1, 0),
    "-": (0.5, 0.5, 0.5),
    }
    

wallString = """maze_wall {{
    rotation 0 0 1 {}
    translation {} {} 0.05
    baseColor {} {} {}
}}"""

for i in range(0, len(maze)-1, 2):
    scale = 1
    even = i
    odd = i+1
    oddRow = maze[odd]
    evenRow = maze[even]

    for j in range(2, len(evenRow), 4):
        wall_num = (j-2)/4

        x = 0.25 * wall_num + 0.125
        y = 0.25 * even/2 + 0.005
        
        for p in range(-1, 2):
            color = maze[even][j+p]
            if color in colors.keys():
                R, G, B = colors[color]
                # draw a wall in this color.
                child_field.importMFNodeFromString(-1, wallString.format(0, x*scale, y*scale, R, G, B))

    for j in range(0, len(oddRow), 4):
        wall_num = j/4
        if maze[odd][j] == "|":
            ## move one space with wall
            x = 0.25 * wall_num + 0.005
            y = 0.25 * even/2 + 0.125
            R, G, B = colors["-"]
                # draw a wall in this color.
            child_field.importMFNodeFromString(-1, wallString.format(1.57, x*scale, y*scale, R, G, B))
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    pass
# Enter here exit cleanup code.
