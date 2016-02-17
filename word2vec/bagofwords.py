import logging
from nltk.corpus import stopwords
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora,models, similarities
documents=[]
with open('documents.txt') as f:
	for line in f:
		documents.append(line)

stoplist = stopwords.words('english')
print stoplist
texts =[[word for word in document.lower().split() if word not in stoplist] for document in documents]

from pprint import pprint
#pprint(texts)
dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict')
#print(dictionary)
#print(dictionary.token2id)
new_doc = "Sara loves animals"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print "we are pring the new vec"
print(new_vec)
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm',corpus)
tfidf = models.TfidfModel(corpus)
print "we are printing the tfidf of the new vec"
print(tfidf[new_vec])
tfidf.save('/tmp/foo.tfidf_model')

