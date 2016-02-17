import pickle
import json
import load_json
datalist = [line.strip() for line in open ('cnn_qa_human_response_name.list')]
database = load_json.LoadData(datalist)
print len(database)
with open('word2vec/test_v1.pkl','w') as f:
	pickle.dump(database,f)


