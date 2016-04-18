import pickle, random
import sentiment
import alice
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
user_list =[]
alpha = 0.1 # learning rate, if it is deterministic environment, then alpha =1
theme = {}
epsilon = 0.5
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
        for state_3 in sub_state_list:
            for turn_id in range(1,11):
                for action in action_list:
                    q_table[((state_1,state_2,state_3,turn_id),action)]=0

#load the reward table (look at reward_table.py)
reward_table = pickle.load(open('reward_table.pkl'))

#each previous real user said utterance is the chosen starting state.
user_input_all = pickle.load(open('user_input_all.pkl'))

#the conv is a list of the stored conversation, starting with ticktock's input.
TopicLib = ['movies','politics','music','sports', 'board games']
conv_index = 1000
def q_conv(q_table,q_table_old):
    value = 0
    for key in q_table.keys():
        value = value +(q_table[key]-q_table_old[key])*(q_table[key]-q_table_old[key])
    return value

for tt_utt in user_input_all:
    conv =[]
    conv.append(tt_utt)
    # clean the cash for alice
    commands.getstatusoutput("rm c.txt")
    f = open('simulate_conv/'+str(conv_index)+'.txt','w')
    f.write('Turn: 0'+'\n')
    f.write('You: Hello'+'\n' )
    f.write('TickTock: ' + tt_utt +'\n')
    f.write('Appropriateness: ' + '\n')
    f.write('Strategy: new' + '\n')
    f.write('')
    f.write('\n')
    sent_3 = sentiment.get_sentiment(tt_utt)
    sent_2 = 'null'
    sent_1 = 'null'
    theme[str(conv_index)] = random.choice(TopicLib)
    previous_history[str(conv_index)] = ['Hello',tt_utt]
    for turn_id in range(1,10):
        print turn_id
        al_utt = alice.alice(tt_utt)
        conv.append(al_utt)
        f.write('Turn: ' + str(turn_id) +'\n')
        f.write('You: ' + al_utt+'\n')
        next_sent_1 = sent_3
        next_sent_2 = sentiment.get_sentiment(al_utt)
        state = (sent_1,sent_2,sent_3,turn_id)
# here we see if we go into get_response, it happen to be in any of the five strategy, then we select one to excecute. otherwise we stick to the original strategy.
        theme_new, strategy, response,previous_history_new,word2vec = galbackend_online.get_response( None,policy_mode,al_utt, str(conv_index) ,previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
        previous_history[str(conv_index)].pop()
        previous_history[str(conv_index)].pop()
        if strategy[-1] in action_list_pass:
            utt_real = response
            conv.append(utt_real)
            next_sent_3 = sentiment.get_sentiment(utt_real)
            q_value = 1000
            action_selected = strategy
        else:
        #action selection portion
            if random.random()<epsilon:
                action_selected = random.choice(action_list)
            else:
                q_value = q_table[(state,action)]
                q_list =[]
                for action in action_list:
                    theme_new, strategy, utt,previous_history_new,word2vec = galbackend_online.get_response(action, policy_mode,al_utt, str(conv_index) ,previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
                    previous_history[str(conv_index)].pop()
                    previous_history[str(conv_index)].pop()
                    next_sent_3 = sentiment.get_sentiment(utt)
                    next_state = (next_sent_1,next_sent_2,next_sent_3,turn_id+1)
                    q_list.append(q_table[next_state,action])
                    maxQ = max(q_list)
                count = q_list.index(maxQ)
                if count>1:
                    best = [i for i in range(len(action_list)) if q_list[i]==maxQ]
                    print best
                    i = random.choice(best)
                else:
                    i = q_list.index(maxQ)
                action_selected = action_list[i]
            theme, strategy, utt_real,previous_history_new,word2vec = galbackend_online.get_response(action_selected, policy_mode,al_utt, str(conv_index) ,previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
            next_sent_3 = sentiment.get_sentiment(utt_real)
            conv.append(utt_real)
            maxQ_real = q_table[((next_sent_1,next_sent_2,next_sent_3,turn_id +1),action_selected)]
            q_table_old = q_table
             # learning rate here is set to be 1
            q_table[(state,action_selected)] =  (1-alpha)*q_table[(state,action_selected)]+alpha*(reward_table[(state,action)] + gamma*maxQ_real)
            f.write('reward: ' + str(reward_table[(state,action)] )+'\n')
            if turn_id > 9:
                con_reward = con_reword.con_reward(conv)
                q_table[(state,action_selected)] =  q_table[(state,action_selected)] + con_reward
                f.write('TickTock: ' +utt_real +'\n')
                f.write('Appropriateness:' +'\n')
                f.write('Strategy: '+ str(action_selected) +'\n')
                f.write('Theme: ' + theme[str(conv_index)] + '\n')
                f.write('\n')
                f.write('Conversation Reward: ' +str(con_reward) + '\n')
                break
            q_value = q_conv(q_table,q_table_old)
        if q_value < 0.1 and conv_index > 1000+10:
                print q_value
                pickle.dump(q_table, open('q_table.pkl','w'))
                break
        f.write('TickTock: ' +utt_real +'\n')
        f.write('Appropriateness:' +'\n')
        f.write('Strategy: '+ str(action_selected) +'\n')
        f.write('Theme: ' + theme[str(conv_index)] + '\n')
        f.write('\n')
        sent_3 = next_sent_3
        sent_2 = next_sent_2
        sent_1 = next_sent_1
        tt_utt = utt_real
    f.close()
    conv_index = conv_index + 1

