import gensim
import nltk


input_str = 'like singing music'

model = gensim.models.Word2Vec.load('/tmp/word2vec_100_break')
tagged = nltk.word_tokenize(input_str)
print tagged
for elem in tagged:
    print model[elem]

print "total: "
print model[tagged]
