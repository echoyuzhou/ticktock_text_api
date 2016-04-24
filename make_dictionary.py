import nltk
import re
import pickle
import json
import os.path as path
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
    for pair in data:
        word = nltk.word_tokenize(pair['question']) +nltk.word_tokenize(pair['answer'])
        database = database +[item.lower() for item in word]
    return database

def main():
    datalist = line.strip() for line in open('cnn_qa_human_response_name_high_app.list')]
    database = LoadData(datalist)
    database = list(set(database))

    with open('dictionary_value.pkl','w') as f:
        pickle.dump(database,f)
if __name__= "__main__":
    main()




