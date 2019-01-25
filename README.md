
# Graph_Search_Algorithms (Python 3.7.0b5)

<p align="center">
  <a href="https://www.linkedin.com/in/guru-sarath-t-4ab648131/">
    <img src="https://github.com/gurusarath1/Snippets/blob/master/GitHubLogo_G_iconSize.png" alt="Guru Sarath T" width="72" height="72">
  </a>
</p>

This code finds a path from a start node to a goal using -
 - A* Algorithm
 - Depth First search
 - Breadth First search
 - Greedy Best First search
 - Branch and bound
 
The algorithm to run is chosen using the parameters given to the Search function in Search.py file

-------------------------------------------------------
## Settings for the Search function 

|DFS|BFS|GeedyBFS | BranchAndBound  |   Search Type
|---|:--|:--------|:----------------|:-----------------
| F | F |   F     |       F         |       A*
| F | F |   T     |       F         |   Greedy BFS
| F | F |   F     |       T         |   Branch and Bound
| F | F |   T     |       T         |       A*
| * | T |   *     |       *         |      BFS
| T | F |   *     |       *         |      DFS
-------------------------------------------------------

The graph to search is taken from the Graph.txt file.
Format of the file should should be maintained to ensure proper execution without any error.
