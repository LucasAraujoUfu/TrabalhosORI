'''
@file pagerank.py
@author Lucas Gabriel Teodoro Araújo - 11921BSI247
@date 28/10/2021
@brief script que calcula o pagerank dos arquivos de uma base de dados111
'''
from pathlib import Path
import sys
import random

TR = 10000 # constante do número de transições aleatorias


def saveGraph(graph, name):
	'''
		Função para salvar um grafo em um arquivo de texto
		
		@param graph dicionario no formato de lista de adjacencia
		@param name nome do arquivo onde o grafo será salvo

	'''
	G = open(name,'w')
	nodes = list(graph.keys())
	nodes.sort()
	for n in nodes:
		G.write(str(n)+':')
		for j in graph[n]:
			G.write(' '+str(j))
		G.write('\n')
	G.close()


def savePageRank(pr,name):
	'''
		Função para salvar um pagerank em um arquivo de texto
		
		@param pr dicionario contendo pagerank
		@param name nome do arquivo de texto

	'''
	P = open(name,'w')
	files = list(pr.keys())
	files.sort()
	for i in files:
		P.write(str(i)+' '+str(pr[i])+'\n')
	P.close()


arq = Path(sys.argv[1]);

arqs = set()
gOut = {}
gIn = {}

for f in [x for x in arq.iterdir()]:
  fname = str(f)[len(sys.argv[1])+1:]
  arqs.add(fname)
  gOut[fname] = set()
  gIn[fname] = set()

for f in [x for x in arq.iterdir()]:
  fname = str(f)[len(sys.argv[1])+1:]
  doc = open(f,'r')
  for i in doc:
    # print(i)
    j = 0
    while j<len(i):
      pos = i.find('<a href=',j)
      # print(pos)
      if pos==-1:
        break;
      #print(fname)
      #print(i[pos:])
      tmp=''
      j = pos+1
      pos += len('<a href=')+1      
      while(i[pos]!="'" and i[pos]!='"'):
        tmp+=i[pos]
        pos+=1
      #print('\t'+tmp)
      if tmp in arqs and tmp!=fname:
        if fname in gOut:
          gOut[fname].add(tmp)
        else:
          gOut[fname] = {tmp}

for i in arqs:
  for j in gOut:
    if i in gOut[j]:
      if i in gIn:
        gIn[i].add(j)
      else:
        gIn[i] = {j}

# print(arqs)
# print(gOut)
# print(gIn)


# Calculando  o pagerank da amostragem
cam = 0
cN = list(arqs)[0]
numV = {}
while cam < TR:
	rand = random.random()
	# print(cN)
	if cN in numV:
		numV[cN]+=1
	else:
		numV[cN]=1

	if rand >= .85 or len(gOut[cN])==0:
		cN = list(arqs)[random.randrange(0,len(arqs))]
	else:
		cN = list(gOut[cN])[random.randrange(0,len(gOut[cN]))]
	cam+=1

for i in numV:
	numV[i] = numV[i]/TR

# print(numV)

# Calculando o pagerank interativo

pg = {}
opg = {}
for i in arqs:
	pg[i] = 1/len(arqs)

while True:
	d = 0.85
	for i in pg:
		opg[i]=pg[i]
	#calcular sun
	den = 0
	for i in pg:
		sun = 0
		if i in gIn:
			for j in gIn[i]:
				sun+=(opg[j]/len(gOut[j]))
		pg[i] = (1-d)/len(arqs)+d*sun
		den += pg[i]
	for i in pg:
		pg[i] = pg[i]/den
	flag = True
	for i in pg:
		# print(abs(opg[i]-pg[i]))
		if abs(opg[i]-pg[i])>10**-6:
			flag = False
			break
	if flag:
		break

# print(pg)

saveGraph(gIn,'links_destino.txt')
saveGraph(gOut,'links_origem.txt')
savePageRank(numV,'pg_amostragem.txt')
savePageRank(pg,'pg_iterativo.txt')

