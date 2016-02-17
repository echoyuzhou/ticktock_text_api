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
galbackend_online.InitResource('v2')
oov_state =1
name_entity_state =1
#while(1):
    #galbackend.LaunchQueryDebug('can you say that again')
#connection.send('ready')
with open('eval_set.txt') as f:
	lines = f.readlines()
f = open('eval_set_output','w')
for line in lines:
        response = galbackend_online.get_response(line, 'user_id',oov_state,name_entity_state)
	f.write('User: '+line)
	f.write('TickTock:' +response+'\n')
	f.write('\n')
