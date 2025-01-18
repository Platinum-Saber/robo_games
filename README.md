### Protos
1. `maze_wall.proto`
A `Solid` node. Describes the basic structure of a wall.

2. `maze.proto`
A `Pose` node. Contains `maze_wall`s as children, translated, scaled, rotated, and colored appropriately, forming the maze.

### Procedure
1. Start with an empty `.wbt` file.
2. Run `controllers/my_supervisor/mazeWallGenerator.py`. This will refer the maze in `controllers/my_supervisor/maze.txt` and populate the `children` node of the `maze` proto specified above, by directly writing to the `maze.proto` file.
3. Add a supervisor `Robot` to the world. Choose `my_supervisor` as its controller.
4. Place e-Puck, or any other robot as desired.
5. Run the simulation. The supervisor will include the `maze` proto node, and it will appear in the world.
