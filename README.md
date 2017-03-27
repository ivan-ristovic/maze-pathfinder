# :sparkles: maze-pathfinder :sparkles:
![ss](https://raw.githubusercontent.com/ivan-ristovic/maze-pathfinder/master/mazes/feature_maze.bmp)

## :page_facing_up: Description
This is a simple program that takes maze input in form of an image and solves it using the
algorithm of your choice.
Program outputs an image with drawn exit path (if the maze is valid)

Rules for a valid maze:
- Everything that is not white will be interpreted as a wall.
- The maze must have one starting point on top, and one exit point in the bottom
(if there are multiple entry/exit points, only the first will be used)
- The maze must be surrounded by walls (i.e. must be closed)
- It is advisable for the corridors to be 1px wide, but it is not mandatory
   (the output will be correct for Dijkstra and A*, but not for DFS or BFS)"

## :computer: Installation
Download the project, navigate to the **/src** folder and run main.py
```
$ python main.py
```
:exclamation: **Note:** For the program to work, you must have the **PIL** and **Tkinter** libraries installed.
Additional information for PIL library can be found **[here](http://www.pythonware.com/products/pil/)**.
**Tkinter** should already be supported natively.

## :video_game: Usage
Mazes are loaded from **/mazes** folder, and you can put your custom mazes there. After you input the file name, you will need to load the maze. Then select an algorithm and start the solver. It might take some time, depending of the maze size.

After that, you will find a new image in **/mazes** folder, named in the format: **out_<filename>** which is the solution for the maze you entered.

## :bug: Known bugs
None so far!
