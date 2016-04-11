import sqlite3
import pprint
import sentiment
import pickle

def most_common(lst):
        return max(set(lst), key=lst.count)

conn = sqlite3.connect('rs_ratings.db')
c = conn.cursor()
c.execute('''SELECT * FROM responses''')
table_num = {}
table_sum = {}
tmplist =[]
for item in c.fetchall():
    print item
    #print item[0]
    #break
    turn_1_user_sent = sentiment.get_sentiment(item[0])
    turn_1_tt_sent = sentiment.get_sentiment(item[1])
    turn_0_user_sent = sentiment.get_sentiment(item[7])
    turn_0_tt_sent = sentiment.get_sentiment(item[8])
    turn_str = item[10]
    if item[11] == None or item[12] == None or item[13] ==None:
        break
    score_list = [ item[11], item[12], item[13] ]
    score = most_common(score_list)
    tmplist.append([turn_0_user_sent,turn_0_tt_sent,turn_1_user_sent,turn_str,score])
    key = (turn_0_user_sent, turn_0_tt_sent,turn_1_user_sent,turn_str)
    if table_sum.has_key(key):
        table_sum[key]= table_sum[key]+score
        table_num[key] = table_num[key]+1
    else:
        table_sum[key] = score
        table_num[key] = 1
# create the table we need.
print table_sum
'''
with open('table_value.pkl') as f:
    table_sum = pickle.load(f)
    table_num = pickle.load(f)
    table_avg = pickle.load(f)
'''
entry_1 = ['pos','neg','neutral']
entry_2 = entry_1
entry_3 = entry_2
entry_4 = ['end','switch','init','joke','more']
table_avg = {}
table_state_strategy = {}
for item_1 in entry_1:
    for item_2 in entry_2:
        for item_3 in entry_3:
            high_avg=0
            for item_4 in entry_4:
                key = (item_1,item_2,item_3,item_4)
                if table_sum.has_key(key):
                #try:
                #print table_sum[(item_1,item_2,item_3,item_4)]
                    value_sum = table_sum[key]
                #print value_sum
                    value_num = table_num[key]
                    value_avg = float(value_sum)/float(value_num)
                    table_avg[key] = value_avg
                    if high_avg < value_avg:
                        table_state_strategy[(item_1,item_2,item_3)] = item_4
                        high_avg = value_avg
                else:
                    value_sum = 0
                    value_num = 0
                    value_avg = 0
                    table_state_strategy[(item_1,item_2,item_3)] = 'end'
                print (item_1 +' , ' + item_2 +' , '+ item_3 +' , '+ item_4 + ' , ' + str(value_avg) + ' , ' + str(value_num)+'\n' )
# save a dictionary that for each situation, pick the one with highest value average.
with open('table_state_strategy.pkl','wb') as f:
    pickle.dump(table_state_strategy,f)

with open('table_value.pkl','wb') as f:
    pickle.dump(table_sum,f)
    pickle.dump(table_num,f)
    pickle.dump(table_avg,f)
#a = c.fetchall()
#pprint.pprint(a)

