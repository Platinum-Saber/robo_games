from controller import Supervisor

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

root = robot.getRoot()
child_field = root.getField('children')

maze = [
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
]

for i in range(0, len(maze)):
    row = maze[i]
    horizontalWallStart = 0
    for j in range(len(row) - 1):
        left, right = row[j], row[j + 1]
        if not left:
            # move one space without wall
            horizontalWallStart += 0.25
        elif left and not right:
            horizontalWallStart += 0.25
            pass
            # don't move
        elif left and right:
            # move one space with wall
            y = 0.25 * i + 0.005
            wallString = """maze_wall {{
                rotation 0 0 1 0
                translation {} {} 1
            }}"""
            child_field.importMFNodeFromString(-1, wallString.format(horizontalWallStart + 0.125, -y))
            horizontalWallStart += 0.25
    continue
    # row = maze[i + 1]
    # horizontalWallStart = 0
    # for j in range(len(row) - 1):
        # left, right = row[j], row[j + 1]
        # top, bottom = row[j], nextRow[j]
        # if not left:
            # move one space without wall
            # horizontalWallStart += 0.25
        # elif left and not right:
            # pass
            # don't move
        # elif left and right:
            # move one space with wall
            # y = 0.25 * (i / 2) + 0.005
            # wallString = """maze_wall {{
                # rotation 0 0 1 0
                # translation {} {} 1
            # }}"""
            # child_field.importMFNodeFromString(-1, wallString.format(horizontalWallStart + 0.125, -y))
            # horizontalWallStart += 0.25
    # if not top:
        # move one space without wall
            # pass
    # elif top and not bottom:
        # stay right there
        # pass
    # elif top and bottom:
        # y = 0.25 * i + 0.125
        # wallString = """maze_wall {{
            # rotation 0 0 1 1.57
            # translation {} {} 1
        # }}"""
        # child_field.importMFNodeFromString(-1, wallString.format(horizontalWallStart + 0.005, -y))
        
for i in range(0, len(maze[0])):
    column = [row[i] for row in maze]
    verticalWallStart = 0
    for j in range(len(column) - 1):
        top, bottom = column[j], column[j + 1]
        if not top:
            # move one space without wall
            verticalWallStart += 0.25
        elif top and not bottom:
            verticalWallStart += 0.25
            pass
            # don't move
        elif top and bottom:
            # move one space with wall
            x = 0.25 * i + 0.005
            wallString = """maze_wall {{
                rotation 0 0 1 1.57
                translation {} {} 1
            }}"""
            child_field.importMFNodeFromString(-1, wallString.format(x, -(verticalWallStart + 0.125)))
            verticalWallStart += 0.25        

            
# for i in range(len(maze)):
    # for j in range(1, len(maze[i]), 2):
        # cell = maze[i][j]
        # if cell:
            # if (i % 2):
                # horizontal wall
                # x = 0.25 * j + 0.125
                # y = 0.25 * (i / 2) + 0.005
                # wallString = """maze_wall {{
                    # rotation 0 0 1 1.57
                    # translation {} {} 1
                # }}"""
                # child_field.importMFNodeFromString(-1, wallString.format(x, y))
            # else:
                # vertical wall
                # x = 0.25 * j + 0.125
                # y = 0.25 * ((i - 1) / 2) + 0.125
                # wallString = """maze_wall {{
                    # rotation 0 0 0 0
                    # translation {} {} 1
                # }}"""
                # child_field.importMFNodeFromString(-1, wallString.format(x, y))
           

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    pass
# Enter here exit cleanup code.
