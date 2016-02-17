import gensim, logging
import pickle
from gensim.models.doc2vec import LabeledSentence


class LabeledLineSentence(object):
    #uid = 1
    def __init__(self, filename):
        self.filename = filename
    def __iter__(self):
        for label, line in enumerate(open(self.filename)):	    
	    print line
	    print label		
	    print type(line)
	    yield LabeledSentence(words=line.split(), tags= ['TXT_%s' % label])
	    #uid = uid + 1

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
#sentences = [['fisrt','sentense'],['second','sentence']]
with open('test.pkl')as f:
	sentences = pickle.load(f)
print len(sentences)
# try to print all the sentences into a txt files, jus to see how they look.

#with open('documents.txt','w') as f:
#	for sentence in sentences:
#		f.write(' '.join(sentence) +'\n')

documents = LabeledLineSentence('documents.txt')
model = gensim.models.Doc2Vec(documents, size=20, window=8, min_count=1, workers=4)
model.save('doc2vec_20')
#model = gensim.models.Doc2Vec.load('doc2vec_100')
#with open('documents.txt', 'r')as f:
array_list =[]
for sentense in sentences:
	array = model[sentense] 
	array_list.append(array)
	print array
with open('doc_vector.pkl','w') as f:
	pickle.dump(array_list,f)

#model = gensim.models.Word2Vec(sentences,min_count=1)
#model.save('model_1')
