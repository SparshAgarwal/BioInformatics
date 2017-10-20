
from collections import defaultdict
import collections
# for file in {'2_14','3_3','3_4','3_5','3_10','3_20','3_60','4_60','5_100','10_1000'}:
for file in {'zika'}:
	with open('test_cases/'+file+'.kmers.txt') as f:
		print(file)
		lines = f.read().splitlines()
		edges = list()
		for line in lines:
			edges.append( (line[0:(len(line)-1)],line[1:len(line)]))
	##print(edges)

	degrees = defaultdict(int)
	for k,v in edges:
		degrees[k] += 1
		degrees[v] -= 1

	source = [k for k, v in degrees.items() if v == 1]
	source = [] if len(source)==0 else source[0]
	##print(source)
	sinc = [k for k, v in degrees.items() if v == -1]
	sinc = [] if len(sinc)==0 else sinc[0]
	##print(sinc)

	#print 'source: %s, sinc: %s' % (source, sinc)
	flag = 0
	if len(source)!=0:
		edges.append((sinc,source))
		flag = 1
	#print(edges)
	edges.sort()
	#print(edges)

	graph = defaultdict(list)
	for edge in edges:
		#print(edge)
		graph[edge[0]].append(edge[1])
	#print(graph)
	graph = collections.OrderedDict(sorted(graph.items()))
	#print(graph)

	cycles = []
	current = next(iter(graph))
	while graph:
		
		#print(current)
		cycle = [current]
		#print(type(cycle))
		#print(cycle)
		while current in graph:
			next_ = graph[current][0]
			#print(next_)
			del graph[current][0]
			#print(graph)
			if len(graph[current]) == 0:
				del graph[current]
			current = next_
			#print(type(cycle))
			cycle.append(next_)
			if(len(cycle)!=1 and cycle[0]==next_):
				if len(cycles) == 0:
					cycles[0:len(cycle)] = cycle
					cycle=[cycle[-1]]
				else:
					cycles[cycles.index(cycle[0]):cycles.index(cycle[0])] = cycle[:-1]
					cycle=[cycle[-1]]
			#print(cycle)
			#print("cycles: ")
			#print(cycles)
			##print("inner loop")
		if(len(cycle)!=0):
			cycles[cycles.index(cycle[0]):cycles.index(cycle[0])] = cycle[:-1]
		##print(len(graph))
		for k in cycles:
			##print("hello")
			if k in graph:
				current = k
				break
		###print("outer loop")
	##print(cycles)



	# boarder = 1
	# for i in range(1, len(cycles)):
	#     if cycles[i-1] == sinc and cycles[i] == source:
	#         boarder = i
	#         break
	#         ##print("boarder:",boarder)
	# if flag == 1:
	# 	path = cycles[boarder:]+cycles[1:boarder]
	# else:
	# 	path = cycles
	# ##print(path[0][:-1], end="")
	# final = path[0][:-1]
	# for k in path:
	# 	final+=k[-1]
	# 	##print(k[-1], end="")
	# # print(final)
	# with open('test_cases/'+file+'.assembly.txt') as f:
	# 	lines = f.read().splitlines()
	# 	if lines[0] != final:
	# 		print("diff")
	# 	else:
	# 		print("same")

	boarder = 1
	for i in range(1, len(cycles)):
	    if cycles[i-1] == sinc and cycles[i] == source:
	        boarder = i
	        break
	        ##print("boarder:",boarder)
	if flag == 1:
		path = cycles[boarder:]+cycles[1:boarder]
	else:
		path = cycles
	##print(path[0][:-1], end="")
	final = path[0][:-1]
	for k in path:
		final+=k[-1]
		##print(k[-1], end="")
	with open('test_cases/'+file+'.reference.txt') as f:
		lines = f.read().splitlines()
		for index,element in enumerate(zip(final,lines[0])):
			#print(index, element[0],element[1])
			if element[0] != element[1]:
				print(element[0],element[1], index)