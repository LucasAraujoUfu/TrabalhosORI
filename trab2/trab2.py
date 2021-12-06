import sys
import nltk


rad = nltk.stem.RSLPStemmer()
nArqC = set()
mArq = {}


def indiceInvertido(path):
	'''
		função que monta o indice invertido da base de dados, informando a frequncia da palavra por arquivo
	
		@param path string, caminho para o arquivo que contem a lista de arquivos que compõe a base
		
		@return dicionario, com os radicais das palavras e suas respectivas aparições em cada arquivo
	'''
	arq = open(path,'r')

	kw = nltk.corpus.stopwords.words('portuguese')+[',','.','..','...','!','?']

	se = nltk.corpus.mac_morpho.tagged_sents()
	un = nltk.tag.UnigramTagger(se)

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
		



def salvaIndice(m,nome='indice.txt'):
	'''
		Função que salva um indice invertido gerado pela função indiceInvertido() em um arquivo
		
		@param m dicionario retornado pela função de indice invertido
		@param nome string, nome do arquivo onde será salvo
		
	'''
	arqw = open(nome,'w')

	for i in m:
		saux=""
		for j in m[i]:
			saux += " {},{}".format(j,m[i][j])
		arqw.write(i+':'+saux+'\n')
		

inp = sys.argv[1]
con = sys.argv[2]

consultas = open(con,'r')

indice = indiceInvertido(inp)
salvaIndice(indice,"indice.txt")

operador = ['&','!','|']

mCon = {}

for k in consultas:
  k = str(k)
  i1 = str(k)
  i = k.split()
  #print(i)
  for j in i:
    if j[0] =='!':
      j = j[1:]
    if j not in operador:
      j = rad.stem(j)
      if j in indice:
        for k in indice[j]:
          if j not in mCon:
            mCon[j] = [k]
          else:
            mCon[j].append(k)
  if '\n' in i1:
    i1 = i1[:-1]
  i1 = i1.split('|')
  cS = set()
  for cond in i1:
    cond = cond.split()
    cST = set()
    for palavras in cond:
      fand = True
      if palavras[0]=='!':
        fand=False
        palavras = palavras[1:]
      if palavras in operador:
        continue
      palavras = rad.stem(palavras)
      if palavras in mCon:
        if len(cST)==0:
          if fand:
            cST = set(mCon[palavras])
          else:
            cST = nArqC-set(mCon[palavras])
        elif fand:
          cST = cST.intersection(set(mCon[palavras]))
        else:
          cST = cST.intersection(nArqC-set(mCon[palavras]))
      #print(cST)
    cS = cS.union(cST)

res = open('resposta.txt','w')
res.write(str(len(cS))+'\n')
for i in cS:
  res.write(mArq[i]+'\n')


