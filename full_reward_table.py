#construct the reward table.
# make the state into a full state table with actions. turn index will be ignored, we will ignore the turn_id, just use the simple sentiment of previous states
import pickle
with open('table_value.pkl') as f:
    table_sum = pickle.load(f)
    table_num = pickle.load(f)
    table_value = pickle.load(f)
'''
print table_value
print table_value[ ('neg','neutral','neg','init')]
keys = table_value.keys()
print keys
def f(x):
    return{'oov':20,'short_answer':20,'continue':20}.get(x,'None')

for key in keys:
    for turn_id in range(1,10):
        state = (key[0],key[1],key[2])
        action = key[3]
        reward_table[state,action] = (table_value[key]-1.5)*10
'''
f={'oov':20,'short_answer':20,'continue':20,'name_entity':20}

reward_table={}
sentiment_list = ['pos','neg','neutral']
action_list =  ['joke','more','switch','end','more','oov','short_answer','name_entity','continue']
for sent_1 in sentiment_list:
    for sent_2 in sentiment_list:
        for sent_3 in sentiment_list:
            for action in action_list:
                state = (sent_1,sent_2,sent_3)
                key = (sent_1,sent_2,sent_3,action)
                if key in table_value.keys():
                    reward_table [(state,action)] = table_value[key]
                else:

                    reward_table[(state,action)] = f[action]


#when there is null involved, we make the reward table manually

#for turn_id in range(1,10):
for action in action_list:
    for state_3 in ['pos','neg','neutral']:
        if action not in f.keys():
            reward_table[('null','null',state_3),action] = -10
        else:
            reward_table[('null','null',state_3),action] = f[action]
pickle.dump(reward_table,open('full_reward_table.pkl','w'))
print reward_table
