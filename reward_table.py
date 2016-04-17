#construct the reward table.
import pickle
with open('table_value.pkl') as f:
    table_sum = pickle.load(f)
    table_num = pickle.load(f)
    table_value = pickle.load(f)
reward_table={}
keys = table_value.keys()
for key in keys:
    for turn_id in range(1,10):
        state = (key[0],key[1],key[2],turn_id)
        action = key[3]
        reward_table[state,action] = table_value[key]
pickle.dump(reward_table,open('reward_table.pkl','w'))
#print reward_table
