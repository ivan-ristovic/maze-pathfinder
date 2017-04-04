# :sparkles: maze-pathfinder :sparkles:
![ss](https://raw.githubusercontent.com/ivan-ristovic/maze-pathfinder/master/mazes/feature_maze.bmp)

## :page_facing_up: Description :page_facing_up:
This is a simple program that takes maze input in form of an image and solves it using the
algorithm of your choice.
Program outputs an image with drawn exit path (if the maze is valid).

Rules for a valid maze:
- Every pixel that is not white will be interpreted as part of a wall.
- The maze must have one starting point on top side, and one exit point on the bottom side
(if there are multiple entry/exit points, only the first will be used so sometimes path will not be found)
- The maze must be surrounded by walls (i.e. must be closed)
- Corridors should be 1px wide because then the program works optimally, but it is not mandatory
(the output will be correct for Dijkstra and A*, but might not be for DFS or BFS)

## :computer: Installation :computer:
Download the project, navigate to the **/src** folder and run main.py
```
$ python main.py
```

You must have the **/assets** folder in the same root folder as **/src** folder
(meaning you shouldn't move the files or folders around).

:exclamation: **Note:** Requirements:
- Python 2.7 (although it should work for 2.5 and above, but not tested)
- Windows or Linux OS (MacOS is not supported)
- For the program to work, you must have the **PIL** and **Tkinter** libraries installed.
Additional information for PIL library can be found **[here](http://www.pythonware.com/products/pil/)**.
**Tkinter** should already be supported natively.
- RAM should not be a problem (if you don't want to benchmark), but if you decide to run
mazes greater than 4000x4000, you will need around 1GB of free RAM memory for best performance.

## :video_game: Usage :video_game:
Mazes are loaded from **/mazes** folder, and you can put your custom mazes there.
After you input the file name, you will need to load the maze.
Then select an algorithm and start the solver. It might take some time, depending of the maze size.

After that, you will find a new image in **/mazes** folder, named in the format:
**out_<filename>** which is the solution for the maze you entered.

You can also create you own maze! Expand the window by clicking on the arrow button.
Choose your maze size and your maze will be created in **/mazes** folder, named in
the format: **generator_<size>**.

## :bug: Known bugs :bug:
None so far!
