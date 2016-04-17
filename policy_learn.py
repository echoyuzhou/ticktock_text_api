#import qlearn
import pickle
import sentiment
import alice
#import NLG
import con_reward
import galbackend_online
import sys
import socket
import time
import commands
galbackend_online.InitLogging()
galbackend_online.InitResource('v4')
oov_state =1
name_entity_state =1
anaphra_state =1
short_answer_state=1
previous_history ={}
word2vec_ranking_state =1
tfidf_state =1
policy_mode = 1
user_list =[]i
alpha = 0.1 # learning rate, if it is deterministic environment, then alpha =1
theme = {}
epsilon = 0.1
gamma =1 #If Gamma is closer to zero, the agent will tend to consider only immediate rewards.  If Gamma is closer to one, the agent will consider future rewards with greater weight, willing to delay the reward.
#a list of list, each has a conversation.
#conversations = pickle.load(open('conversations.pkl'))
action_list = ['init','joke','more','end','switch']
action_list_pass = ['continue','name_entity','oov','short_answer']
#initilize q table.
#we only do 10 turn converstion.
q_table = {}
sub_state_list = ['null','pos','neg','neutral']
for state_1 in sub_state_list:
    for state_2 in sub_state_list:
        for state_2 in sub_state_list:
            for turn_id in range(10)+1:
                for action in action_list:
                    q_table[((state_1,state_2,state_3,turn_id),action)]=0

#load the reward table (look at reward_table.py)
reward_table = pickle.load(open('reward_table.pkl'))

#each previous real user said utterance is the chosen starting state.
user_input_all = pickle.load(open('user_input.pkl'))

# the conv is a list of the stored conversation, starting with ticktock's input.
@
TopicLib = [movies,politics,music,sports, board games]
con_index = 1000
def q_conv(q_table,q_table_old):
    value = 0
    for key in q_table.keys():
        value = value +(q_table[key]-q_table_old[key])*(q_table[key]-q_table_old[key])
    return value

for tt_utt in user_input_all:
    conv = tt_utt
    # clean the cash for alice
    commands.getstatusoutput("rm c.txt")
    f = fopen('simulate_conv/'+str(conv_index)+'.txt','w')
    f.write('Turn: 0'+'\n')
    f.write('You: Hello'+'\n' )
    f.write('TickTock: ' +tt_utt +'\n')
    sent_1 = sentiment.get_sentiment(tt_utt)
    sent_2 = 'null'
    sent_3 = 'null'
    theme[str(con_index)] = random.choice(TopicLib)
    previous_history[str(con_index)] = [tt_utt]
    for turn_id in range(1,10)
        al_utt = alice.alice(tt_utt)
        conv.append(al_utt)
        f.write('Turn: ' + str(turn_id) +'\n')
        f.write('You: ' + al_utt+'\n')
        next_sent_3 = sent_1
        next_sent_2 = sentiment.get_sentiment(al_utt)
        state = (sent_1,sent_2,sent_3,turn_id)
# here we see if we go into get_response, it happen to be in any of the five strategy, then we select one to excecute. otherwise we stick to the original strategy.
        theme, strategy, response,previous_history_new,word2vec = galbackend_online.get_response( None,policy_mode,al_utt, str(con_index) ,previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
        if len(strategy)>1
            strategy_end = strategy[-1]
        else
            strategy_end = strategy
        if strategy_end in action_list_pass:
            previous_history = previous_history_new
            conv.append(response)
        else:
        #action selection portion
            if random.random()<epsilon:
                action_selected = random.choice(action_list)
            else:
                q_value = q_table[(state,action)]
                q_list =[]
                for action in action_list:
                    utt = NLG.fillTemplate(action) # need more params
                    next_sent_1 = sentiment.get_sentiment(utt)
                    next_state = (next_sent_1,next_sent_2,next_sent_3,index+1)
                    q_list.append(q_table[next_state,action])
                    maxQ = max(q_list)
                count = q_list(maxQ)
                if count>1:
                    best = [i for i in range(len(action_list)) if q_list==maxQ]
                    i = random.choice(best)
                else:
                    i = q_list.index(maxQ)
                action_selected = action_list[i]
            theme, strategy, utt_real,previous_history_new,word2vec = galbackend_online.get_response(action_selected, policy_mode,al_utt, str(con_index) ,previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
            previous_history[str(con_index)].append(al_utt)
            previous_history[str(con_index)].append(utt_real)
            conv.append(utt_real)
            q_table_old = q_table
             # learning rate here is set to be 1
            q_table[(state,action_selected)] =  (1-alpha)*q_table[(state,action_selected)]+alpha*(reward_table[(state,action)] + gamma*maxQ)
            if turn_id == 10
                con_reward = con_reword.con_reward(conv)
                q_table[(state,action_selected)] =  q_table[(state,action_selected)] + con_reward
                continue
            q_value = q_conv(q_table,q_table_old)
            if q_value < 0.1 or conv_index >1000+100:
                print q_value
                pickle.dump(q_table, open('q_table.pkl','w'))
                break
        f.write('TickTock: ' +utt_real +'\n')
        f.write('Appropriateness:' +'\n')
        f.write('Strategy: '+ action_selected +'\n')
        f.write('\n')
        tt_utt = sentiment.get_sentiment(utt_real)
        sent_1 = next_sent_1_real
        sent_2 = next_sent_2
        sent_3 = next_sent_3
    # check q_table's convergence.
    f.close()
    con_index = con_index + 1

