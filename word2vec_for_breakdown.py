import gensim, logging
import pickle
import readall
import nltk
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
all_v1 = readall.readall('/home/ubuntu/zhou/Backend/rating_log/v1')
all_v2 = readall.readall('/home/ubuntu/zhou/Backend/rating_log/v2')
all_v3 = readall.readall('/home/ubuntu/zhou/Backend/rating_log/v3')
all_logs = dict(all_v1.items() + all_v2.items() + all_v3.items())
sentences =[]
user_input = []
for item in all_logs:
        #print item
        conv = all_logs[item]["Turns"]
        for turn in conv:
                sentences.append(nltk.word_tokenize(conv[turn]["You"]))
                sentences.append(nltk.word_tokenize(conv[turn]["TickTock"]))
                user_input.append(conv[turn]["You"])
#print len(sentences)
#print sentences
model = gensim.models.Word2Vec(sentences,size =100, min_count=1)
model.save('/tmp/word2vec_100_break')
with open('user_input_all.pkl','w') as f:
    pickle.dump(user_input,f)
