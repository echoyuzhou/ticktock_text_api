#construct the reward table.
import pickle
with open('table_value.pkl') as f:
    table_sum = pickle.load(f)
    table_num = pickle.load(f)
    table_value = pickle.load(f)
print table_value
print table_value[ ('neg','neutral','neg','init')]
reward_table={}
keys = table_value.keys()
print keys
for key in keys:
    for turn_id in range(1,12):
        state = (key[0],key[1],key[2],turn_id)
        action = key[3]
        reward_table[state,action] = (table_value[key]-1.5)*20-turn_id
#when there is null involved, we make the reward table manually
for turn_id in range(1,12):
    for action in ['joke','more','switch','end','more']:
        for state_3 in ['pos','neg','neutral']:
            reward_table[('null','null',state_3,turn_id),action] = -10
pickle.dump(reward_table,open('reward_table.pkl','w'))
#print reward_table
