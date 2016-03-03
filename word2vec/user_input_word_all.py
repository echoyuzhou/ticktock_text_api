import logging, gensim, pickle, re
from gensim import corpora,models
from nltk.corpus import stopwords
import nltk
from nltk.stem.lancaster import LancasterStemmer
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora,models, similarities
pronounlist = ['he','she','his','her','him','they','their','them','it','its','we','our','us','you','your']
with open('user_input_v1.txt') as f:
	documents = f.readlines()

stoplist = [stopwords.words('english'),'d','dd','ddd','dddd']
print stoplist
#texts =[[word for word in ' '.join(document).lower().split() if word not in stoplist] for document in documents]
with open('contraction.pkl') as f:
	contractions = pickle.load(f)
texts_stemmed = []
texts_all = []
n_pronoun = []
n_word = []
for document in documents:
        print document
        n_word_i = 0
        n_pronoun_i =0
        texts_stemmed = []
	for text in document.split():
		text = re.sub('[?!,.]', ' ', text)
		text = text.lower()
                n_word.append(len(text))
		#text = LancasterStemmer().stem(text)
			#texts_stemmed.append(text)
		if text in contractions.keys():
			text = contractions[text].split()
			print text
			if type(text) is list:
				for text_i in text:
					if text_i not in stoplist:
						texts_stemmed.append(text_i)
                                        if text_i in pronounlist:
                                                n_pronoun_i = n_pronoun_i + 1
			else:
				if text not in stoplist:
					texts_stemmed.append(text)
                                if text in pronounlist:
                                        n_pronoun_i = n_pronoun_i + 1
		else:
			if text not in stoplist:
				texts_stemmed.append(text)
                        if text in pronounlist:
                                n_pronoun_i = n_pronoun_i +1
                n_pronoun.append(n_pronoun_i)
        print "this is one document"
        texts_all.append(texts_stemmed)

print "pronoun percentage"
print sum(n_pronoun)
print sum(n_word)
print float(sum(n_pronoun))/float(sum(n_word))
print 'this is the texts_all'
fdist = nltk.FreqDist([item for sublist in texts_all for item in sublist])
print fdist.most_common(50)

with open('texts_all.txt','w') as f:
	for texts in texts_all:
		f.write( ' '.join(texts) +'\n')
# here let us try, if we git rid of all the usual words shown
freqwordlist = ['hello','favorite','sure','like','what','think','know','do','hi']
text_all_nf =[]
for text_all_i in texts_all:
    #print text_all_i
    #if text_all_i.find(' '):
        #text = text_all_i.split()
    text_filter = [w for w in text_all_i if not w in freqwordlist]
    text_all_nf.append(text_filter)

#dictionary = corpora.Dictionary(texts_all)
dictionary = corpora.Dictionary(text_all_nf)
print "we are printing the dictionary"
print dictionary

dictionary.save('user_input.dict')
new_doc = "i like to watch movies"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print "we are printing the new vec"
print(new_vec)
corpus = [dictionary.doc2bow(text) for text in text_all_nf]
corpora.MmCorpus.serialize('user_input.mm',corpus)
id2word = dictionary
mm = corpus
#lda = gensim.models.ldamodel.LdaModel(corpus=mm,id2word = id2word,num_topics=10,update_every=0,chunksize=10, passes=20)
#lda.print_topics(10)
