import nltk
sent = nltk.corpus.treebank.tagged_sents()[22]
print(nltk.ne_chunk(sent,binary=True))
