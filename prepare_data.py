import pickle
import json
import load_json
datalist = [line.strip() for line in open ('cnn_hr_v1_v2.list')]
database = load_json.LoadData(datalist)
with open('word2vec/test_complete.pkl','w') as f:
	pickle.dump(database,f)


