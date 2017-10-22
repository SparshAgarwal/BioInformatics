from collections import defaultdict

with open('1-kmers.txt') as f:
	lines = f.read().splitlines()
	edges = list()
	for line in lines:
		edges.append( (line[0:(len(line)-1)],line[1:len(line)]))

edges.sort()
print(edges)

graph = defaultdict(list)
for edge in edges:
	graph[edge[0]].append(edge[1])

# edges = [(k,v) for k, v in graph.items() ]
# graph = {x: y for x, y in edges}
# print(type(graph))
print(graph)

degrees = defaultdict(int)
for k in graph:
	for v in graph[k]:
		degrees[k] += 1
		degrees[v] -= 1
for k, v in degrees.items():
	print(k,v)

source = [k for k, v in degrees.items() if v == 1]
print(source)
sinc = [k for k, v in degrees.items() if v == -1]
print(sinc)
#print 'source: %s, sinc: %s' % (source, sinc)

# if sinc in graph.keys():
# 	graph[sinc].append(source)
# else:
# 	graph[sinc] = [source]


# cycles= {}
# while graph:




cycles = {}
while graph:
	current = next(iter(graph))
	print(current)
	cycle = [current]
	print(cycle)
	cycles[current] = cycle
	while current in graph:
		next_ = graph[current][0]
		print(next_)
		del graph[current][0]
		if len(graph[current]) == 0:
			del graph[current]
		current = next_
		cycle.append(next_)



def traverse(tree, root):
	out = []
	for r in tree[root]:
		if r != root and r in tree:
			out += traverse(tree, r)
		else:
			out.append(r)
	return out

print(cycle)

cycle = traverse(cycles, 0)
for i in range(1, len(cycle)):
	if cycle[i-1] == sinc and cycle[i] == source:
		boarder = i
path = cycle[boarder:]+cycle[1:boarder]
print ('->'.join([str(i) for i in path]))