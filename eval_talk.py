#!/usr/bin/etc python

import galbackend_online
import sys
import socket
import time
#socket = None
#sys.path.append("~/nltk_data")
#target = galbackend.GalInterface()
#print(target)
#gt = galbackend.Thread(target=galbackend.GalInterface)
galbackend_online.InitLogging()
galbackend_online.InitResource('v3')
oov_state =1
name_entity_state =1
anaphra_state =1
short_answer_state=1
previous_history ={}
word2vec_ranking_state =0
theme = {}
f = open('eval_talk_out.txt','w')
turn_id = 1
line = 'Hello'
while True:
        f.write('Turn: ' + str(turn_id) + '\n')
        theme, strategy, response,previous_history,word2vec = galbackend_online.get_response( line, 'user_id',previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,1)
        f.write('User: '+line + '\n')
	f.write('TickTock:' +response+'\n')
	f.write('\n')
        theme, strategy, line,previous_history,word2vec = galbackend_online.get_response( response, 'user_id',previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,0,1)
        turn_id = turn_id +1
        if turn_id > 20:
            break

