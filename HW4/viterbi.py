
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
# #print type(arg[2])
def getInput():
	with open(arg[2]) as f:
		lines = f.read().splitlines()
		for line in lines:
			values = map(float, line.split(' '))
			values[0] = int(values[0])
			values[1] = int(values[1])
			transitionprob[(values[0],values[1])]=values[2]
			if values[0] in transitionmap:
				transitionmap[values[0]].append(values[1])
			else:
				transitionmap[values[0]] = list()
				transitionmap[values[0]].append(values[1])
			if values[0] not in statespossible:
				statespossible.append(values[0])
			if values[1] not in statespossible:
				statespossible.append(values[1])
			statespossible.sort()
	# #print transitionmap
	#print transitionprob
	# #print statespossible

			
	with open(arg[3]) as f:
		lines = f.read().splitlines()
		for line in lines:
			values = line.split(' ')
			values[0] = int(values[0])
			values[2] = float(values[2])
			stateprob[(values[0],values[1])]=float(values[2])
	# #print stateprob
	# #print stateprob.get((1,'T'))

paths = list(list())
path = list()

def findpaths(root,count):
	#print('dkhdlk')
	#print root
	path.append(root)
	#print path
	count = count -1
	#print ('xlzhvnl;xfgnvl;xbl')
	#print count
	if root == arg[1]+1 and count==-1:
		return True
	if count<-1:
		return False
	if root == arg[1]+1 and count!=-1:
		return False
	for node in transitionmap.get(root):
		#print('yay')
		#print path
		#print node
		if findpaths(node,count)==True:
			#print('yayua')
			#print path
			optpath = list(path)
			paths.append(optpath)
		path.pop()
		#print(',dhflghlnhblckh;cmn;clgmn;gn')
		#print count


# def main():
# 	getInput()
# 	findpaths(0,len(arg[4])+1)
# 	#print paths
# 	for state in statespossible:
# 		if state == 0:
# 			probmatrix[0][state] = 1
# 		else:
# 			probmatrix[0][state] = 0
# 	maxstate.append(0)
# 	# #print maxstate
# 	for pos in range (1, len(arg[4])+1):
# 		# #print ("pos") + str(pos)
# 		maxcurrprob = 0
# 		maxcurrstate = 0
# 		for state in statespossible[1:-1]:
# 			tp = 0.0 if transitionprob.get((maxstate[pos-1],state))==None else transitionprob.get((maxstate[pos-1],state)) 
# 			#print probmatrix[pos-1][maxstate[pos-1]]
# 			#print tp
# 			#print stateprob.get((state,arg[4][pos-1]))
# 			# #print maxstate[pos-1]
# 			#print state
# 			#print pos
# 			# #print arg[4][pos-1]
			
# 			probmatrix[pos][state] = probmatrix[pos-1][maxstate[pos-1]]*tp*stateprob.get((state,arg[4][pos-1]))
# 			#print probmatrix[pos][state]
# 			if maxcurrprob<probmatrix[pos][state]:
# 				maxcurrprob = probmatrix[pos][state]
# 				maxcurrstate = state
# 			#print ("maxcurrstate")+str(maxcurrstate)
# 		maxstate.append(maxcurrstate)
# 		#print maxstate


def main():
	getInput()
	findpaths(0,len(arg[4])+1)
	print paths
	maxprob = 0
	optpath = list()
	for path in paths:
		pos  = 0
		prob = 1
		print path
		for ele in path[1:-1]:
			print ele
			print arg[4][pos]
			print transitionprob.get((path[ele-1],ele))
			print stateprob.get((ele,arg[4][pos]))
			print prob
			# print (transitionprob.get((path[ele-1],ele))*stateprob.get((ele,arg[4][pos])))
			prob = prob*(transitionprob.get((path[ele-1],ele))*stateprob.get((ele,arg[4][pos])))
			print prob
		prob = prob* (transitionprob.get((ele,path[-1])))
		print prob
		if prob>maxprob:
			maxprob = prob
			optpath = list(path)

	for state in optpath[1:-1]:
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
			print probmatrix[pos-1][maxstate[pos-1]]
			print transitionprob.get(maxstate[pos-1],state)
			# print state
			# print pos
			# print arg[4][pos-1]
			print stateprob.get((state,arg[4][pos-1]))
			probmatrix[pos][state] = probmatrix[pos-1][maxstate[pos-1]]*transitionprob.get(maxstate[pos-1],state)*stateprob.get((state,arg[4][pos-1]))
			if maxcurrprob<probmatrix[pos][state]:
				maxcurrprob = probmatrix[pos][state]
				maxcurrstate = state
			print ("maxcurrstate")+str(maxcurrstate)
		maxstate.append(maxcurrstate)
		print maxstate


	for state in maxstate[1:]:
		print state,

main()


















