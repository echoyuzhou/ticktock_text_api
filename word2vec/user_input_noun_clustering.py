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

stoplist = stopwords.words('english')+['d','dd','ddd','dddd']
print stoplist
#texts =[[word for word in ' '.join(document).lower().split() if word not in stoplist] for document in documents]
with open('contraction.pkl') as f:
	contractions = pickle.load(f)
texts_stemmed = []
texts_all = []
n_pronoun = []
n_word = []
noun_list ={'NN':[],'NNS':[],'NNP':[],'NNPS':[]}
for document in documents:
        print document
        pos_tag_list = nltk.pos_tag(nltk.word_tokenize(document))
        print pos_tag_list
        for pos_tag_name in pos_tag_list:
            #print pos_tag_name
            if pos_tag_name[1] in ['NN','NNS','NNP','NNPS']:
                #print pos_tag_name
                noun_list[pos_tag_name[1]].append(pos_tag_name[0])
#noun_list_lower = [item.lower() for item in noun_list]
with open('noun_list.pkl','w') as f:
    pickle.dump(noun_list,f)
#fdist = nltk.FreqDist(noun_list_lower)
#print fdist.most_common(50)

# here let us try, if we git rid of all the usual words shown
freqwordlist = ['hello','favorite','sure','like','what','think','know','do','hi']
dictionary = corpora.Dictionary(noun_list_lower)
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
lda = gensim.models.ldamodel.LdaModel(corpus=mm,id2word = id2word,num_topics=10,update_every=0,chunksize=10, passes=20)
lda.print_topics(10)
