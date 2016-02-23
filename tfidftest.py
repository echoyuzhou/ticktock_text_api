from gensim import models, corpora
import galbackend_online
import sys
import socket
import time
sampleRequest = 'You are a good person'
galbackend_online.InitLogging()
galbackend_online.InitResource('v3')
response = galbackend_online.get_response(sampleRequest, '322',0,0,0, tfidf_mode=1)

