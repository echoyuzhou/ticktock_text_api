import logging
import re
import pickle
from nltk.corpus import stopwords
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora,models, similarities
#def oov_out(user_input, dictionry_value):
#	print user_input
	#documents=[]
	#with open('documents.txt') as f:
	#	for line in f:
	#		documents.append(line)
#	stoplist = stopwords.words('english')
	#texts =[[word for word in document.lower().split() if word not in stoplist] for document in documents]
dictionary = corpora.Dictionary.load('/tmp/deerwester.dic')
dictionary_value = dictionary.values()
with open('dictionary_value.pkl','w') as f:
	pickle.dump(dictionary_value,f)

