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

os.environ['GC_HOME'] = os.path.join(os.environ['OLYMPUS_ROOT'], 'Libraries', 'Galaxy')
sys.path.append(os.path.join(os.environ['GC_HOME'], 'contrib', 'MITRE', 'templates'))
sys.path.append(os.path.join(os.environ['OLYMPUS_ROOT'], 'bin', 'x86-nt'))

import GC_py_init
import Galaxy, GalaxyIO
import time
import unicodedata
import random
galaxyServer = None 

current_dialog_state = None
home_dialog_state = None
current_dialog_state_counter = 0
current_dialog_state_begin = None
global_dialog_state_counter = 0

from random import randrange

logger = None
def InitLogging():
    global logger
    logger = logging.getLogger('BE')
    hdlr = logging.FileHandler('BE.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)

def Log(input):
    global logger
    print input
    logger.error(input)
    sys.stdout.flush()

#@yipeiw
database = {}
resource = {}
listfile='cnn_qa.list'
rescource_root = 'resource'
template_list=['template/template_new.txt', 'template/template_end.txt', 'template/template_open.txt', 'template/template_expand.txt']
template_list = [path.join(rescource_root, name) for name in template_list]
topicfile = path.join(rescource_root, 'topic.txt')
#currentime = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
#fileout = open(currentime, 'w')

def InitResource():
	global database, resource
	datalist=[line.strip() for line in open(listfile)]
	database = Loader.LoadDataPair(datalist)
	resource = Loader.LoadLanguageResource()
	global TemplateLib, TopicLib, TreeState, Template
	TemplateLib = Loader.LoadTemplate(template_list)
	TopicLib = Loader.LoadTopic(topicfile)
	TreeState, Template = Control.Init()

def Welcome(env, dict):
    Log(dict)
    user_id = dict[":user_id"]
    # Log(user_id)
    # if env and user_id not in provider_env:
    #     provider_env[user_id] = env
    #     Log('Stored the env for user_id %s' %(user_id))
    Log("Welcome to the new Backend Server")
    prog_name = "reinitialize"
    #print Galaxy.Frame(prog_name, Galaxy.GAL_CLAUSE,dict)
    print dict
    return Galaxy.Frame(prog_name, Galaxy.GAL_CLAUSE,dict)
	


def SetDialogState(env, dict):
    global current_dialog_state
    global home_dialog_state
    global current_dialog_state_counter
    global current_dialog_state_begin
    global global_dialog_state_counter

    inframe = dict[":dialog_state"]
    # extracting the dialog state and turn number
    # main logic of updating the dialog state, such as sleeping, awake, etc
    lines = inframe.split('\n')
    new_dialog_state = None
    turn_counter = 0

    for l in lines:
        components = l.split(' = ')
        if (len(components)!=2):
            continue
        prefix = components[0]
        suffix = components[1]
        if (prefix == "dialog_state"):
            new_dialog_state = suffix
            
            if (global_dialog_state_counter == 0):
                home_dialog_state = new_dialog_state
            
            print "current_dialog_state", current_dialog_state
            print "new_dialog_state", new_dialog_state
            if (current_dialog_state == new_dialog_state):            
                current_dialog_state_counter = turn_counter - current_dialog_state_begin
                current_dialog_state = new_dialog_state
                print "cur == new, cur_counter =", current_dialog_state_counter
            else:                
                current_dialog_state = new_dialog_state
                current_dialog_state_counter = 0
                current_dialog_state_begin = turn_counter
                print "cur != new, cur_begin =", current_dialog_state_begin
                print "cur_counter =", current_dialog_state_counter

            
        elif (prefix == "turn_number"):
            turn_counter = int(suffix)
            print "get turn counter", turn_counter
            if (global_dialog_state_counter == -1 or turn_counter == 0):
                global_dialog_state_counter = 0
                #print "set g_d_s_c to 0"
            else:
                global_dialog_state_counter = turn_counter
                #print "g_d_s_c =", turn_counter

            #print "end of turn counter"
    print "==============================="
    print "DIALOG STATE is", current_dialog_state
    print "CURRENT TURN NUMBER is", current_dialog_state_counter

    state_out = -1

    if (current_dialog_state.endswith(aware_state)):
        print "system is aware of the person but can't see"
        state_out = 4
    elif (current_dialog_state == home_dialog_state):
        print "system is sleeping now ... zzz"
        state_out = 1
    elif (current_dialog_state_counter >= 1):
        print "system is puzzled ... "
        state_out = 2
    else:
        print "system can understand you." 
        state_out = 3

    count = 1
    onDialogState(state_out)
    print "==============================="
    # end of the main logic
    
    prog_name = "main"
    outframe = "got dialog state"
    f = Galaxy.Frame(prog_name, Galaxy.GAL_CLAUSE, {":outframe": outframe})
    return f


def ReadRawInFrame(inframe_str):
    
    Log("In Read Raw InFrame")
    inframe_str = inframe_str.strip('\n').strip('}').strip('{')
    inframe_dict = {}
    inframe_lines = inframe_str.split('\n')	
    list_holder = None
    current_list_key = None
    in_array = False
    Log(inframe_lines)
    Log("######")
    for line in inframe_lines:
        line = line.strip('\n').strip(' ').lower()
        if in_array is False:
            # very likely key value pairs
            if ' ' in line:
                if ':' in line:
                    #beginning of array?
                    Log(line)
                    key, value = line.split(' ')
                    if re.match('^:\d+$', value) is not None:
                        in_array = True
                        list_holder = []
                        current_list_key = key
                        
                else:
                    Log(line)
                    key, value = line.split(' ')
                    inframe_dict[key] = value
        else:
            if line != '{' and line !='}':
                if ' ' in line:
                    line = line.replace(' ', '_')
                list_holder.append(line)
            elif line == '}':
                new_list = list_holder
                inframe_dict[current_list_key] = new_list
                list_holder = None
                in_array = False

    return inframe_dict
    

def SayThanks():
    msg = {'[schedule_final]':'Your activity has been scheduled'}
    SendMessageToDM('A', '[schedule]', msg)
    SendMessageToDM('B', '[schedule]', msg)

#@yipeiw
def get_response(user_input):
    global database, resource
    global TemplateLib, TopicLib, TreeState, Template
    relavance, answer = Control.FindCandidate(database, resource, user_input)
    state = Control.SelectState(relavance, TreeState)
    Log('DM STATE is [ %s ]' %(state))
    print 'state:', state['name']
    print "candidate answer ", relavance, answer
    output = NLG.FillTemplate(TemplateLib, TopicLib, Template[state['name']], answer)
    if isinstance(output, str):
        output2 = output
    else:
        output2 = unicodedata.normalize('NFKD',output).encode('ascii','ignore')
    Log('OUTPUT is [ %s ]' %(output2))
    #fileout = open('input_response_history.txt', 'a')
    #fileout.write(str(user_input) + '\n')
    #fileout.write(str(output) + '\n')
    #fileout.close()
    return output2

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
    system_response = random.choice(['pardon me ?','can you say that again ?', 'excuse me?'])
    try:
        user_input = inframe_raw_dict['user_input'].strip('"')
        user_input = user_input.replace('_', ' ')
    except KeyError:
        system_response = 'I am TickTock, how are you doing'
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
        elif ((user_input.find('repeat')> 0) or (user_input.find('say that again')>0) or (user_input.find('excuse me')>0)):
            filein = open('history.txt', 'r')
            system_response = 'sure ... ' + filein.readline()
            filein.close()
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

# oas in C is -increment i.

OAS = [("-increment i", "initial increment")]

# Write a wrapper for the usage check.

class BackEnd(GalaxyIO.Server):
    def CheckUsage(self, oas_list, args):
        global InitialIncrement
        data, out_args = GalaxyIO.Server.CheckUsage(self, OAS + oas_list, args)
        if data.has_key("-increment"):
            InitialIncrement = data["-increment"][0]
            del data["-increment"]
        return data, out_args
    

def SendToHub(provider, frame):
    prog_name = "main"
    global provider_env
    env = provider_env[provider]
    if env:
        f = Galaxy.Frame(prog_name, Galaxy.GAL_CLAUSE, frame)

        try: 
            env.WriteFrame(f) 
        except GalaxyIO.DispatchError: 
            Log('ERROR: cannot send frame')


def SendMessageToDM(provider, msgtype, msg):
    prog_name = "main"
    
    print  'lets say hello to DM async way'
    
    nets = []
    parse_str = []
    hyp_str = []
    for k, v in msg.iteritems():
        net = Galaxy.Frame("slot", Galaxy.GAL_CLAUSE, {':name':k, ':contents':v})
        nets.append(net)
        parse_str.append('( %s ( %s ) )' %(k, v))
        hyp_str.append(v)
        
     #Log('Test Printing the nets\n %s' %(Galaxy.OPr(nets)))
     #Log('----------THEEND OF NETS -------')
    gfSlot = {}    
    gfParse = {}
    gfSlot[":nets"] = nets
    gfSlot[":numnets"] = len(nets)
    gfSlot[":name"] = msgtype
    gfSlot[":contents"] = ' '.join(hyp_str)
    gfSlot[":frame"] = "Fake Frame"
    gfSlotFrame = Galaxy.Frame("slot", Galaxy.GAL_CLAUSE, gfSlot)
    slots = [gfSlotFrame]
     
     #Log('Test Printing the slots\n %s' %(Galaxy.OPr(slots)))
     #Log('----------THEEND OF SLOTS-------')
    gfParse[":gal_slotsstring"] = Galaxy.OPr(slots)
    gfParse[":slots"] = slots
    gfParse[":numslots"] = 1
    gfParse[":uttid"] = "-1"
    gfParse[":hyp"] = ' '.join(hyp_str)
    gfParse[":hyp_index"] = 0
    gfParse[":hyp_num_parses"] = 1
    gfParse[":decoder_score"] = 0.0
    gfParse[":am_score"] = 0.0
    gfParse[":lm_score"] = 0.0
    gfParse[":frame_num"] = 0
    gfParse[":acoustic_gap_norm"] = 0.0
    gfParse[":avg_wordconf"] = 0.0
    gfParse[":min_wordconf"] = 0.0
    gfParse[":max_wordconf"] = 0.0
    gfParse[":avg_validwordconf"] = 0.0
    gfParse[":min_validwordconf"] = 0.0
    gfParse[":max_validwordconf"] = 0.0
    gfParse[":parsestring"] = ' '.join(parse_str)
    Log('Test printing the parse frame')
    gfParseFrame = Galaxy.Frame("utterance", Galaxy.GAL_CLAUSE, gfParse)
     #gfParseFrame.Print()
    
    parses = [gfParseFrame]
    confhyps = [gfParseFrame]
    
    f = Galaxy.Frame(prog_name, Galaxy.GAL_CLAUSE, {":confhyps": confhyps, 
                                                    ":parses": parses, 
                                                    ':total_numparses': 1, 
                                                    ':input_source': 'gal_be',
                                                    ':gated_input': 'gated_input'})
    Log("Sending the message to DM")
    #Log(f)
    SendToHub(provider, f)
    Log("Sent to DM")

def GalInterface():
    InitLogging()
    Log("Starting Galaxy Server")
    global galaxyServer

    #load database and other resources @yipeiw   
    InitResource()
 
    galaxyServer = BackEnd(sys.argv, "gal_be",
                    default_port = 2900)
    galaxyServer.AddDispatchFunction("set_dialog_state", SetDialogState,
            [[], Galaxy.GAL_OTHER_KEYS_NEVER,
            Galaxy.GAL_REPLY_NONE, [],
            Galaxy.GAL_OTHER_KEYS_NEVER])
    galaxyServer.AddDispatchFunction("launch_query", LaunchQuery,
            [[], Galaxy.GAL_OTHER_KEYS_NEVER,
            Galaxy.GAL_REPLY_NONE, [],
            Galaxy.GAL_OTHER_KEYS_NEVER])
    galaxyServer.AddDispatchFunction("reinitialize", Welcome,
            [[], Galaxy.GAL_OTHER_KEYS_NEVER,
            Galaxy.GAL_REPLY_NONE, [],
            Galaxy.GAL_OTHER_KEYS_NEVER])
    galaxyServer.AddDispatchFunction("welcome", Welcome,
            [[], Galaxy.GAL_OTHER_KEYS_NEVER,
            Galaxy.GAL_REPLY_NONE, [],
            Galaxy.GAL_OTHER_KEYS_NEVER])

    galaxyServer.RunServer()
    
    
def MonitorThread():
        current_focus = {}

def LaunchQueryDebug(user_input):
# this guy is only used in debugging
        #system_response = user_input
        #system_response = get_response(user_input)
        filehistory = open('input_response_history.txt', 'r')
        system_tail = tail(filehistory, 4)
        filehistory.close()
        Log('USER INPUT is [ %s ]' %(user_input))
        if user_input == '':
            system_response = random.choice(['pardon me ?','can you say that again ?', 'excuse me?'])
        elif ((user_input.find('repeat')> 0) or (user_input.find('say that again')>0) or (user_input.find('excuse me')>0)):
            filein = open('history.txt', 'r')
            system_response = 'sure ... ' + filein.readline()
            filein.close()
        elif (system_tail[0] == system_tail[2]) and (system_tail[0] == user_input):
            system_response = 'I am having a good time, do you want to keep going,...' \
                              ' if not, you can say goodbye'
        else:
            system_response = get_response(user_input)
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
        print(system_response)

    
if __name__ == "__main__":
    gt = Thread(target=GalInterface)
    gt.start()
    gt.join()
