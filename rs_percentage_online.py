import sqlite3
import pprint
import sentiment
import pickle
import sys
import numpy as np
def most_common(lst):
        return max(set(lst), key=lst.count)

conn = sqlite3.connect('rs_ratings.db')
c = conn.cursor()
c.execute('''SELECT * FROM responses''')
'''
table_num = {}
table_sum = {}
table_entry = {}
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
        table_entry[key].append(score)
    else:
        table_sum[key] = score
        table_num[key] = 1
        table_entry[key] = [score]
# create the table we need.
print len(c.fetchall())
print table_entry
with open('table_value_new.pkl','wb') as f:
    pickle.dump(table_sum,f)
    pickle.dump(table_num,f)
    pickle.dump(table_entry,f)
#print table_sum
sys.exit()
'''
with open('table_value_new.pkl') as f:
    table_sum = pickle.load(f)
    table_num = pickle.load(f)
    table_entry = pickle.load(f)
entry_4 = ['end','switch','init','joke','more']
entry_1 = ['pos','neg','neutral']
for strategy in entry_4:
    key = ('neg','neg','neg',unicode(strategy,'utf-8'))
    key_1 = ('neg','neutral','neg',unicode(strategy,'utf-8'))
    print key
    if key_1 in table_entry.keys():
        print table_entry[key]+table_entry[key_1]
    else:
        print table_entry[key]

for strategy in entry_4:
    key = ('pos', 'pos','pos',unicode(strategy,'utf-8'))
    if key in table_entry.keys():
        print key
        print table_entry[key]
        value = table_entry[key]
        for i in range(1,4):
            print len(np.where(np.array(value)==i)[0])/float(len(value))


for strategy in entry_4:
    key = ('neg','neg','neg',unicode(strategy,'utf-8'))
    key_1 = ('neg','neutral','neg',unicode(strategy,'utf-8'))
    print key
    if key_1 in table_entry.keys():
        print table_entry[key]+table_entry[key_1]
    else:
        print table_entry[key]
        print table_entry[key]
entry_1 = ['neutral','neg']
for strategy in entry_4:
    strategy_sum =[]
    for sent_1 in entry_1:
        for sent_2 in entry_1:
            key = (sent_1,sent_2,'neg', unicode(strategy, 'utf-8'))
            if key in table_entry.keys():
                strategy_sum.append(table_entry[key])
    print strategy
    print strategy_sum
sys.exit()
entry_2 = entry_1
entry_3 = entry_2
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
                    table_avg[key] = 1
                print (item_1 +' , ' + item_2 +' , '+ item_3 +' , '+ item_4 + ' , ' + str(value_avg) + ' , ' + str(value_num)+'\n' )

print '-----------'
for key in  table_avg.keys():
    print key
    print '\n'

# save a dictionary that for each situation, pick the one with highest value average.
with open('table_state_strategy_new.pkl','wb') as f:
    pickle.dump(table_state_strategy,f)
'''
for item in entry_4:
    print item + str(table_avg['neg','neg','neg',item])
#a = c.fetchall()
#pprint.pprint(a)
'''
