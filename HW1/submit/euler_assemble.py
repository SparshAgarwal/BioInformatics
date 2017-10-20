from collections import defaultdict
import sys
import collections
arg = sys.argv
with open(arg[1]) as f:
	lines = f.read().splitlines()
	edges = list()
	for line in lines:
		edges.append( (line[0:(len(line)-1)],line[1:len(line)]))

degrees = defaultdict(int)
for k,v in edges:
	degrees[k] += 1
	degrees[v] -= 1

start = [k for k, v in degrees.items() if v == 1]
start = [] if len(start)==0 else start[0]
last = [k for k, v in degrees.items() if v == -1]
last = [] if len(last)==0 else last[0]

flag = 0
if len(start)!=0:
	edges.append((last,start))
	flag = 1
edges.sort()

graph = defaultdict(list)
for edge in edges:
	graph[edge[0]].append(edge[1])
graph = collections.OrderedDict(sorted(graph.items()))

cycles = []
current = next(iter(graph))
while graph:
	cycle = [current]
	while current in graph:
		next_ = graph[current][0]
		del graph[current][0]
		if len(graph[current]) == 0:
			del graph[current]
		current = next_
		cycle.append(next_)
		if(len(cycle)!=1 and cycle[0]==next_):
			if len(cycles) == 0:
				cycles[0:len(cycle)] = cycle
				cycle=[cycle[-1]]
			else:
				cycles[cycles.index(cycle[0]):cycles.index(cycle[0])] = cycle[:-1]
				cycle=[cycle[-1]]
	if(len(cycle)!=0):
		cycles[cycles.index(cycle[0]):cycles.index(cycle[0])] = cycle[:-1]
	for k in cycles:
		if k in graph:
			current = k
			break

border = 1
for i in range(1, len(cycles)):
    if cycles[i-1] == last and cycles[i] == start:
        border = i
        break
if flag == 1:
	path = cycles[border:]+cycles[1:border]
else:
	path = cycles
genome = path[0][:-1]
for k in path:
	genome+=k[-1]
print(genome)