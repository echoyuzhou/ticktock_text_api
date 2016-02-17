import logging, gensim, pickle, re
from gensim import corpora,models
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora,models, similarities
with open('user_input_v1.txt') as f:
	documents = f.readlines()
print documents
#with open ('test_v2_user_input.pkl') as f:
#	documents = pickle.load(f)
#with open('user_input.txt','w') as f:
#	for doc in documents:
#		f.write(' '.join(doc)+'\n')
#		documents.append(line)

stoplist = stopwords.words('english')
#print stoplist
#texts =[[word for word in ' '.join(document).lower().split() if word not in stoplist] for document in documents]
#from pprint import pprint
#pprint(texts)
# do a pass of stemming,
#print type(texts)
#print type(texts[0])
with open('contraction.pkl') as f:
	contractions = pickle.load(f)
texts_stemmed = []
texts_all = []
for document in documents:
	for text in document.split():
		text = re.sub('[?!,.]', ' ', text)
		text = text.lower()
		#text = LancasterStemmer().stem(text)
			#texts_stemmed.append(text)
		if text in contractions.keys():
			text = contractions[text].split()
			print text
			if type(text) is list:
				for text_i in text: 
					if text not in stoplist:
						texts_stemmed.append(text_i)
			else:
				if text not in stoplist:
					texts_stemmed.append(text)
		else:
			if text not in stoplist:
				texts_stemmed.append(text)
	texts_all.append(texts_stemmed)
with open('texts_all.txt','w') as f:
	for texts in texts_all:
		f.write( ' '.join(texts) +'\n')

dictionary = corpora.Dictionary(texts_all)
print "we are printing the dictionary"
print dictionary
dictionary.save('user_input.dict')
#print(dictionary)
#print(dictionary.token2id)
new_doc = "i like to watch movies"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print "we are printing the new vec"
print(new_vec)
corpus = [dictionary.doc2bow(text) for text in texts_all]
corpora.MmCorpus.serialize('user_input.mm',corpus)
#tfidf = models.TfidfModel(corpus)
#print "we are printing the tfidf of the new vec"
#print(tfidf[new_vec])
#tfidf.save('user_input_tfidf_model')
id2word = dictionary
mm = corpus
#id2word = corpora.Dictionary.load('/tmp/deerwester.dict')
#mm = gensim.corpora.MmCorpus('/tmp/deerwester.mm')
#lsi = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=id2word,num_topics =10)
#lsi.print_topics(10)
lda = gensim.models.ldamodel.LdaModel(corpus=mm,id2word = id2word,num_topics=5,update_every=0,chunksize=10, passes=20)
lda.print_topics(5)
