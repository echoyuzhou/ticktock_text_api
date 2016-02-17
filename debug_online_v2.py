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
#while(1):
    #galbackend.LaunchQueryDebug('can you say that again')
#connection.send('ready')
while True:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Log('serversocket')
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('localhost', 13111))
        serversocket.listen(5)
        connection, address = serversocket.accept()
        #Log('connection established')
        print connection
        user_input = connection.recv(1024)
	print user_input
        user_id, user_input_real = user_input.split('|')
	print user_id
        print user_input_real
        response = galbackend_online.get_response(user_input_real, user_id,1,1)
        connection.send(response)
        print 'finish sending response'
        serversocket.close()

