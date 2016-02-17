#!/usr/env/python3
import logging
import json
from gensim import corpora, models, similarities


fileLists = 
['AHC_CNN.list', 
'AHC_json.list', 
'cnn_qa_human_response.list',
'cnn_qa_human_response_name_high_app.list',
'cnn_qa_human_response_name.list',
'cnn_qa.list',
'conversation.list',
'friends.list',
'human_response_jasn.list',
'reddit.list',
'v2.list']

compiledFileList = 'compList.list'

for list in fileLists:

