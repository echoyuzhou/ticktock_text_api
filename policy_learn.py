import pickle, random
import sentiment_vader
import alice
import con_reward
import galbackend_online
import sys
import socket
import time
import commands
import gensim
galbackend_online.InitLogging()
galbackend_online.InitResource('v4')
oov_state =1
name_entity_state =1
anaphra_state =1
short_answer_state=1
previous_history ={}
word2vec_ranking_state =1
tfidf_state = 1
policy_mode = 0
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
            for turn_id in range(1,12):
                for action in action_list:
                    q_table[((state_1,state_2,state_3,turn_id),action)]=0

#load the reward table (look at reward_table.py)
reward_table = pickle.load(open('reward_table.pkl'))
dic = pickle.load(open('dictionary_conv.pkl'))
model = gensim.models.Word2Vec.load('/tmp/word2vec_100_break')
#each previous real user said utterance is the chosen starting state.
user_input_all = pickle.load(open('user_input_all.pkl'))

#the conv is a list of the stored conversation, starting with ticktock's input.
TopicLib = ['movies','politics','music','sports', 'board games']
start_index = 1000
conv_index = start_index
reward_avg ={}
f_reward  = open('reward_value.txt','w')
conv_reward_list =[]
conv = {"Turns":{}}
for tt_utt in user_input_all:
    print 'conv_index: '+ str(conv_index)
    #conv =[]
    conv["Turns"][0]={}
    conv["Turns"][0]["You"] = 'Hello'
    conv["Turns"][0]["TickTock"] = tt_utt
    conv["Turns"][0]["Appropriateness"] =0# clean the cash for alice
    conv["Turns"][0]["Strategy"] = ['new']
    commands.getstatusoutput("rm c.txt")
    if conv_index > start_index+300:
        epsilon = 0.1
        if (conv_index-start_index)%20 == 0:
        # here we do testing.
            epsilon = 0
            f = open('simulate_conv/'+str(conv_index)+'_test.txt','w')
        else:
            f = open('simulate_conv/'+str(conv_index)+'.txt','w')
    else:
        epsilon = 0.8
        f = open('simulate_conv/'+str(conv_index)+'.txt','w')
    f.write('Turn: 0'+'\n')
    f.write('You: Hello'+'\n' )
    f.write('TickTock: ' + tt_utt +'\n')
    f.write('Appropriateness: ' + '\n')
    f.write('Strategy: new' + '\n')
    f.write('')
    f.write('\n')
    sent_3 = sentiment_vader.get_sentiment(tt_utt)
    sent_2 = 'null'
    sent_1 = 'null'
    theme[str(conv_index)] = random.choice(TopicLib)
    old_theme = theme[str(conv_index)]
    previous_history[str(conv_index)] = ['Hello',tt_utt]
    reward_list = []
    for turn_id in range(1,11):
        print 'turn_id' +str(turn_id)+'\n'
        al_utt = alice.alice(tt_utt)
        conv["Turns"][turn_id] ={}
        conv["Turns"][turn_id]["You"] = al_utt
        f.write('Turn: ' + str(turn_id) +'\n')
        f.write('You: ' + al_utt+'\n')
        next_sent_1 = sent_3
        next_sent_2 = sentiment_vader.get_sentiment(al_utt)
        state = (sent_1,sent_2,sent_3,turn_id)
# here we see if we go into get_response, it happen to be in any of the five strategy, then we select one to excecute. otherwise we stick to the original strategy.
        strategy, response,word2vec = galbackend_online.get_response(None,policy_mode,al_utt, str(conv_index), previous_history,{str(conv_index):old_theme}, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
        previous_history[str(conv_index)].pop()
        previous_history[str(conv_index)].pop()
        if strategy[-1] in action_list_pass:
            utt_real = response
            next_sent_3 = sentiment_vader.get_sentiment(utt_real)
        #   q_value = 1000
            action_selected = strategy[-1]
        else:
        #action selection portion
            if random.random()<epsilon:
                action_selected = random.choice(action_list)
                strategy, utt_real, word2vec = galbackend_online.get_response(action_selected, policy_mode,al_utt, str(conv_index) ,previous_history,{str(conv_index):old_theme}, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
                next_sent_3 = sentiment_vader.get_sentiment(utt_real)
            else:
                q_list =[]
                q_sent = []
                q_utt =[]
                for action in action_list:
                    strategy, utt,word2vec = galbackend_online.get_response(action,policy_mode,al_utt, str(conv_index),previous_history,{str(conv_index):old_theme}, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
                    previous_history[str(conv_index)].pop()
                    previous_history[str(conv_index)].pop()
                    next_sent_3 = sentiment_vader.get_sentiment(utt)
                    next_state = (next_sent_1,next_sent_2,next_sent_3,turn_id+1)
                    q_list.append(q_table[next_state,action])
                    q_sent.append(next_sent_3)
                    q_utt.append(utt)
                    maxQ = max(q_list)
                count = q_list.index(maxQ)
                if count>1:
                    best = [i for i in range(len(action_list)) if q_list[i]==maxQ]
                    #print best
                    i = random.choice(best)
                else:
                    i = q_list.index(maxQ)
                action_selected = action_list[i]
                next_sent_3 = q_sent[i]
                utt_real = q_utt[i]
            maxQ_real = q_table[((next_sent_1,next_sent_2,next_sent_3,turn_id +1),action_selected)]
            q_table[(state,action_selected)] =  (1-alpha)*q_table[(state,action_selected)]+alpha*(reward_table[(state,action)] + gamma*maxQ_real)
            #f.write('reward: ' + str(reward_table[(state,action)] )+'\n')
            reward_list.append(reward_table[(state,action)])
            if action_selected == 'switch':
            #    print old_theme
            #    print theme
            #    print utt_real
            #    #sys.exit()
                old_theme = theme[str(conv_index)]
        f.write('TickTock: ' +utt_real +'\n')
        f.write('Appropriateness:' +'\n')
        f.write('Strategy: '+ str(action_selected) +'\n')
        #f.write('Theme: ' + old_theme + '\n')
        f.write('\n')
        conv["Turns"][turn_id]["TickTock"] = utt_real
        conv["Turns"][turn_id]["Appropriateness"] =0
        conv["Turns"][turn_id]["Strategy"] = [action_selected]
        #conv["Turns"][turn_id]
        # clean the cash for alice
        if turn_id > 9:
                app, depth, info = con_reward.con_reward(conv,dic,model)
                con_reward_value = app*10+depth*100 + info
                #print con_reward_value
                if action_selected in action_list:
                    q_table[(state,action_selected)] =  q_table[(state,action_selected)] + con_reward_value
                f.write('app Reward:' + str(app))
                f.write('depth reward:' +str(depth))
                f.write('info:' +str(info))
                f.write('Conversation Reward: ' +str(con_reward_value) + '\n')
                f_reward.write('Conversation Reward: ' +str(con_reward_value) + '\n')
                conv_reward_list.append(con_reward_value)
                if conv_index -start_index >20:
                    if conv_reward_list[-1] ==conv_reward_list[-2] and conv_reward_list[-3] == conv_reward_list[-2]:
                        print 'converged'
                        pickle.dump(q_table, open('q_table.pkl','w'))
                        break
                if reward_list ==[]:
                    reward_avg[str(conv_index)] =0 # no action is selected
                else:
                    reward_avg[str(conv_index)] = (sum(reward_list)+con_reward_value)/len(reward_list)
                f.write('Average_reward:' + str(reward_avg[str(conv_index)]) +'\n')
        sent_3 = next_sent_3
        sent_2 = next_sent_2
        sent_1 = next_sent_1
        tt_utt = utt_real
    f.close()
    conv_index = conv_index + 1
    if conv_index == 1000+300:
        pickle.dump(q_table, open('q_table_100.pkl','w'))
    if conv_index > 1000+3000:
        pickle.dump(q_table, open('q_table.pkl','w'))
        break

