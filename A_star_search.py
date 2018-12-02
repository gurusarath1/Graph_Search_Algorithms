#December 1 2018
#Written by Guru Sarath

import copy 
import math

problem_file_pt = open("Graph.txt")

startGoal = None
graphConnections = None
graphConnections_String = ''
graphNodes = None
graphNodes_String = ''

inputType = 0
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


#print(startGoal)
graphConnections = eval(graphConnections_String[1:])
graphNodes = eval(graphNodes_String[1:])

def ConnectedNodes(CurrentNode):

	NodesList = []
	connections  = graphConnections[CurrentNode]

	for NodeX in connections:
		NodesList.append(NodeX[0])

	return NodesList

def h_value(CurrentNode, GoalNode):

	h = 0

	return h

def g_value(NodeFrom, NodeTo):
	NodesConnectedToNodeFrom = ConnectedNodes(NodeFrom)

	if NodeTo in NodesConnectedToNodeFrom:
		nodesWithCost = graphConnections[NodeFrom]

		for ConnectionX in nodesWithCost:
			if ConnectionX[0] == NodeTo:
				g_value_From_To = ConnectionX[1]
				return g_value_From_To
	else:

		return 'Impossible'

def f_value(NodeFrom, NodeTo, GoalNode):
	h = h_value(NodeTo, GoalNode)
	g = g_value(NodeFrom, NodeTo)
	

	if g != 'Impossible':
		f = g + h
		return f
	else:
		return 'Impossible'


def MergeTwoNodeLists(NodesX, NodesY):
	
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

def returnLeastCostNode(NodeList):
	minCost = NodeList[0][1]
	minNode = NodeList[0][0]
	camefromOfTheNode = NodeList[0][2]

	for nodeX in NodeList:
		if minCost > nodeX[1]:
			minCost = nodeX[1]
			minNode = nodeX[0]
			camefromOfTheNode = nodeX[2]

	return [minNode, minCost, camefromOfTheNode]

def reConstructPath(CameFromDict, start, goal):

	current = goal
	path = []
	path_string = 'Start'

	#reversedDict = {value: key for key,value in CameFromDict.items()}
	#print(reversedDict)

	while CameFromDict[current] != 'Entry':
		path.append(current)
		current = CameFromDict[current]

	path.append(start)

	for nodeX in path[::-1]:
		path_string = path_string + ' -> ' + nodeX

	return (path[::-1], path_string)




def A_Star_search(startNode, GoalNode):
	openList = [[startNode, 0, 'Entry']]
	currentNode = ['Entry',0]
	closedSet = set()
	CameFrom = {}

	while openList:
		

		prevNode = currentNode[0]
		currentNode = returnLeastCostNode(openList)
		CameFrom[currentNode[0]] = currentNode[2]
		openList.remove(currentNode)
		closedSet.add(currentNode[0])
		#print(currentNode, 'CN')
		

		if currentNode[0] == GoalNode:
			print('Goal found ----------------\n')
			#print(CameFrom, 'Came from')
			print(reConstructPath(CameFrom, startNode, GoalNode)[1], '\n')
			return


		nextNodes = copy.deepcopy(graphConnections[currentNode[0]])

		i = 0
		for nodeX in nextNodes:
			nextNodes[i][1] = f_value(currentNode[0], nodeX[0], GoalNode) + currentNode[1]
			nextNodes[i].append(currentNode[0])
			i = i + 1

		for nodeX in nextNodes:
			if nodeX[0] not in closedSet:
				openList.append(nodeX)

		#print(openList,' O')
		#print(closedSet, ' C')
		#print('-----------------------------------')

A_Star_search(startGoal['start'],startGoal['goal'])
