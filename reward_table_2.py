#construct the reward table.
import pickle
with open('table_value.pkl') as f:
    table_sum = pickle.load(f)
    table_num = pickle.load(f)
    table_value = pickle.load(f)
#print table_value
#print table_value[ ('neg','neutral','neg','init')]
reward_table={}
keys = table_value.keys()
print keys
state_3 = ['']
for turn_id in range(1,12):
    for action in ['joke','more','switch','end','more']:
        for state_3 in ['pos','neg','neutral']:
            table_value[('null','null',state_3,action)] = 0
# the state looks like:
action_list = ['switch','init','joke','more','end','oov','short_answer','name_entity','not_repeat','continue']
#(sent_1,sent_2,sent_3,turn_id,conf_score,num_switch,num_init,num_joke,num_more,num_end,num_oov,num_short_answer, num_name_entity,num_not_repeat,num_continue)
for key in keys:
    print key
    for turn_id in range(1,12):
        for conf_score in [0, 0.3, 0.6,1]:
            for num_switch in range(4):
                for num_init in range(2):
                    for num_joke in range(2):
                        for num_more in range(2):
                            for num_end in range(2):
                                #for num_oov in range(11):
                                #   for num_short_answer in range(11):
                                #        for num_name_entity in range(11):
                                #           for num_not_repeat in range(11):
                                                for num_continue in range(2):
                                                    state = (key[0],key[1],key[2],turn_id, conf_score/10, num_switch,num_init,num_joke,num_more,num_end,num_continue)
                                                    action = key[3]
                                                    if action == 'switch':
                                                        num_action = num_switch
                                                    if action == 'joke':
                                                        num_action = num_joke
                                                    if action == 'more':
                                                        num_action = num_more
                                                    if action == 'end':
                                                        num_action = num_end
                                                    if action == 'init':
                                                        num_action = num_init
                                                    if action == 'continue':
                                                        reward_table[state,action] = conf_score *8 + turn_id*0.5 + (num_switch+num_joke+num_init+num_more+num_end)*5
                                                    #elif action == 'oov':
                                                    #    reward_table[state,action] = 30 + turn_id - num_oov
                                                    #elif action == 'name_entity':
                                                    #    reward_table[state,action] = 30 + turn_id - num_name_entity
                                                    #elif action == 'not_repeat':
                                                    #    reward_table[state,action] = 30 + turn_id - num_not_repeat
                                                    #elif action == 'short_answer':
                                                    #    reward_table[state,action] = 30 + turn_id - num_short_answer
                                                    else:
                                                        reward_table[state,action] = (table_value[key]-1.5)*20 - turn_id - num_action*5
for sent_1 in ['null','neg','pos','neutral']:
    for sent_2 in ['null','neg','pos','neutral']:
        for sent_3 in ['null','neg','pos','neutral']:
            for turn_id in range(1,12):
                for conf_score in [0, 0.3, 0.6,1]:
                    for num_switch in range(4):
                        for num_init in range(2):
                            for num_joke in range(2):
                                for num_more in range(2):
                                    for num_end in range(2):
                                        for num_continue in range(2):
                                            state = (sent_1,sent_2,sent_3,turn_id,conf_score,num_switch,num_init,num_joke,num_more,num_end,num_end)
                                            for action in action_list:
                                                if state not in reward_table.keys():
                                                    if action == 'switch':
                                                        num_action = num_switch
                                                    if action == 'joke':
                                                        num_action = num_joke
                                                    if action == 'more':
                                                        num_action = num_more
                                                    if action == 'end':
                                                        num_action = num_end
                                                    if action == 'init':
                                                        num_action = num_init
                                                    if action == 'continue':
                                                        reward_table[state,action] = conf_score *8 + turn_id*0.5 + (num_switch+num_joke+num_init+num_more+num_end)*5
                                                    #elif action == 'oov':
                                                    #    reward_table[state,action] = 30 + turn_id - num_oov
                                                    #elif action == 'name_entity':
                                                    #    reward_table[state,action] = 30 + turn_id - num_name_entity
                                                    #elif action == 'not_repeat':
                                                    #    reward_table[state,action] = 30 + turn_id - num_not_repeat
                                                    #elif action == 'short_answer':
                                                    #    reward_table[state,action] = 30 + turn_id - num_short_answer
                                                    else:
                                                        reward_table[state,action] = (table_value[key]-1.5)*20 - turn_id - num_action*5

pickle.dump(reward_table,open('reward_table_2.pkl','w'))
