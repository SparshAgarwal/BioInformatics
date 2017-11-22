
import sys
import collections
import math

arg = sys.argv
arg[1] = int(arg[1])
transitionprob = {}
transitionmap = {}
stateprob = {}
statespossible = list()
probmatrix = [[0 for x in range(arg[1]+2)] for y in range(len(arg[4])+1)]
probmatrixlog = [[0 for x in range(arg[1]+2)] for y in range(len(arg[4])+1)]

def getInput():
	with open(arg[2]) as f:
		lines = f.read().splitlines()
		for line in lines:
			values = map(float, line.split(' '))
			values[0] = int(values[0])
			values[1] = int(values[1])
			transitionprob[(values[0],values[1])]=values[2]
			if values[1] in transitionmap:
				transitionmap[values[1]].append(values[0])
			else:
				transitionmap[values[1]] = list()
				transitionmap[values[1]].append(values[0])
			if values[0] not in statespossible:
				statespossible.append(values[0])
			if values[1] not in statespossible:
				statespossible.append(values[1])
			statespossible.sort()

			
	with open(arg[3]) as f:
		lines = f.read().splitlines()
		for line in lines:
			values = line.split(' ')
			values[0] = int(values[0])
			values[2] = float(values[2])
			stateprob[(values[0],values[1])]=float(values[2])

def findprob():
	for state in statespossible:
		print state
		if state == 0:
			probmatrix[0][state] = 1.0
		else:
			probmatrix[0][state] = 0.0
	for i in range (0,len(arg[4])):
		for currstate in statespossible[1:-1]:
			states = transitionmap.get(currstate)
			reqvalue = 0
			for state in states:
				reqvalue+= probmatrix[i-1][state] * transitionprob.get(state,currstate)
			print stateprob.get((currstate, str(arg[4][i])))
			print currstate
			print str(arg[4][i])
			probmatrix[i][currstate] = reqvalue*stateprob.get((currstate, str(arg[4][i])))
			probmatrixlog[i][currstate] = math.log(probmatrix[i][currstate]) if probmatrix[i][currstate]!=0 else -1000000 
	states = transitionmap.get(statespossible[arg[1]+1])
	reqvalue = 0
	for state in states:
		reqvalue+= probmatrix[arg[1]][state] * transitionprob.get(state,arg[1]+1)
	probmatrix[-1][arg[1]+1] = reqvalue
	probmatrixlog[-1][arg[1]+1] = math.log(probmatrix[i][currstate]) if probmatrix[i][currstate]!=0 else -1000000 


getInput()
findprob()
print(probmatrixlog)
