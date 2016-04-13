#!/usr/bin/etc python

import galbackend_online
import sys
import socket
import time
import commands
import pickle
#socket = None
#sys.path.append("~/nltk_data")
#target = galbackend.GalInterface()
#print(target)
#gt = galbackend.Thread(target=galbackend.GalInterface)
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
theme = {}
user_input = pickle.load(open('user_input_all.pkl'))
conversation_id = 1000
print len(user_input)
for line in user_input:
    commands.getstatusoutput("rm c.txt")
    turn_id = 1
    name = 'simulated_conversations/'+str(conversation_id)+'.txt'
    f = open(name,'w')
    while True:
        f.write('Turn: ' + str(turn_id) + '\n')
        theme, strategy, response,previous_history,word2vec = galbackend_online.get_response( policy_mode,line, name ,previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
        if strategy =='new':
            continue
        f.write('Alice: '+line + '\n')
	f.write('TickTock:' +response+'\n')
	f.write('\n')
        # Here write the Alice response, send in response, get out line.
        cmd = '''curl -b c.txt -c c.txt -e sheepridge.pandorabots.com --data "input=hello" 'http://sheepridge.pandorabots.com/pandora/talk?botid=b69b8d517e345aba&skin=custom_input' 2>/dev/null | tail -n 1 '''.replace('hello',response)
        print 'cmd'
        print cmd
        output_all = commands.getstatusoutput(cmd)
        output = output_all[1]
        print output
        sentence = output.split('<br>')
        print 'sentence'
        print sentence
        line = sentence[-1][10:]
        print 'line'
        print line
        turn_id = turn_id +1
        if turn_id > 15:
            break
    conversation_id = conversation_id+1

