import sys
import nltk

arq = open(sys.argv[1],'r')

kw = nltk.corpus.stopwords.words('portuguese')+[',','.','..','...','!','?']

rad = nltk.stem.RSLPStemmer()
se = nltk.corpus.mac_morpho.tagged_sents()
un = nltk.tag.UnigramTagger(se)

m = {}

ca = 1

for a in arq:
	if a.find('\n')!=-1:
		a = a[:-1]

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
	#verrificar se cada palavra é preposição, conjunção ou artigo APRENDE a LER
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

arqw = open('indice.txt','w')

for i in m:
	saux=""
	for j in m[i]:
		saux += " {},{}".format(j,m[i][j])
	arqw.write(i+':'+saux+'\n')

#print(sorted(m))
