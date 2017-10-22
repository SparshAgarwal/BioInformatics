
from collections import defaultdict
import networkx as nx
with open('1-kmers.txt') as f:
    lines = f.read().splitlines()
    edges = list()
    for line in lines:
        edges.append( (line[0:(len(line)-1)],line[1:len(line)]))

print(edges)

graph = nx.Graph()
graph.add_edges_from(edges)
print(graph.edges())
print(graph.nodes())

degrees = defaultdict(int)
for k in graph:
    print(k)
    for v in graph[k]:
        print(v)
        degrees[k] += 1
        degrees[v] -= 1
source = [k for k, v in degrees.items() if v == 1]
sinc = [k for k, v in degrees.items() if v == -1]
#print 'source: %s, sinc: %s' % (source, sinc)

if sinc in graph.nodes():
    graph.add_edge(sink,source)
else:
    graph.add_node(sink)
    graph.add_edge(sink,source)

cycles = {}
while graph:
    current = next(iter(graph))
    cycle = [current]
    cycles[current] = cycle
    while current in graph:
        next_ = graph[current][0]
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

cycle = traverse(cycles, 0)
for i in range(1, len(cycle)):
    if cycle[i-1] == sinc and cycle[i] == source:
        boarder = i
path = cycle[boarder:]+cycle[1:boarder]
print ('->'.join([str(i) for i in path]))