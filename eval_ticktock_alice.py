#!/usr/bin/etc python

import galbackend_online
import sys
import socket
import time
import commands
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
f = open('eval_ticktock_alice.txt','w')
turn_id = 1
line = 'Hello'
commands.getstatusoutput("rm c.txt")
while True:
        f.write('Turn: ' + str(turn_id) + '\n')
        theme, strategy, response,previous_history,word2vec = galbackend_online.get_response( line, 'user_id',previous_history,theme, oov_state,name_entity_state,short_answer_state,anaphra_state,word2vec_ranking_state,1)
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
        if turn_id > 20:
            break

