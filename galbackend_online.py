#!/usr/bin/env python
##########################################################################
##                                                                       ##
##                  Language Technologies Institute                      ##
##                     Carnegie Mellon University                        ##
##                         Copyright (c) 2016                            ##
##                        All Rights Reserved.                           ##
##                                                                       ##
##  Permission is hereby granted, free of charge, to use and distribute  ##
##  this software and its documentation without restriction, including   ##
##  without limitation the rights to use, copy, modify, merge, publish,  ##
##  distribute, sublicense, and/or sell copies of this work, and to      ##
##  permit persons to whom this work is furnished to do so, subject to   ##
##  the following conditions:                                            ##
##   1. The code must retain the above copyright notice, this list of    ##
##      conditions and the following disclaimer.                         ##
##   2. Any modifications must be clearly marked as such.                ##
##   3. Original authors' names are not deleted.                         ##
##   4. The authors' names are not used to endorse or promote products   ##
##      derived from this software without specific prior written        ##
##      permission.                                                      ##
##                                                                       ##
##  CARNEGIE MELLON UNIVERSITY AND THE CONTRIBUTORS TO THIS WORK         ##
##  DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING      ##
##  ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT   ##
##  SHALL CARNEGIE MELLON UNIVERSITY NOR THE CONTRIBUTORS BE LIABLE      ##
##  FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES    ##
##  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN   ##
##  AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,          ##
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF       ##
##  THIS SOFTWARE.                                                       ##
##                                                                       ##
###########################################################################
##  Author: Zhou Yu (zhouyu@cs.cmu.edu)                                  ##
##  Date  : Feb 2016                                                     ##
###########################################################################
## Description: TickTock
##                                                                       ##
##                                                                       ##
###########################################################################
import nltk
import os, sys, string, math, random
import exceptions, logging
from copy import copy, deepcopy
from time import sleep
from random import randint
from threading import Thread, Timer
import os.path as path
import Control,Loader,NLG
import socket,datetime,pickle,unicodedata,zmq,threading
from gensim import corpora, models
connection = None
filepointer = None
socket = None

def InitLogging():
	global logger, filepointer, folder_name
	logger = logging.getLogger('BE')
	hdlr = logging.FileHandler('BE.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.WARNING)
	#latest_subdir = max([os.path.join(folder_name,d) for d in os.listdir(folder_name)], key=os.path.getmtime)
	#folder_sub =  latest_subdir
	datenow = datetime.datetime.now()
	subfoldername = str(datenow.year)+str(datenow.month)+str(datenow.day)+str(datenow.hour)+ str(datenow.minute)+str(datenow.second)
	#folder_sub = folder_name + '\\'+subfoldername
	#latest_subdir_session = max([os.path.join(folder_sub,d) for d in os.listdir(folder_sub)], key=os.path.getmtime)
	filepointer = open( subfoldername +  'backend.log', 'w')
        print filepointer
def Log(input):
	global logger
	print input
	logger.error(input)
	sys.stdout.flush()

def InitResource(version):
    global TemplateLib, TopicLib, TreeState, Template, model,init_id,joke_id,more_id, dictionary_value, turn_id,wizard,isAlltag,engaged_input, engagement_mode
    global q_table, database, resource, socket, listflie, tfidfmodel, tfidfdict, table_state_strategy
    database = {}
    resource = {}
    listfile = None
    init_id =0
    joke_id =0
    more_id =0
    wizard =3
    isAlltag =0
    turn_id =0
    engaged_input =[]
    engagement_mode =0
    rescource_root = 'resource'
    template_list=['template/template_new.txt', 'template/template_end.txt', 'template/template_open.txt', 'template/template_expand.txt', 'template/template_init.txt', 'template/template_joke.txt', 'template/template_back.txt', 'template/template_more.txt']
    template_list = [path.join(rescource_root, name) for name in template_list]
    topicfile = path.join(rescource_root, 'topic.txt')
    tfidfname = 'tfidf_reference'
    with open('dictionary_value.pkl') as f:
	dictionary_value = pickle.load(f)
    if version is 'v1':
		listfile = 'cnn_qa_human_response_name.list'
    elif version is 'v2':
		listfile = 'cnn_qa_human_response_name_high_app.list'
    elif version is 'v2.5':
		listfile = 'cnn_qa_human_response_name_high_app.list'
                tfidfdict = corpora.Dictionary.load(tfidfname + '.dict')
                tfidfmodel = models.tfidfmodel.TfidfModel.load(tfidfname + '.tfidf')
    elif version is 'v3':
                listfile = 'cnn_hr_v1_v2.list'
                tfidfdict = corpora.Dictionary.load(tfidfname + '.dict')
                tfidfmodel = models.tfidfmodel.TfidfModel.load(tfidfname + '.tfidf')
    elif version is 'v4':
                listfile = 'cnn_hr_v1_v2_v4.list'
                tfidfdict = corpora.Dictionary.load(tfidfname + '.dict')
                tfidfmodel = models.tfidfmodel.TfidfModel.load(tfidfname + '.tfidf')
    datalist=[line.strip() for line in open(listfile)]
    q_table = pickle.load(open('q_table.pkl'))
    database = Loader.LoadDataPair(datalist)
    resource = Loader.LoadLanguageResource()
    TemplateLib = Loader.LoadTemplate(template_list)
    TopicLib = Loader.LoadTopic(topicfile)
    TreeState, Template = Control.Init()
    model = models.Doc2Vec.load('/tmp/word2vec_50')
    if wizard is 2:
		context= zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:5555")
    with open('table_state_strategy.pkl') as f:
        table_state_strategy = pickle.load(f)

def get_response(fix_strategy,policy_mode,user_input,user_id,previous_history, theme, oov_mode =1,name_entity_mode=1, short_answer_mode=1,anaphora_mode=1, word2vec_ranking_mode=1,tfidf_mode=1):
        global database, resource, turn_id, time, wizard, socket,isAlltag, tfidfmodel, tfidfdict, turn_id, engagement_mode, engaged_input, isAlltag, wizard
	global TemplateLib, TopicLib, TreeState, Template, connection, filepointer,engaged_input, init_id,joke_id,more_id,dictionary_value,model, table_state_strategy, q_table
        #print 'user_input: ' + user_input
        #print 'user_id:' + user_id
        strategy = []
        filepointer.write('turn_id: ' + str(turn_id) + '\n')
	filepointer.write('user_id: ' + user_id + '\n')
	turn_id = turn_id+1
	filepointer.write('time:' + str(datetime.datetime.now())+ '\n')
	filepointer.write('user_input:' + user_input + '\n')
        if fix_strategy is None:
            if user_id in previous_history.keys():
                history = previous_history[user_id]
            else:
                if user_id not in theme.keys():
                    theme[user_id] = random.choice(TopicLib)
                output = 'Hello, I really like ' + theme[user_id] + '. How about we talk about ' + theme[user_id]
                previous_history[user_id]=[user_input,output]
                return 'new', output,0
            if tfidf_mode is 1:
                relavance, answer, anaphora_trigger,word2vec = Control.FindCandidate(model,database, resource, user_input,isAlltag,history,anaphora_mode, word2vec_ranking_mode, tfidfmodel=tfidfmodel, tfidfdict=tfidfdict)
            else:
	        relavance, answer, anaphora_trigger,word2vec  = Control.FindCandidate(model,database, resource, user_input,isAlltag,history,anaphora_mode,word2vec_ranking_mode)
	    filepointer.write('relevance: ' + str(relavance)+ '\n')
	    filepointer.write('RetrievedAnswer: ' + str(answer) + '\n')
            if anaphora_trigger is 1:
                strategy.append('anaphora')
            if engagement_mode is 1:
		if wizard is 1:
			if connection is None:
				serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				serversocket.bind(('localhost', 13011))
				serversocket.listen(5)
				connection, address = serversocket.accept()
				print 'connection established'
				print connection
			connection.send('ready')
			engagement = connection.recv(64)
		elif wizard is 2: # this is taking the automatic engagement computed as the engagement input
			print 'Sending request'
			socket.send("ready\0")
			engagement = socket.recv()
			#print engagement`
			#print("Received reply [ %s ]" %  message)
		else:# this is random generating engagement for testing.
			engagement = random.choice('12345')
		print engagement
		filepointer.write('engagement: ' + engagement + '\n')
		if int(engagement)>3:
			engaged_input.append(user_input)
		state = Control.SelectState_rel(relavance, int(engagement), TreeState,engaged_input)
	    else:
		state,output,theme_new,init_id,joke_id,more_id = Control.SelectState_rel_only(table_state_strategy, relavance, user_input, history, TreeState, dictionary_value,oov_mode,name_entity_mode,short_answer_mode,policy_mode, q_table,theme[user_id],TemplateLib, TopicLib, Template,init_id,joke_id,more_id)
#                print 'old_theme' + theme[user_id]
                theme[user_id] = theme_new
#                print 'new_theme' + theme_new
        else:
            state = {'name': fix_strategy}
            output = None
            answer = ''
            word2vec = 0
        #print strategy
        #print state['name']
        strategy.append(state['name'])
        if output == None:
            theme[user_id], output,init_id,joke_id,more_id, engagement_input = NLG.FillTemplate(theme[user_id], TemplateLib, TopicLib, Template[state['name']],init_id,joke_id,more_id,engaged_input, answer,output)
        #print theme
        if isinstance(output, unicode):
		output = unicodedata.normalize('NFKD',output).encode('ascii','ignore')
	if output.find("Piers") is not -1:
		output = output.replace("Piers","dear")
	filepointer.write('TickTockResponse:' + output + '\n')

        if user_id in previous_history.keys():
                previous_history[user_id].append(user_input)
                previous_history[user_id].append(output)
        else:
            #if fix_strategy is None:
                print "we are in the else user_id"
                previous_history[user_id] = [user_input,output]
        #if output[-2:-1]==' ':
        #    output = output[0:-2] +output[-1]
        #print 'strategy' +  str(strategy)
        #print 'response: ' + output
        #print "end response generation =================="
	#print "==========================================="
        filepointer.flush()
        #print "this is previous history"
        #print previous_history
        print 'init_id' +str(init_id)
        return strategy,output,word2vec #,dictionary_value



