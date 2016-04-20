import sentiment_online
import sentiment_vader
import pickle
f = open('test_sentiment.txt','w')
all_conversation = pickle.load(open('all_conversation.pkl'))
id =1
for utt in all_conversation:
    id = id+1
    sent = sentiment_online.get_sentiment(utt)
    sent_vader = sentiment_vader.get_sentiment(utt)
    f.write('utterance:' + utt +'\n')
    f.write('online:' + sent +'\n' )
    f.write('vader:' + sent_vader+'\n')
    f.write('\n')
    if id >1000:
        break
