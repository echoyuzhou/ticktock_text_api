from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
corpus = corpora.MmCorpus('/tmp/deerwester.mm')
lsi = models.LsiModel(corpus, id2word=dictionary,num_topics=2)
doc = "l love swimming"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]
print(vec_lsi)
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('/tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
sims = index[vec_lsi]
sims = sorted(enumerate(sims),key=lambda item: -item[1])# sort into descending order
print sims[0] 
