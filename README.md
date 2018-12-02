# Graph_Search_Algorithms
This code finds a path from a start node to a goal using -
 - A* Algorithm
 - Depth First search
 - Breadth First search
 - Greedy Best First search
The algorithm to run is chosen using the parameters given to the Search function in Search.py file

-------------------------------------------------------
Settings for the Search function 
-------------------------------------------------------
DFS|BFS|GeedyBFS | BranchAndBound  |   Search Type
 F | F |   F     |       F         |       A*
 F | F |   T     |       F         |   Greedy BFS
 F | F |   F     |       T         |   Branch and Bound
 F | F |   T     |       T         |       A*
 * | T |   *     |       *         |      BFS
 T | F |   *     |       *         |      DFS
-------------------------------------------------------

The graph to search is taken from the Graph.txt file.
Format of the file should should be maintained to ensure proper execution without any error.
