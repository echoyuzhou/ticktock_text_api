import random
action_list =['a','b','c','d','e','f']
q_list = [3,4,5,6,3,6]
maxQ = max(q_list)
count = q_list.index(maxQ)
if count>1:
    best = [i for i in range(len(action_list)) if q_list[i]==maxQ]
    print best
    i = random.choice(best)
else:
    i = q_list.index(maxQ)
action_selected = action_list[i]

print action_selected

