mazeMatrix = []

with open("maze.txt", "r") as mazeSourceFile:
    for line in mazeSourceFile:
        mazeMatrix.append(line.rstrip("\n"))

mazeMatrix.append(line) # Appending a dummy line. Is there a 'nicer' way where we don't do this?

wallWidth = 0.25
wallWidthColored = 0.1
wallThickness = 0.01
wallHeight = 0.1

mazeLength = ((len(mazeMatrix) - 1) / 2) * wallWidth

wallTemplate = """
    maze_wall  {{
        rotation 0 0 1 {angle}
        translation {x} {y} {z}
        size {width} {breadth} {height}
        baseColor {R} {G} {B}
    }}
"""

colors = {
    "R" : {
        "R" : 1,
        "G" : 0,
        "B" : 0
    },
    "B" : {
        "R" : 165 / 255,
        "G" : 105 / 255,
        "B" : 30 / 255
    },
    "G" : {
        "R" : 0,
        "G" : 1,
        "B" : 0
    },
    "Y" : {
        "R" : 1,
        "G" : 1,
        "B" : 0
    },
    "P" : {
        "R" : 1,
        "G" : 0,
        "B" : 1
    },
    "-" : {
        "R" : 1,
        "G" : 1,
        "B" : 1
    }
}

wallParams = {
    "C" : { # C for colored
        "z" : wallHeight / 2,
        "width" : wallWidthColored,
        "breadth" : wallThickness,
        "height" : wallHeight
    },
    "-" : {
        "z" : wallHeight / 2,
        "width" : (wallWidth - wallWidthColored + (wallThickness / 2)) / 2,
        "breadth" : wallThickness,
        "height" : wallHeight
    },
    "---" : {
        "z" : wallHeight / 2,
        "width" : wallWidth + wallThickness,
        "breadth" : wallThickness,
        "height" : wallHeight
    }
}

mazeTargetFile = open("../../protos/maze.proto", "w")

header = """#VRML_SIM R2023b utf8
# template language: javascript

PROTO maze [
    field SFVec3f translation 0 0 0
    field SFRotation rotation 0 0 1 0
    field MFNode children [
"""

mazeTargetFile.write(header)

for row in range(0, len(mazeMatrix) - 1, 2):
    horizontalWalls = mazeMatrix[row]
    verticalWalls = mazeMatrix[row + 1]

    wallYStart = wallWidth * (row / 2)

    for i in range(2, len(horizontalWalls), 4):
        wallIndex = (i - 2) / 4

        # wallXStart = (wallWidth + wallThickness) * wallIndex + wallThickness
        # wallYStart = (wallWidth + wallThickness) * (row / 2)
        wallXStart = wallWidth * wallIndex

        wallString = horizontalWalls[i - 1 : i + 2]
        
        if wallString == "   ":
            continue

        elif wallString == "---":
            mazeTargetFile.write(wallTemplate.format(
                angle = 0,
                x = wallXStart + wallWidth / 2,
                y = mazeLength - (wallYStart), # + wallThickness / 2),
                **wallParams["---"],
                **colors["-"]
            ))

        else:
            for p in range(-1, 2):
                xOffset = 0
                wallType = "-"

                wallCharacter = horizontalWalls[i + p]
                if wallCharacter == "-":
                    xOffset = (wallWidth - wallWidthColored + (wallThickness / 2)) / 4
                else:
                    wallType = "C"
                    xOffset = wallWidthColored / 2

                mazeTargetFile.write(wallTemplate.format(
                    angle = 0,
                    x = wallXStart + xOffset,
                    y = mazeLength - (wallYStart), # + wallThickness / 2),
                    **wallParams[wallType],
                    **colors[wallCharacter]
                ))

                wallXStart += 2 * xOffset

    for j in range(0, len(verticalWalls), 4):
        wallIndex = j / 4

        # wallXStart = (wallWidth + wallThickness) * wallIndex
        # wallYStart = wallWidth * (row / 2) + wallThickness * ((row / 2) + 1)
        wallXStart = wallWidth * wallIndex

        wallCharacter = verticalWalls[j]

        if wallCharacter == "|":
            mazeTargetFile.write(wallTemplate.format(
                angle = 1.57,
                x = wallXStart, # + wallThickness / 2,
                y = mazeLength - (wallYStart + wallWidth / 2),
                **wallParams["---"],
                **colors["-"]
            ))

trailer = """
    ]
]
{
  Pose {
    translation IS translation
    rotation IS rotation
    children IS children
  }
}
"""

mazeTargetFile.write(trailer)

mazeTargetFile.close()
