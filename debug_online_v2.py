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
tfidf_state =1
#while(1):
    #galbackend.LaunchQueryDebug('can you say that again')
#connection.send('ready')
while True:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Log('serversocket')
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('localhost', 13112))
        serversocket.listen(5)
        connection, address = serversocket.accept()
        #Log('connection established')
        print connection
        user_input = connection.recv(1024)
	print user_input
        user_id, user_input_real = user_input.split('|')
	print user_id
        print user_input_real
        strategy,response,previous_history = galbackend_online.get_response(user_input_real, user_id,previous_history,oov_state,name_entity_state,short_answer_state,word2vec_ranking_state,anaphra_state,tfidf_state)
        connection.send(response)
        print 'finish sending response'
        serversocket.close()

