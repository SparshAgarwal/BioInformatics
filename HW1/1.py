with open('1-kmers.txt') as f:
	lines = f.read().splitlines()
	edges = list()
	for line in lines:
		edges.append( [line[0:(len(line)-1)],line[1:len(line)]])
	for edge in edges:
		print(edge)