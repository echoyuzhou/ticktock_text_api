#!/usr/bin/etc python

import sys
import time
import os
import json

def readfile(fn):
    lines = fn.readlines()
    line_num = 1
    writelist =[]
    for line in lines:
        if line_num%3 ==1:
		tmpdict ={}
                tmpdict["question"]= line[0:-1]
        if line_num%3 ==2:
                tmpdict["answer"] = line[0:-1]
		tmpdict["docId"]='v2'
		tmpdict["qSentId"]=2016
		tmpdict["aSentId"]=2016
		writelist.append(tmpdict)
        line_num = line_num+1
    json.dump(writelist,open("v5/high_app_data_v4.json",'w'))

fn = open('v4_app_high_pairs.txt')
rating_logs = readfile(fn)
