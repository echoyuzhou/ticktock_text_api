#!/usr/bin/etc python

import galbackend_online
import sys
import socket
import time
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
while True:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Log('serversocket')
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('localhost', 13113))
        serversocket.listen(5)
        connection, address = serversocket.accept()
        #Log('connection established')
        print connection
        user_input = connection.recv(1024)
	print user_input
        user_id, user_input_real = user_input.split('|')
	print user_id
        print user_input_real
        strategy,response, word2vec = galbackend_online.get_response(None,policy_mode, user_input_real, user_id,previous_history,theme,oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,tfidf_state)
        print previous_history
        connection.send(response + "|" + str(strategy))
        print 'finish sending response'
        serversocket.close()

