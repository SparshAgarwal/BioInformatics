import sys
import collections
import math

clusters = list()
D = {}

def getInput():
	with open(sys.argv[1]) as f:
		lines = f.read().splitlines()
		for line in lines:
			values = line.split('\t')
			values = values[:2]+map(float,values[2:])
			clusters.append(values[:])

def findD(i,j):
	x = 0
	# print "again"
	# print len(clusters[i][2:])
	for index in range(2,len(clusters[i])):
		# print "hello"
		# print clusters[i][index]
		# print clusters[j][index]
		# print x
		x = x+math.pow(clusters[i][index]-clusters[j][index],2)
	return math.sqrt(x)


def fdist(A,B):
	if sys.argv[2]=='S':
		dist = 1000000000.0
	if sys.argv[2]=='C':
		dist = 0.0
	if sys.argv[2]=='A':
		dist = 0.0
	# fdist = 0
	for x in A:
		# print "in fdist"+str(x)
		for y in B:
			if sys.argv[2]=='S':
				# print D[x,y]
				if dist > D[x,y]:
					dist = D[x,y]
			if sys.argv[2]=='C':
				if dist < D[x,y]:
					dist = D[x,y]
			if sys.argv[2]=='A':
				dist = dist + D[x,y]
	if sys.argv[2]=='A':
		return dist/(len(A)*len(B))
	return dist


getInput()
for i in xrange(len(clusters)):
	for j in xrange(i+1,len(clusters)):
		if i == j :
			continue
		D[i,j] = D[j,i]=findD(i,j)
# print D
# print clusters[0][2:]

FC = [[x] for x in range(len(clusters))]
# print FC
# print len(FC)
# print int(sys.argv[3])
while len(FC)>int(sys.argv[3]):
	# print "inside"
	dist = 1000000000.0
	for i in range(len(FC)):
		for j in range(i+1,len(FC)):
			td = fdist(FC[i],FC[j])
			# print "td"+str(td)
			if dist > td:
				dist = td
				comA = FC[i]
				comB = FC[j]
	FC.remove(comA)
	# print FC
	FC.remove(comB)
	# print FC
	FC.append(comA+comB)
	# print FC
	# updateD()
	# print D
print FC

avgc = {}
for i in range(len(FC)):
	sumc = 0.0
	avgg = {}
	for j in range(len(FC[i])):
		sumg = 0.0
		for a in clusters[FC[i][j]][2:]:
			sumg = sumg+a
		clusters[FC[i][j]].append(sumg/len(clusters[FC[i][j]][2:]))
		avgg[FC[i][j]]=sumg/len(clusters[FC[i][j]][2:-1])
		sumc = sumc+avgg[FC[i][j]]
	FC[i]=sorted(avgg, key=avgg.get)
	FC[i].append(sumc/len(FC[i]))
	avgc[tuple(FC[i])]= sumc/len(FC[i][:-1])
FC = sorted(avgc, key=avgc.get)

print FC

for c in FC:
	for g in c[:-1]:
		print clusters[g][0]+'\t'+clusters[g][1]+'\t'+str("%.3f" % clusters[g][-1])
	print str("%.3f" % c[-1])+'\n'