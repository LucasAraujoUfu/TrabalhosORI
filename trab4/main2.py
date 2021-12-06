import numpy as np
import matplotlib.pyplot as plt
import sys


arq = open(sys.argv[1],'r')

n = int(arq.readline().split()[0])

print(n)

r = []

for i in range(n):
	line = arq.readline()
	r.append(line.split())

q = []

for i in range(n):
	line = arq.readline()
	q.append(line.split())

num = [0]*n

for i in range(len(q)):
	for j in q[i]:
		if j in r[i]:
			num[i]+=1

val = []

for i in range(len(num)):
	val.append(list())

for	i in range(len(num)): 
	for j in [1.,.9,.8,.7,.6,.5,.4,.3,.2,.1]:
		val[i].append(int(j*num[i]))

pre = np.zeros((n,11))
rev = np.zeros((n,11))

for i in range(len(q)):
	ca=0
	P = {}
	R = {}
	for j in range(len(q[i])):
		if q[i][j] in r[i]:
			ca+=1
			if ca in val[i]:
				P[ca] = (ca/(j+1))
				R[ca] = (ca/len(r))
	
	ct=0
	for j in val[i]:
		pre[i][ct] = P[j]
		rev[i][ct] = R[j]
		ct+=1

print(pre)
print(rev)
	
