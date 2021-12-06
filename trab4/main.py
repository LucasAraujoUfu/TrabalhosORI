import numpy as np
import matplotlib.pyplot as plt
import sys
import math


arq = open(sys.argv[1],'r')

n = int(arq.readline().split()[0])

#print(n)

r = []

for i in range(n):
	line = arq.readline()
	r.append(line.split())

q = []

for i in range(n):
	line = arq.readline()
	q.append(line.split())

val = []

for i in range(n):
	val.append(list())

for	i in range(n): 
	for j in [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.]:
		val[i].append(math.ceil(j*len(r[i])))

pre = np.zeros((n,11))
rev = np.zeros((n,11))

Map = []
Mar = []

for i in range(n):
	Map.append({0:0})
	Mar.append({0:0})

for i in range(len(q)):
	ca=0
	for j in range(len(q[i])):
		if q[i][j] in r[i]:
			ca+=1
			if ca in val[i]:
				Map[i][ca]= ca/(j+1)
				Mar[i][ca]= ca/len(r[i])

#print(Map)
#print(Mar)
print(val)

for i in range(n):
	for j in range(len(val[i])):
	  if val[i][j] not in Map[i]:
	    Map[i][val[i][j]] = 0
	    Mar[i][val[i][j]] = val[i][j]/len(r[i])
	  pre[i][j]=Map[i][val[i][j]]
	  rev[i][j]=Mar[i][val[i][j]]

for i in range(n):
  mC=0
  for j in range(len(pre[i])-1,-1,-1):
    if pre[i][j]<mC:
      pre[i][j]=mC
    else:
      mC = pre[i][j]

#print(pre)
#print(rev)

avg = np.zeros(11)

for i in range(11):
  soma = 0
  for j in range(n):
    soma += pre[j][i]
  avg[i] = soma/n

mC=0
for j in range(len(avg)-1,-1,-1):
  if avg[j]<mC:
    avg[j]=mC
  else:
    mC = avg[j]
  
for i in range(n):
	plt.plot([0,10,20,30,40,50,60,70,80,90,100],pre[i])
	#plt.plot(rev[i],pre[i])
	plt.show()

plt.plot([[0,10,20,30,40,50,60,70,80,90,100],avg)
plt.show()

arqS = open('media.txt','w')
for i in range(11):
  if i != 0:
    arqS.write(' ')
  arqS.write(str(avg[i]))
arqS.write('\n')

