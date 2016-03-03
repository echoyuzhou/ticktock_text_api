import json
import nltk

def LoadData(datalist):
         database = []
         for datafile in datalist:
                 f = open(datafile)
                 line = f.readline()
                 f.close()
                 raw_data = json.loads(str(line.strip()))
                 database = PushData(raw_data, database)
         return database

def PushData(data, database):
         #last = len(database)
         for pair in data:
                 database.append(nltk.word_tokenize(pair['question']))
                 database.append(nltk.word_tokenize(pair['answer']))
         return database

def PushDataPair(data, database):
         last = len(database['Q'].keys())
         for pair in data:
                 database['Q'][last] = pair['question'].split()
                 database['A'][last] = pair['answer'].split()
                 last += 1
         return database

def LoadData_Q(datalist):
         database = []
         for datafile in datalist:
                 f = open(datafile)
                 line = f.readline()
                 f.close()
                 raw_data = json.loads(str(line.strip()))
                 database = PushData_Q(raw_data, database)
         return database

def PushData_Q(data, database):
         #last = len(database)
         for pair in data:
                 database.append(pair['question'].split())
                 #last += 1
                 #database.append(pair['answer'].split())
                 #last += 1
         return database


