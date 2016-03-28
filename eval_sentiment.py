import sentiment
import pickle
import readall

rating_logs = readall.readall("/home/ubuntu/zhou/Backend/rating_log/")
user_input  = readall.get_log(rating_logs)
'''
with open('user_input_v2.pkl') as ff:
    user_input = pickle.load(ff)
'''
f = open ('sentiment_log.txt','w')
sentiment_label = []
for turn in user_input:
    question = turn['question']
    label = sentiment.get_sentiment(question)
    sentiment_label.append(label)
    f.write(question+'\n')
    f.write('sentiment: '+ label + '\n')

pos_number = sentiment_label.count('pos')
print pos_number
neg_number = sentiment_label.count('neg')
print neg_number
neutral_number = sentiment_label.count('neutral')
print neutral_number
