import sys
import nltk
import math


rad = nltk.stem.RSLPStemmer()
nArqC = set()
mArq = {}

kw = nltk.corpus.stopwords.words('portuguese')+[',','.','..','...','!','?']

se = nltk.corpus.mac_morpho.tagged_sents()
un = nltk.tag.UnigramTagger(se)


def indiceInvertido(path):
	'''
		função que monta o indice invertido da base de dados, informando a frequncia da palavra por arquivo
	
		@param path string, caminho para o arquivo que contem a lista de arquivos que compõe a base
		
		@return dicionario, com os radicais das palavras e suas respectivas aparições em cada arquivo
	'''
	arq = open(path,'r')

	m = {}

	ca = 1

	for a in arq:
		if a.find('\n')!=-1:
			a = a[:-1]
		
		nArqC.add(ca)
		mArq[ca] = a

		bs = open(a,'r')

		df = bs.readlines()

		pa = []
		for i in df:
			pa += nltk.word_tokenize(i)

		for i in range(len(pa)):
			pa[i] = pa[i].lower()
			
		etq = un.tag(pa)
		
		for i in range(len(etq)):
			if etq[i][1] in ['ART','PREP','KC','KS']:
				pa.remove(etq[i][0])

		aux = list(pa)

		for i in aux:
			if i in kw:
				pa.remove(i)
		
		for i  in pa:
			i = rad.stem(i)
			if i in m:
				if ca in m[i]:
					m[i][ca] += 1
				else:
					m[i][ca] = 1
			else:
				m[i] = {ca: 1}
		ca+=1
	
	return m


def indiceConsulta(path):  # falta remover as stopwords da consulta
	'''
		Função que recebe um arquivo de consulta e retorna o indice invertido referente a ele

		@param path caminho para o arquivo de pesquisa

		@return dicionario de dicionario, indice invertido da consulta
	'''
	con = open(path,'r')
	con = con.readlines()
	con = con[0].split()
	con = set(con)
	if '&' in con:
		con.remove('&')
	# print(con)
	cInd = {}
	
	for i in con:
		i = i.lower()
		if i in kw:
			continue
		
		etq = un.tag([i])
		
		if etq[0][1] in ['ART','PREP','KC','KS']:
			continue
		
		i = rad.stem(i)
		cInd[i] = {1:1}
	
	return cInd


def calcIDF(indIv, nArq):
	'''
		Função que calcula o idf palavra por palavra de uma base de texto apartir de um indice invertido
		
		@param indIV dicionario de dicionario, indice invertido retornado pela função indiceInvertido
		@param nArq número de documentos na base

		@return dicionario onde a chave é a palavra e o valor mapeado é o idf da palavra

	'''
	idf = {}
	for i in indIv:
		idf[i] = math.log10(nArq/float(len(indIv[i])))
	return idf


def calcPeso(indIv,nArq, idf=None):
	'''
		função que recebe um indice invertido e retorna os vetores esparços de pesos tf-idf

		@param indIv dicionario retornado pela função que calcula o indice invertido
		@param nArq número de arquivos na base de documentos
		@param idf dicionario do idf pre-calculado por palavra

		@return dicionario, vetor esparço de pesos de cada arquivo

	'''

	if idf==None:
		idf = calcIDF(indIv,nArq)

	pesoP = {}

	for i in range(1,nArq+1):
		for j in indIv:
			if i in indIv[j]:
				if i in pesoP: 
					if j in idf:
						pesoP[i][j] = (1+math.log10(indIv[j][i]))*idf[j] # math.log10(nArq/float(len(indIv[j])))
					else:
						pesoP[i][j] = 0
				else:
					if j in idf:
						pesoP[i] = {j:(1+math.log10(indIv[j][i]))*idf[j]} #math.log10(nArq/float(len(indIv[j])))}
					else:
						pesoP[i] = {j:0}

	return pesoP


def compConsulta(indIv,indCs):
	'''
		função que calcula a similaridade da consulta para cada arquivo da base de textos

		@param indIv vetor de pesos dos arquivos
		@param indCs vetor de pesos da consulta

		@return dicionario onde a chave é o número do arquivo e seu valor mapeado a similaridade do mesmo com a consulta.
	'''
	sim = {}
	for j in indIv:
		num = 0
		denC = 0
		denB = 0
		for i in indCs[1]:
			if i in indIv[j]:
				num += indIv[j][i] * indCs[1][i]
			denC += indCs[1][i] * indCs[1][i]
		
		for i in indIv[j]:
			denB += indIv[j][i] * indIv[j][i]
		
		sim[j] = num/(math.sqrt(denB)*math.sqrt(denC))
	
	return sim


def verifica(vSim):
	'''
		função que verifica quais arquivos aparecerão no resultado e retorna uma lista ordenada dos arquivos de resultado

		@param vSim vetor de similaridades retornado pela função compConsulta

		@return lista de tuplas, o primeiro valor a similaridade o segundo o número do arquivo
	'''
	res = []
	for i in vSim:
		if vSim[i] > .001:
			res.append((vSim[i],i))
	res.sort()
	res.reverse()

	return res


def salvaRes(res,nome='resposta.txt'):
	'''
		função que salva a lista de arquivos que respondem a consulta em um arquivo

		@param res vetor de resposta
		@param nome nome do arquivo que se deseja salvar
		
	'''
	arqR = open(nome,'w')

	arqR.write(str(len(res))+'\n')

	for i in res:
		arqR.write(mArq[i[1]]+' '+str(i[0])+'\n')
	

def salvaTF_IDF(vetB,nome='pesos.txt'):
	'''
		função que salva o vetor de pesos da base em um arquivo

		@param vetB vetor de pesos da base
		@param nome nome do arquivo que se deseja salvar

	'''
	arqR = open(nome,'w')

	for i in vetB:
		arqR.write(mArq[i])
		for j in vetB[i]:
			if vetB[i][j] != 0:
				arqR.write(' '+j+','+str(vetB[i][j]))
		arqR.write('\n')


base = sys.argv[1]
con = sys.argv[2]

indice = indiceInvertido(base)

idf = calcIDF(indice,len(nArqC))

vetP = calcPeso(indice,len(nArqC),idf)

cI = indiceConsulta(con)

vetC = calcPeso(cI,1,idf)

sim = compConsulta(vetP,vetC)

res = verifica(sim)

salvaRes(res)
salvaTF_IDF(vetP)

# print(cI)
# print(vetP)
# print(vetC)
# print(sim)
# print(res)
