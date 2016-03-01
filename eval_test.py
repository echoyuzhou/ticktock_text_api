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
word2vec_ranking_state =1
theme = {}
#while(1):
    #galbackend.LaunchQueryDebug('can you say that again')
#connection.send('ready')
with open('test_test.txt') as f:
	lines = f.readlines()
f = open('test_test','w')
for line in lines:
        theme, strategy, response,previous_history = galbackend_online.get_response( line, 'user_id',previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,1)
        f.write('User: '+line)
	f.write('TickTock:' +response+'\n')
	f.write('\n')
