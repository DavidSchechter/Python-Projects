__author__ = 'DavidSchechter'

#Student: David Schechter
#Student ID: 009987848
#email: david.schehcter.mail@gmail.com

import heapq
import math
import sys

# class definition of BoardSquare - a square in the maze
#content, x and y location, cost from starting location in the path, heuristic estimate cost,total cost,
#what was the previous square in the path
#builder receives x and y location and content


class BoardSquare:
	def __init__(self, content, xloc, yloc):
		self.content = content
		self.xloc = xloc
		self.yloc = yloc
		self.costFromStart = 0
		self.heuristic = 0
		self.fcost = 0
		self.cameFromSquare = self


#function for getting all accessible cell from current cell
#function checks if square in all possible locations and return only the accessible ones
#function receives a maze and a cell to check


def getaccessiblecellsfromcell(tempmazeboard, cell):
	accessiblecells = []
	mazelength = len(tempmazeboard)
	mazewidth = len(tempmazeboard[0])
	if cell.xloc - 1 >= 0:
		if not (tempmazeboard[cell.yloc][cell.xloc - 1].content == 2):
			accessiblecells.append(tempmazeboard[cell.yloc][cell.xloc - 1])
	if cell.yloc - 1 >= 0:
		if not (tempmazeboard[cell.yloc - 1][cell.xloc].content == 2):
			accessiblecells.append(tempmazeboard[cell.yloc - 1][cell.xloc])
	if cell.yloc + 1 <= mazelength - 1:
		if not (tempmazeboard[cell.yloc + 1][cell.xloc].content == 2):
			accessiblecells.append(tempmazeboard[cell.yloc + 1][cell.xloc])
	if cell.xloc + 1 <= mazewidth - 1:
		if not (tempmazeboard[cell.yloc][cell.xloc + 1].content == 2):
			accessiblecells.append(tempmazeboard[cell.yloc][cell.xloc + 1])
	return accessiblecells


#function for getting equlidian distance from cell to the goal cell
#function receives a cell, a goal cell, cell which we came from and maze check


def getequlidiandistance(cell, tempgoalcell, camerromcell, tempmazeboard):
	return math.sqrt(math.pow((cell.xloc - tempgoalcell.xloc), 2) + math.pow((cell.yloc - tempgoalcell.yloc), 2))


#function for getting manhattan distance from cell to the goal cell
#function receives a cell, a goal cell, cell which we came from and maze check


def getmanhattandistance(cell, tempgoalcell, camefromcell, tempmazeboard):
	return math.sqrt(math.fabs(cell.xloc - tempgoalcell.xloc) + math.fabs(cell.yloc - tempgoalcell.yloc))


#function for getting made-up heuristic distance from cell to the goal cell
#Fucntion uses manhattan heuristic and adds 100 to value if cell is a dead end
#function receives a cell, a goal cell, cell which we came from and maze check


def getmadeupheuristic(cell, tempgoalcell, camefromcell, tempmazeboard):
	currentx = cell.xloc
	currenty = cell.yloc
	mazelength = len(tempmazeboard)
	mazewidth = len(tempmazeboard[0])
	deadendleft = 0
	deadendright = 0
	deadendup = 0
	deadenddown = 0
	if currentx - 1 >= 0:
		if tempmazeboard[currenty][currentx - 1] == 2 or (
						currenty == camefromcell.yloc and currentx - 1 == camefromcell.xloc):
			deadendleft = 1
		else:
			deadendleft = 0
	else:
		deadendleft = 1

	if currenty - 1 >= 0:
		if tempmazeboard[currenty - 1][currentx] == 2 or (
							currenty - 1 == camefromcell.yloc and currentx == camefromcell.xloc):
			deadenddown = 1
		else:
			deadenddown = 0
	else:
		deadenddown = 1

	if currentx + 1 <= mazewidth - 1:
		if tempmazeboard[currenty][currentx + 1] == 2 or (
						currenty == camefromcell.yloc and currentx + 1 == camefromcell.xloc):
			deadendright = 1
		else:
			deadendright = 0
	else:
		deadendright = 1

	if currenty + 1 <= mazelength - 1:
		if tempmazeboard[currenty + 1][currentx] == 2 or (
							currenty + 1 == camefromcell.yloc and currentx == camefromcell.xloc):
			deadendup = 1
		else:
			deadendup = 0
	else:
		deadendup = 1

	if deadendleft == 1 and deadendright == 1 and deadenddown == 1 and deadendup == 1:
		return math.sqrt(math.fabs(cell.xloc - tempgoalcell.xloc) + math.fabs(cell.yloc - tempgoalcell.yloc)) + 100
	else:
		return math.sqrt(math.fabs(cell.xloc - tempgoalcell.xloc) + math.fabs(cell.yloc - tempgoalcell.yloc))


#function for getting the a star path from a cell to the goal cell on the maze board using a heuristic function
#fucntion return the a star path found
#function receives a maze, a start cell, a goal cell and a heuristic function to check


def astarpath(tempstartcell, tempgoalcell, tempmazeboard, tempheuristicfunc):
	bestpath = []
	tempstartcell.heuristic = tempheuristicfunc(tempstartcell, tempgoalcell, tempstartcell, tempmazeboard)
	tempstartcell.fcost = tempstartcell.costFromStart + tempstartcell.heuristic
	frontier = []
	heapq.heapify(frontier)
	heapq.heappush(frontier, (tempstartcell.fcost, tempstartcell))
	exploredcells = []
	foundpath = 0
	currentcell = BoardSquare(0, 0, 0)
	while frontier:
		fcost, currentcell = heapq.heappop(frontier)
		if (currentcell.xloc == tempgoalcell.xloc) and (currentcell.yloc == tempgoalcell.yloc):
			foundpath = 1
			frontier = []
		exploredcells.append(currentcell)
		accessiblecells = getaccessiblecellsfromcell(tempmazeboard, currentcell)
		for i in xrange(0, len(accessiblecells)):
			childnode = accessiblecells[i]
			childnode.costFromStart = currentcell.costFromStart + 1
			childnode.heuristic = tempheuristicfunc(childnode, tempgoalcell, currentcell, tempmazeboard)
			childnode.fcost = childnode.heuristic + childnode.costFromStart
			if (not ((childnode.fcost, childnode) in frontier)) and (not (childnode in exploredcells)):
				childnode.cameFromSquare = currentcell
				heapq.heappush(frontier, (childnode.fcost, childnode))
			else:
				for k in xrange(0, len(frontier)):
					if frontier[k][1].xloc == childnode.xloc and frontier[k][1].yloc == childnode.yloc:
						if frontier[k][0] > childnode.fcost:
							frontier[k][0] = childnode.fcost
							frontier[k][1] = childnode
							heapq.heapify(frontier)
	if (not frontier) and (foundpath == 1):
		tempcell = currentcell.cameFromSquare
		while not ((tempcell.xloc == currentcell.xloc) and (tempcell.yloc == currentcell.yloc)):
			bestpath.append(currentcell)
			tempcell = currentcell.cameFromSquare
			currentcell = tempcell
			tempcell = currentcell.cameFromSquare
		bestpath.append(currentcell)
		bestpath.reverse()
		return bestpath
	else:
		return []


#function to convert a maze text file into a two-d array
#function receives a filename


def readmazefileandcreatemaze(tempfilename):
	tempmazeboard = []
	f = open(tempfilename)
	line = f.readline()
	y = 0
	tempstartcell = BoardSquare(0, 0, 0)
	tempgoalcell = BoardSquare(0, 0, 0)
	while line:
		tempmazeboardrow = []
		linelength = len(line)
		for x in xrange(0, linelength):
			currentchar = line[x]
			if currentchar == "@":
				tempstartcell = BoardSquare(1, x, y)
				tempmazeboardrow.append(tempstartcell)
			elif currentchar == "#":
				tempmazeboardrow.append(BoardSquare(2, x, y))
			elif currentchar == "%":
				tempgoalcell = BoardSquare(3, x, y)
				tempmazeboardrow.append(tempgoalcell)
			elif currentchar == ".":
				tempmazeboardrow.append(BoardSquare(0, x, y))
			else:
				pass
		line = f.readline()
		y += 1
		tempmazeboard.append(tempmazeboardrow)
	f.close()
	return tempmazeboard, tempstartcell, tempgoalcell


#function to print the a a star path step by step
#function receives a path and a maze


def printsolutionpath(tempsolvedpath, tempmazeboard):
	place = ""
	if tempsolvedpath:
		for i in xrange(0, len(tempsolvedpath)):
			if i > 0:
				print "step %d:\n" % i
			else:
				print "inital:\n"
			row = ""
			for y in xrange(0, len(tempmazeboard)):
				for x in xrange(0, len(tempmazeboard[0])):
					if tempmazeboard[y][x].content == 2:
						place = "#"
					elif tempmazeboard[y][x].content == 0:
						place = "."
					elif tempmazeboard[y][x].content == 3:
						place = "%"
					elif tempmazeboard[y][x].content == 1:
						place = "@"
					else:
						pass
					row += place + " "
				print row
				row = ""
			print "\n"
			if i + 1 < len(tempsolvedpath):
				oldcontent = tempmazeboard[tempsolvedpath[i + 1].yloc][tempsolvedpath[i + 1].xloc].content
				tempmazeboard[tempsolvedpath[i + 1].yloc][tempsolvedpath[i + 1].xloc].content = \
					tempmazeboard[tempsolvedpath[i].yloc][tempsolvedpath[i].xloc].content
				if oldcontent == 3:
					oldcontent = 0
				tempmazeboard[tempsolvedpath[i].yloc][tempsolvedpath[i].xloc].content = oldcontent
		print "Problem Solved! I had some noodles!"
	else:
		print "Problem can not be Solved! I am still hungry!"


#main function


if (len(sys.argv)) != 3:
	print "Please supply a filename and type of heuristic function to use"
	raise SystemExit(1)
else:
	filename = sys.argv[1]
	heuristicMethod = sys.argv[2]
	mazeBoard, startcell, goalcell = readmazefileandcreatemaze(filename)
	solvedPath = []
	if heuristicMethod == "euclidean":
		solvedPath = astarpath(startcell, goalcell, mazeBoard, getequlidiandistance)
	elif heuristicMethod == "manhattan":
		solvedPath = astarpath(startcell, goalcell, mazeBoard, getequlidiandistance)
	elif heuristicMethod == "made_up":
		solvedPath = astarpath(startcell, goalcell, mazeBoard, getmadeupheuristic)
	else:
		print "no such heuristic can be used, please try one of the following: euclidean,manhattan,made_up"
		raise SystemExit(1)
	printsolutionpath(solvedPath, mazeBoard)