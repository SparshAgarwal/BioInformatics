from collections import defaultdict
import sys
import collections

arg = sys.argv
global G
global S
global match
global mismatch
global MIN
global sequ1 
global sequ2 
flag =0

#return match or mismatch score
def _match(s, t, i, j):
	if s[i-1] == t[j-1]:
		return match
	else:
		return mismatch

#initializers for matrices
def _init_x(i, j):
	if j > 0 and i == 0:
		return MIN
	else:
		if i >= 0 and j == 0:
			return G + (S * i)
		else:
			return 0

def _init_y(i, j):
	if j == 0 and i > 0:
		return MIN
	else:
		if j >= 0 and i == 0:
			return G + (S * j)
		else:
			return 0

def _init_m(i, j):
	if j == 0 and i == 0:
		return 0
	else:
		if j == 0 or i == 0:
			return MIN
		else:
			return 0

def distance_matrix(s, t):
	dim_i = len(s) + 1
	dim_j = len(t) + 1
	#abuse list comprehensions to create matrices
	X = [[_init_x(i, j) for j in range(0, dim_j)] for i in range(0, dim_i)]
	Y = [[_init_y(i, j) for j in range(0, dim_j)] for i in range(0, dim_i)]
	M = [[_init_m(i, j) for j in range(0, dim_j)] for i in range(0, dim_i)]

	for i in range(1, dim_i):
		for j in range(1, dim_j):
			X[i][j] = max((G + S + M[i-1][j]), (S + X[i-1][j]))
			Y[i][j] = max((G + S + M[i][j-1]), (S + Y[i][j-1]))
			M[i][j] = max(_match(s, t, i, j) + M[i-1][j-1], _match(s, t, i, j) + X[i-1][j-1], _match(s, t, i, j) + Y[i-1][j-1])
	# print("X")
	# print(X)
	# print("Y")
	# print(Y)
	# print("M")
	# print(M)
	return [X, Y, M]

def backtrace(s, t, X, Y, M, ele, ina, inb):
	if(ina == 0 and inb == 0):
		return
	global sequ1
	global sequ2
	global flag
	#print("---reads----")
	#print(s)
	#print(t)
	if(ele == M[ina][inb] and flag==1):
		sequ1 = s[ina-1]+sequ1
		sequ2 = t[inb-1]+sequ2
		ina -= 1; inb -= 1
		# print(sequ1)
		# print(sequ2)
		# print("10")
		# print(ele)
		# print(Y[ina][inb]+_match(s, t, ina+1, inb+1))
		# print(M[ina][inb]+_match(s, t, ina+1, inb+1))
		# print(X[ina][inb]+_match(s, t, ina+1, inb+1))
		if(ele == M[ina][inb]+_match(s, t, ina+1, inb+1)):
			# print("1")
			flag = 1
			backtrace(s,t,X,Y,M,M[ina][inb],ina,inb)
		elif(ele == X[ina][inb]+_match(s, t, ina+1, inb+1)):
			# print("2")
			flag = 2
			backtrace(s,t,X,Y,M,X[ina][inb],ina,inb)
		elif(ele == Y[ina][inb]+_match(s, t, ina+1, inb+1)):
			# print("3")
			flag = 3
			backtrace(s,t,X,Y,M,Y[ina][inb],ina,inb)
	elif(ele == X[ina][inb] and flag==2):
		sequ1 = s[ina-1]+sequ1
		sequ2 = '_'+sequ2
		ina -= 1
		# print(sequ1)
		# print(sequ2)
		# print("11")
		# print(ele)
		# print(Y[ina][inb])
		if(ele == M[ina][inb]+G+S):
			# print("4")
			flag = 1
			backtrace(s,t,X,Y,M,M[ina][inb],ina,inb)
		elif(ele == X[ina][inb]+S):
			# print("5")
			flag = 2
			backtrace(s,t,X,Y,M,X[ina][inb],ina,inb)
	elif(ele == Y[ina][inb] and flag==3):
		sequ1 = '_'+sequ1
		sequ2 = t[inb-1]+sequ2
		inb -= 1
		# print(sequ1)
		# print(sequ2)
		# print("12")
		# print(ele)
		#print(Y[ina][inb])
		if(ele == M[ina][inb]+G+S):
			# print("6")
			flag = 1
			backtrace(s,t,X,Y,M,M[ina][inb],ina,inb)
		elif(ele == Y[ina][inb]+S):
			# print("7")
			flag = 3
			backtrace(s,t,X,Y,M,Y[ina][inb],ina,inb)

lines = list()
aPair = list()
values = list()

with open(arg[1]) as f:
	lines = f.read().splitlines()
	values = lines[0].split()
	inp1 = lines[1]
	inp2 = lines[2]
	if values[0]!=0:
		for line in lines[3:]:
			if line!='':
				aPair.append(line.split())

match = float(values[1])
mismatch = -float(values[2])
G   = -float(values[3])
S   = -float(values[4])
MIN = -float("inf")

read1 = list()
read2 = list()
prevx = 0
prevy = 0
for x,y in aPair:
	read1.append(inp1[prevx:int(x)-1])
	read1.append(inp1[int(x)-1])
	prevx = int(x)
	read2.append(inp2[prevy:int(y)-1])
	read2.append(inp2[int(y)-1])
	prevy = int(y)
read1.append(inp1[prevx:])
read2.append(inp2[prevy:])
# print(read1)
# print(read2)

frList = list()
for a,b in zip(read1,read2):
	alen = len(a)
	blen = len(b)
	sequ1 = ''
	sequ2 = ''
	[X, Y, M] = distance_matrix(a, b)
	if(max(X[alen][blen],Y[alen][blen],M[alen][blen])==M[alen][blen]):
		flag = 1
		backtrace(a, b, X, Y, M, M[alen][blen],alen,blen)
	elif(max(X[alen][blen],Y[alen][blen],M[alen][blen])==X[alen][blen]):
		flag = 2
		backtrace(a, b, X, Y, M, X[alen][blen],alen,blen)
	elif(max(X[alen][blen],Y[alen][blen],M[alen][blen])==Y[alen][blen]):
		flag = 3
		backtrace(a, b, X, Y, M, Y[alen][blen],alen,blen)
	frList.append([sequ1, sequ2])

first = ''
second = ''

for x,y in frList:
	first = first+x;
	second = second+y;
print(first)
print(second)