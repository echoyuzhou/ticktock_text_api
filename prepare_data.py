import pickle
import json
import load_json
datalist = [line.strip() for line in open ('cnn_qa_human_response_name_high_app.list')]
database = load_json.LoadData(datalist)
with open('word2vec/test.pkl','w') as f:
	pickle.dump(database,f)


