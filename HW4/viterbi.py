
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
maxstate = list()
# print type(arg[2])
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
	# print transitionmap
	# print transitionprob
	# print statespossible

			
	with open(arg[3]) as f:
		lines = f.read().splitlines()
		for line in lines:
			values = line.split(' ')
			values[0] = int(values[0])
			values[2] = float(values[2])
			stateprob[(values[0],values[1])]=float(values[2])
	# print stateprob
	# print stateprob.get((1,'T'))
getInput()

def main():
	for state in statespossible:
		if state == 0:
			probmatrix[0][state] = 1
		else:
			probmatrix[0][state] = 0
	maxstate.append(0)
	# print maxstate
	for pos in range (1, len(arg[4])+1):
		# print ("pos") + str(pos)
		maxcurrprob = 0
		maxcurrstate = 0
		for state in statespossible[1:-1]:
			# print probmatrix[pos-1][maxstate[pos-1]]
			# print transitionprob.get(maxstate[pos-1],state)
			# print state
			# print pos
			# print arg[4][pos-1]
			# print stateprob.get((state,arg[4][pos-1]))
			probmatrix[pos][state] = probmatrix[pos-1][maxstate[pos-1]]*transitionprob.get(maxstate[pos-1],state)*stateprob.get((state,arg[4][pos-1]))
			if maxcurrprob<probmatrix[pos][state]:
				maxcurrprob = probmatrix[pos][state]
				maxcurrstate = state
			# print ("maxcurrstate")+str(maxcurrstate)
		maxstate.append(maxcurrstate)
		# print maxstate


	for state in maxstate[1:]:
		print state,

main()


















