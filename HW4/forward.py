 
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
f = [[0 for x in range(arg[1]+2)] for y in range(len(arg[4])+2)]
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

# def findprob():
# 	for state in statespossible:
# 		print state
# 		if state == 0:
# 			probmatrix[0][state] = 1.0
# 		else:
# 			probmatrix[0][state] = 0.0
# 	for i in range (0,len(arg[4])):
# 		for currstate in statespossible[1:-1]:
# 			states = transitionmap.get(currstate)
# 			reqvalue = 0
# 			for state in states:
# 				reqvalue+= probmatrix[i-1][state] * transitionprob.get(state,currstate)
# 			print stateprob.get((currstate, str(arg[4][i])))
# 			print currstate
# 			print str(arg[4][i])
# 			probmatrix[i][currstate] = reqvalue*stateprob.get((currstate, str(arg[4][i])))
# 			probmatrixlog[i][currstate] = math.log(probmatrix[i][currstate]) if probmatrix[i][currstate]!=0 else -1000000 
# 	states = transitionmap.get(statespossible[arg[1]+1])
# 	reqvalue = 0
# 	for state in states:
# 		reqvalue+= probmatrix[arg[1]][state] * transitionprob.get(state,arg[1]+1)
# 	probmatrix[-1][arg[1]+1] = reqvalue
# 	probmatrixlog[-1][arg[1]+1] = math.log(probmatrix[i][currstate]) if probmatrix[i][currstate]!=0 else -1000000 


# getInput()
# findprob()
# print(probmatrixlog)




def main():
	getInput()

	for pos in range (1, len(arg[4])+1):
		f[pos][0] = 0
	for state in statespossible[1:]:
		f[0][state] = 0
	f[0][0] = 1

	for pos in range (1, len(arg[4])+2):
		for state in statespossible[1:]:
			totalfprob = 0.0
			for prevstate in statespossible:
				tp = 0.0 if transitionprob.get((prevstate,state))==None else transitionprob.get((prevstate,state)) 
				fprob = f[pos-1][prevstate]*tp
				totalfprob = totalfprob + fprob
			if state == statespossible[-1] or pos == len(arg[4])+1:
				f[pos][state] = totalfprob
			else:
				# print state
				# print pos
				# print arg[4][pos-1]
				# print stateprob.get((state,arg[4][pos-1]))
				f[pos][state] = stateprob.get((state,arg[4][pos-1]))*totalfprob
	# printoutput(len(arg[4])+1, arg[1]+1)
	for pos in range (1, len(arg[4])+1):
		for state in statespossible[1:-1]:
			if f[pos][state]==0:
				print -1000000.00,
			else:
				# print pos
				# print state
				lop_p = math.log(f[pos][state])
				print "%.2f" % lop_p,
		print '\n',
	print "%.2f" % math.log(f[len(arg[4])+1][statespossible[-1]])
main()
