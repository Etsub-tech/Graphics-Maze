# Maze Generator And Solver
This project is a maze generator solver made using pytjon and Pygame. The maze is generated using a stack based DFS(Depth First Search) algorithm and solved using a backtracking algorithm.

## The program visually shows:
-the maze being generated
-the solving process
-dead ends and the final solution path

## How the maze works
the maze uses two arrays:
northWall[R+1][C]
eastWall[R][C+1]
-northwall stors top walls whereas eastwall stores right walls
if the value is: 
    1 -> wall exists
    0 -> wall removed

## Maze Generation
the maze starts as a full grid then a DFS mouth moves through the cells:
1, chooses a random unvisited neighbour
2, removes the wall between them
3, pushes the new cell onto a stack
4, backtracks when it reaches a dead end
this continues until all cells are visited.
Because DFS is used, the maze becomes a perfect maze with one unique path between cells.

## Maze solving
the solver uses backtrackinh.
the mouse: 
1, tries random valid directions
2, stores its path using a stack
3, backtracks from dead ends
4, reconstructs the final path once the exit is found

## Colors
Blue -> current mouse position
Orange -> dead ends
Green -> final solution path
Yellow -> starts and end cells

## Bonus Feature
A bonus mode can randomly remove extra walls to create cycles or loops in the maze. this breaks the perfect maze property (which we could use the sholder to the wall solving rule to) and creats multiple pathes.

## How to run it 
first install pygame: write pip instgall pygame in the bash
then run it: python maze.py
Files: maze.py, README.md

## SECTION 3
## Group Members: 
Eden Yirefu - UGR/2749/16
Etsub Amha - UGR/7052/16
Eyerusalem Gebrat - UGR/9470/16
Feven Tamene - UGR/9745/16 
Misgana Yonas - UGR/5936/16 
Naomi Tilahun - UGR/8935/16

# DEMO VIDEO
https://www.awesomescreenshot.com/video/52856391?key=e1439ea546f9bbf6f98284b933122bde
