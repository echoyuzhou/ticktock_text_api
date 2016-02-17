#!/usr/bin/env python
###########################################################################
##                                                                       ##
##                  Language Technologies Institute                      ##
##                     Carnegie Mellon University                        ##
##                         Copyright (c) 2012                            ##
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
##  Author: Aasish Pappu (aasish@cs.cmu.edu)                             ##
##  Date  : November 2012                                                ##
###########################################################################
## Description: Example python backend module for olympus applications   ##
##                                                                       ##
##                                                                       ##
###########################################################################
import os, sys, string, math, random
import exceptions
from copy import copy, deepcopy
import re
from time import sleep
from random import randint
from threading import Thread, Timer
import logging
import os.path as path
import Control #@yipeiw
import Loader
import NLG
import sys
import socket
import time
import datetime
import pickle
#os.environ['GC_HOME'] = os.path.join(os.environ['OLYMPUS_ROOT'], 'Libraries', 'Galaxy')
#sys.path.append(os.path.join(os.environ['GC_HOME'], 'contrib', 'MITRE', 'templates'))
#sys.path.append(os.path.join(os.environ['OLYMPUS_ROOT'], 'bin', 'x86-nt'))

#import GC_py_init
#import Galaxy, GalaxyIO
import unicodedata
import zmq
import threading
import threading
import oov
import name_entity
galaxyServer = None
connection = None
current_dialog_state = None
home_dialog_state = None
current_dialog_state_counter = 0
current_dialog_state_begin = None
global_dialog_state_counter = 0
filepointer = None
socket = None
from random import randrange
logger = None
engaged_input = []
turn_id = 0
time = None
wizard = 3
engagement_mode = 0# this is used when engagement is not used, and the strategies are controled by response relevance only.
isAlltag =0
#folder_name = 'C:\Users\zhou\Documents\\actorimpersonator\logs\Kiosk'

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

#@yipeiw
database = {}
resource = {}
listfile = None
topic_id = 0 # the index of the starting topic
init_id =0
joke_id =0
rescource_root = 'resource'
template_list=['template/template_new.txt', 'template/template_end.txt', 'template/template_open.txt', 'template/template_expand.txt', 'template/template_init.txt', 'template/template_joke.txt', 'template/template_back.txt']
template_list = [path.join(rescource_root, name) for name in template_list]
topicfile = path.join(rescource_root, 'topic.txt')
#currentime = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
#fileout = open(currentime, 'w')
with open('dictionary_value.pkl') as f:
	dictionary_value = pickle.load(f)
def InitResource(version):
	global database, resource, socket, listflie
	if version is 'v1':
		listfile = 'cnn_qa_human_response_name.list'
	if version is 'v2':
		listfile = 'cnn_qa_human_response_name_high_app.list'
	datalist=[line.strip() for line in open(listfile)]
	database = Loader.LoadDataPair(datalist)
	resource = Loader.LoadLanguageResource()
	global TemplateLib, TopicLib, TreeState, Template

	TemplateLib = Loader.LoadTemplate(template_list)
	TopicLib = Loader.LoadTopic(topicfile)
	TreeState, Template = Control.Init()
	if wizard is 2:
		context= zmq.Context()
	#print("connectting to server")
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:5555")
#@yipeiw
def get_response(user_input,user_id,oov_mode,name_entity_mode):
	#oov_mode is used to switch on and off if we ask the unkonwn words
	#name_entity_mode is used to switch on and off if we will detect the name_entity and use the wiki api to get some knowledge expansion.
        global database, resource, turn_id, time, wizard, socket,isAlltag
	global TemplateLib, TopicLib, TreeState, Template, connection, filepointer,engaged_input, topic_id, init_id,joke_id,dictionary_value
	filepointer.write('turn_id: ' + str(turn_id) + '\n')
	filepointer.write('user_id: ' + user_id + '\n')
	turn_id = turn_id+1
	filepointer.write('time:' + str(datetime.datetime.now())+ '\n')
	filepointer.write('user_input:' + user_input + '\n')
	relavance, answer = Control.FindCandidate(database, resource, user_input,isAlltag)
	filepointer.write('relevance: ' + str(relavance)+ '\n')
	filepointer.write('RetrievedAnswer: ' + str(answer) + '\n')
	#connection.send('input engagement')
	#global connection, address
	#Log('before get response')
	if engagement_mode is 1:
		if wizard is 1:
			if connection is None:
				#Log('I asm here')
				serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				#Log('serversocket')
				serversocket.bind(('localhost', 13011))
				serversocket.listen(5)
				connection, address = serversocket.accept()
				print 'connection established'
				print connection
			connection.send('ready')
			engagement = connection.recv(64)
			#engagement = raw_input('What is the engagement state of the user of this turn?, score 1-5.  ')
		#engagement = 2
		elif wizard is 2: # this is taking the automatic engagement computed as the engagement input
			print 'Sending request'
			socket.send("ready\0")
			engagement = socket.recv()
			#print engagement
			#print("Received reply [ %s ]" %  message)
		else:# this is random generating engagement for testing.
			engagement = random.choice('12345')
		print engagement
		filepointer.write('engagement: ' + engagement + '\n')
		if int(engagement)>3:
			engaged_input.append(user_input)
		state = Control.SelectState_rel(relavance, int(engagement), TreeState,engaged_input)
	else:
		state = Control.SelectState_rel_only(relavance,TreeState)
	filepointer.write('State:' + str(state['name']) + '\n')
	Log('DM STATE is [ %s ]' %(state))
	print 'state:', state['name']
	print "candidate answer ", answer #relavance, unicodedata.normalize('NFKD',answer).encode('ascii','ignore')#answer
	#make an exception to back_state.
	output,topic_id,init_id,joke_id, engagement_input = NLG.FillTemplate(TemplateLib, TopicLib, Template[state['name']],topic_id, init_id,joke_id, engaged_input, answer)
	if isinstance(output, unicode):
		output = unicodedata.normalize('NFKD',output).encode('ascii','ignore')
#fileout = open('input_response_history.txt', 'a')
	#fileout.write(str(user_input) + '\n')
	#fileout.write(str(output) + '\n')
	#fileout.close()
	# filter name entity Piers
	#print output
	#print output.find("Piers")
	if oov_mode is 1:
		is_chosen, output_oov = oov.oov_out(user_input,dictionary_value)
                if is_chosen is 1:
			print 'oov is activated'
			output = output_oov
        if name_entity_mode is 1:
                name_entity_list = name_entity.name_entity_detection(user_input)
                if not is_chosen:
                    print name_entity

	if output.find("Piers") is not -1:
		output = output.replace("Piers","dear")
		print output
	filepointer.write('TickTockResponse:' + output + '\n')
	print "end response generation =================="
	print "==========================================="
	filepointer.flush()
	Log('OUTPUT is [ %s ]' %(output))
        return output

def LaunchQuery(env, dict):
	global requestCounter
	Log("Launching a query")

	Log(dict.keys())

	propertiesframe = env.GetSessionProperties(dict.keys())
	hub_opaque_data = propertiesframe[':hub_opaque_data']
	provider_id = hub_opaque_data[':provider_id'].strip('[').strip(']')


	try: prog_name = dict[":program"]
	except: prog_name = "main"


	inframe = dict[":inframe"]
	inframe = inframe.replace("\n{c inframe \n}", "")

	Log("Converting inframe to galaxy frame")
	#Log(inframe)

	raw_inframe_str = dict[":inframe"]
	inframe_raw_dict = ReadRawInFrame(raw_inframe_str)

	Log('RAW INFRAME is \n%s' %(str(inframe_raw_dict)))
	user_input = ''
	system_response = 'pardon me'
	try:
		user_input = inframe_raw_dict['user_input'].strip('"')
		user_input = user_input.replace('_', ' ')
	except KeyError:
		system_response = 'I am Tick Tock, how are you doing'
		pass

	if user_input:
		#system_response = user_input
		#system_response = get_response(user_input)
		filehistory = open('input_response_history.txt', 'r')
		system_tail = tail(filehistory, 4)
		filehistory.close()
		Log('USER INPUT is [ %s ]' %(user_input))
		if user_input == '':
			system_response = 'pardon me'
		elif (user_input == 'repeat') or (user_input == 'say that again') or (user_input == 'what did you say'):
			filein = open('history.txt','r')
			system_response = filein.readline()
			filein.close()
		elif len(user_input)==1:
			system_resopnse = 'can you say something longer'
		elif (system_tail[0] == system_tail[2]) and (system_tail[0] == user_input):
			system_response = 'I am having a good time talking to you.{ {BREAK TIME="2s"/}} Do you want to keep going,' \
							  ' if not, you can say goodbye'
		else:
			system_response = get_response(user_input)
			#Log(type(system_response))
		fileout = open('history.txt', 'w')
		fileout.write(str(system_response) + '\n')
		fileout.close()
		prefix = ['', 'well ... ', 'uh ... ', '', 'let me see ... ', 'oh ... ']
		cur_index = -1
		while True:
			random_index = randrange(0, len(prefix))
			if random_index != cur_index:
				break
		cur_index = random_index
		system_response = prefix[cur_index] + system_response
		#system_response_2 = unicodedata.normalize('NFKD',system_response).encode('ascii','ignore')
	resultsFrame = '{\n res %s \n}\n}' %(system_response)

#Log("outframe")
	f = Galaxy.Frame(prog_name, Galaxy.GAL_CLAUSE, {":outframe": resultsFrame})
	#Log(f)


	return f

def tail(f, n, offset=0):
	"""Reads a n lines from f with an offset of offset lines."""
	avg_line_length = 74
	to_read = n + offset
	while 1:
		try:
			f.seek(-(avg_line_length * to_read), 2)
		except IOError:
			# woops.  apparently file is smaller than what we want
			# to step back, go to the beginning instead
			f.seek(0)
		pos = f.tell()
		lines = f.read().splitlines()
		if len(lines) >= to_read or pos == 0:
			return lines[-to_read:offset and -offset or None]
		avg_line_length *= 1.3

