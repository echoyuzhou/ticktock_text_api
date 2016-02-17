import logging, gensim
from gensim import corpora,models
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
id2word = corpora.Dictionary.load('/tmp/deerwester.dict')
mm = gensim.corpora.MmCorpus('/tmp/deerwester.mm')
#lsi = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=id2word,num_topics =10)
#lsi.print_topics(10)
lda = gensim.models.ldamodel.LdaModel(corpus=mm,id2word = id2word,num_topics=10,update_every=1,chunksize=10, passes=1)
lda.print_topics(10)
