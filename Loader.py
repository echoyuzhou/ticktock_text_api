#!/usr/bin/etc python

import nltk
from collections import defaultdict
import json
import os.path as path

def LoadLanguageResource():
        WeightRules=defaultdict(int)
        nounlist = ['NN', 'NNS', 'NNP', 'NNPS','PRP']
        verblist = ['VBP','VB','VBG','VBZ']
        whlist = ['WDT','WP','WP$','WRB']
        for noun in nounlist:
                WeightRules[noun] = 3
        for verb in verblist:
                WeightRules[verb] =1
        for wh in whlist:
                WeightRules[wh] =1
        #WeightRules['VBP','VB','VBG','VBZ','VBN','WDT','WP','WP$','WRB'] = 1
        stop_dict=defaultdict(bool)
        for word in ltk.corpus.stopwords.words('english'):
                stop_dict[word] = True
        resource = {}
        resource['rules'] = WeightRules
        resource['stop_words'] = stop_dict
        return resource

def LoadData(datalist):
	database = {}
	for datafile in datalist:
		f = open(datafile)
		line = f.readline()
		f.close()
		raw_data = json.loads(str(line.strip()))
		database = PushData(raw_data, database)
	return database

def PushData(data, database):
	last = len(database.keys())
	for pair in data:
		database[last] = nltk.word_tokenize(pair['question'])
		last += 1
		database[last] = nltk.word_tokenize(pair['answer'])
		last += 1
	return database

def LoadDataPair(datalist):
        database = {}
        database['Q'] = {}
        database['A'] = {}

        for datafile in datalist:
                f = open(datafile)
                line = f.readline()
                f.close()
                raw_data = json.loads(str(line.strip()))
                database = PushDataPair(raw_data, database)
        return database

def PushDataPair(data, database):
        last = len(database['Q'].keys())
        for pair in data:
                database['Q'][last] = nltk.word_tokenize(pair['question'])
                database['A'][last] = nltk.word_tokenize(pair['answer'])
                last += 1
        return database

def LoadTemplate(filelist):
	Library = {}
	for filepath in filelist:
		name = path.splitext(path.basename(filepath))[0]
                if name in ['template_init','template_joke']:
                    Library[name]={}
                    for line in open(filepath):
                        #print line
                        theme, line_real = line.strip().split(';')
                        #print theme
                        try:
                            Library[name][theme].append(line_real)
                        except KeyError:
                            Library[name][theme] = []
                            Library[name][theme].append(line_real)
                else:
                    Library[name] = [line.strip() for line in open(filepath)]
	return Library

def LoadTopic(topicfile):
	return [line.strip() for line in open(topicfile)]


