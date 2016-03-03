import gensim, logging
import pickle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
#sentences = [['fisrt','sentense'],['second','sentence']]
with open('test_complete.pkl')as f:
	sentences = pickle.load(f)
print len(sentences)
#model = gensim.models.Doc2Vec(sentences, size=100, window=8, min_count=1, workers=4)
#model.save('/tmp/doc2vec_50')
model = gensim.models.Word2Vec(sentences,min_count=1)
model.save('/tmp/word2vec_50')
