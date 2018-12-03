#December 1 2018
#Written by Guru Sarath

import copy 
import math
import time



#############################################################
#                                                           #
#       Code to extract graph from Graph.txt file           #
#                                                           #
#############################################################


problem_file_pt = open("Graph.txt")

startGoal = None
graphConnections = None
graphConnections_String = ''
graphNodes = None
graphNodes_String = ''

inputType = 0
LineX = problem_file_pt.readline() # Skip the first line - First line in the file is used for comments
LineX = problem_file_pt.readline()

while LineX:
	if LineX[0] == '#':
		inputType = inputType + 1

	if inputType == 0:
		startGoal = eval(LineX)

	if inputType == 1:
		graphNodes_String = graphNodes_String + LineX[:-1]

	if inputType == 2:
		graphConnections_String = graphConnections_String + LineX[:-1]

	LineX = problem_file_pt.readline()
	

#############################################################
#                                                           #
#       Search algorithm code                               #
#                                                           #
#############################################################

#print(startGoal)
graphConnections = eval(graphConnections_String[1:])
graphNodes = eval(graphNodes_String[1:])

def ConnectedNodes (CurrentNode):

	NodesList = []
	connections  = graphConnections[CurrentNode]

	for NodeX in connections:
		NodesList.append(NodeX[0])

	return NodesList

def h_value (CurrentNode, GoalNode):

	h = ((graphNodes[CurrentNode][0] - graphNodes[GoalNode][0])**2 + (graphNodes[CurrentNode][1] - graphNodes[GoalNode][1])**2)**0.5

	return h

def g_value (NodeFrom, NodeTo):
	NodesConnectedToNodeFrom = ConnectedNodes(NodeFrom)

	if NodeTo in NodesConnectedToNodeFrom:
		nodesWithCost = graphConnections[NodeFrom]

		for ConnectionX in nodesWithCost:
			if ConnectionX[0] == NodeTo:
				g_value_From_To = ConnectionX[1]
				return g_value_From_To
	else:

		return 'Impossible'

def f_value (NodeFrom, NodeTo, GoalNode, GeedyBFS = False, BranchAndBound = False):
	h = h_value(NodeTo, GoalNode)
	g = g_value(NodeFrom, NodeTo)

	if GeedyBFS:
		g = 0

	if BranchAndBound:
		h = 0
	

	if g != 'Impossible':
		f = g + h
		return f
	else:
		return 'Impossible'


def MergeTwoNodeLists (NodesX, NodesY):
	
	MergedList = []

	lenX = len(NodesX)
	lenY = len(NodesY)
	Maxindex = lenX + lenY
	index = 0

	for i in range(Maxindex):
		if NodesX[index][1] < NodesY[index][1]:
			MergedList.append(NodesX[index])
		elif NodesX[index][1] > NodesY[index][1]:
			MergedList.append(NodesY[index])
		else:
			MergedList.append(NodesY[index])
			MergedList.append(NodesX[index])
			index = index + 1

		index = index + 1

	return MergedList

# Returns the node with least cost 
# Nodelist - [['B', 2, 'A'], ['C', 2, 'D'], ['I', 6, 'H'], ['P', 10, 'H'], ['N', 11, 'H'], ['L', 6, 'H'], ['G', 6, 'H']]  Open list
def returnLeastCostNode (NodeList, Goal, GeedyBFS, BranchAndBound):
	minCost = minCost_g_score_only = NodeList[0][1]
	minNode = NodeList[0][0]
	camefromOfTheNode = NodeList[0][2]

	#In case of A* search add the h score also
	if GeedyBFS == BranchAndBound:
		minCost += h_value(NodeList[0][0], Goal)
		for nodeX in NodeList:
			if minCost > nodeX[1] + h_value(nodeX[0], Goal):
				minCost = nodeX[1] + h_value(nodeX[0], Goal)
				minCost_g_score_only = nodeX[1]
				minNode = nodeX[0]
				camefromOfTheNode = nodeX[2]

	# if it is not A* search
	else:
		for nodeX in NodeList:
			if minCost > nodeX[1]:
				minCost = nodeX[1]
				minCost_g_score_only = nodeX[1]
				minNode = nodeX[0]
				camefromOfTheNode = nodeX[2]

	return [minNode, minCost_g_score_only, camefromOfTheNode]

# Reconstruct the path after reaching the goal node
def reConstructPath (CameFromDict, start, goal):

	current = goal
	path = []
	path_string = 'start'
	path_cost = 0

	#reversedDict = {value: key for key,value in CameFromDict.items()}
	#print(reversedDict)

	while CameFromDict[current] != 'Entry':
		# Back track from the goal node to the start node
		path.append(current)
		current = CameFromDict[current]

	path.append(start)

	# Create the string output of the path
	for nodeX in path[::-1]:
		path_string = path_string + ' -> ' + nodeX

	reversed_path = path[::-1] # actually not reversed

	# Calculate the path cost - g score sum from start to goal
	i = 1
	for nodex in path[::-1]:
		path_cost += g_value(nodex, path[::-1][i])
		#print(nodex, path[::-1][i], g_value(nodex, path[::-1][i]))
		i += 1

		if i==len(path[::-1]):
			break

	# return a tuple containing list(reversed) and string form of the output path and path length and path cost (g score sum)
	return (path[::-1], path_string, len(path), path_cost)


# This function returns the type of search performed based on the settings in Search function 
def printSearchType (GeedyBFS = False, BranchAndBound = False, DFS = False, BFS = False):
	if DFS:
		return 'Depth First Search'
	elif BFS:
		return 'Breadth First Search'
	elif GeedyBFS == False and BranchAndBound == False:
		return 'A* Search'
	elif GeedyBFS == True and BranchAndBound == False:
		return 'Greedy Best First search'
	elif GeedyBFS == False and BranchAndBound == True:
		return 'Branch and Bound'
	elif GeedyBFS == True and BranchAndBound == True:
		return 'A*'

"""
Settings for the Search function 
-------------------------------------------------------
DFS|BFS|GeedyBFS | BranchAndBound  |   Search Type
 F | F |   F     |       F         |       A*
 F | F |   T     |       F         |   Greedy BFS
 F | F |   F     |       T         |   Branch and Bound
 F | F |   T     |       T         |       A*
 * | T |   *     |       *         |      BFS
 T | F |   *     |       *         |      DFS
 -----------------------------------------------------
"""

# This function performs the actual search
def Search (startNode, GoalNode, GeedyBFS = False, BranchAndBound = False, DFS = False, BFS = False):
	'''
	Node is a list with 3 elements
	Format:
	[node name, g score, came from node]
	'''
	openList = [[startNode, 0, 'Entry']] # Start the search with only the start node in the open list (came from of start node is 'Entry')
	currentNode = ['Entry',0]
	closedSet = set()
	CameFrom = {}
	startTime = time.time()
	goalFound = False

	iteration_count = 1
	# Search until all nodes are visited
	while openList:

		prevNode = currentNode[0]

		'''
		Node is a list with 3 elements
		Format:
		[node name, g score, came from node]
		'''

		if not DFS and not BFS:
			# Take the node with least cost
			currentNode = returnLeastCostNode(openList, GoalNode, GeedyBFS, BranchAndBound)
		elif BFS:
			# Take the next node in the starting of the list 
			currentNode = openList[0]
		elif DFS:
			# Take the node at the end of the list (Most recently added node)
			currentNode = openList[-1]
		else:
			# impossible to hit this code
			pass

		#Update camefrom dictionary to reconstruct the path later
		CameFrom[currentNode[0]] = currentNode[2]
		openList.remove(currentNode)
		closedSet.add(currentNode[0])
		#print(currentNode, 'Node moved to closed')
		

		# Goal test is done only after moving a node to the closed list
		if currentNode[0] == GoalNode:
			goalFound = True
			path = reConstructPath(CameFrom, startNode, GoalNode)
			path_string = path[1]
			path_length = path[2]
			print('\n' + 
				printSearchType (GeedyBFS, BranchAndBound, DFS, BFS) + '----\n'+ 
				path_string + 
				' - Path length - '+ str(path_length) + 
				' - Cost - ' + str(path[3]) +
				' - Iterations - ' + str(iteration_count) +
				' - Search Time - ' + str(time.time() - startTime))

			return True


		nextNodes = copy.deepcopy(graphConnections[currentNode[0]])

		# This loop below is used to assign the f score to all the discovered nodes (f score is the second element in the list)
		'''
		Node is a list with 3 elements
		Format:
		[node name, g score, came from node]
		'''
		i = 0
		for nodeX in nextNodes:

			# Branch and Bound 
			if GeedyBFS == False and BranchAndBound == True:
				# f score function only returns the g score
				nextNodes[i][1] = f_value(currentNode[0], nodeX[0], GoalNode, GeedyBFS, BranchAndBound) + currentNode[1]

			# Greedy BFS
			elif GeedyBFS == True and BranchAndBound == False:
				# f score function only returns the h score
				nextNodes[i][1] = f_value(currentNode[0], nodeX[0], GoalNode, GeedyBFS, BranchAndBound)

			# A*
			else:
				# Accumulate only the g score; h score is considered in 'returnLeastCostNode' funtion
				nextNodes[i][1] = g_value(currentNode[0], nodeX[0]) + currentNode[1]

			nextNodes[i].append(currentNode[0])
			i = i +  1


		# Add the nodes to open list only if it was never visited
		for nodeX in nextNodes:
			# Check if the node is not present in closed list
			if nodeX[0] not in closedSet:
				# Add the node to the end of the list
				openList.append(nodeX)

		#print(openList,' Open list')
		#print(closedSet, ' Closed list')
		#print('-----------------------------------')
		iteration_count += 1

	if not goalFound:
		print ('Cannot reach the ' + GoalNode + ' from ' + startNode  +  printSearchType (GeedyBFS, BranchAndBound, DFS, BFS) +  ' - Search Time - ' + str(time.time() - startTime) )
		return False

		
#############################################################
#                                                           #
#       Algorithm Execution                                 #
#                                                           #
#############################################################

Search(startGoal['start'],startGoal['goal'], GeedyBFS = False, BranchAndBound = False, DFS = False, BFS = False)

Search(startGoal['start'],startGoal['goal'], GeedyBFS = False, BranchAndBound = True, DFS = False, BFS = False)

Search(startGoal['start'],startGoal['goal'], GeedyBFS = True, BranchAndBound = False, DFS = False, BFS = False)

Search(startGoal['start'],startGoal['goal'], GeedyBFS = False, BranchAndBound = False, DFS = False, BFS = True)

Search(startGoal['start'],startGoal['goal'], GeedyBFS = False, BranchAndBound = False, DFS = True, BFS = False)

problem_file_pt.close()
input('\n\n\nPress enter')



