#!/usr/bin/etc python
# this is used to random sample 10 percent of the turns in totall, and then write them into two csv files.
# one is emply of appropriate scores.
import sys
import time
import os
import json
import random

def readfile(fn):
  result = {}
  result["Turns"] = {}
  current_turn = 0
  key_index = 0
  keys = ["Turn", "You", "TickTock", "Appropriateness"]
  for l in open(fn):
    if ":" in l:
      key = l.split(":")[0]
      value = ":".join(l.split(":")[1:]).strip()
      if key == "TurkID" or key == "UserID":
        result[key] = value
      else:
        if keys[key_index%4] != key:
          print l
          assert(False)
        key_index += 1
        if key == "Turn":
          current_turn = int(value)
          result["Turns"][current_turn] = {}
        elif key in keys[1:4]:
          result["Turns"][current_turn][key] = value
        else:
          assert(False)
  return result

def readall(dir_path):
  result = {}
  for f in os.listdir(dir_path):
    if ".txt" in f and "rating" in f:
      full_path = os.path.join(dir_path, f)
      result[full_path] = readfile(full_path)
  return result

def write_csv(rating_logs):
  writelist =[]	

  f_ex = open('rating_expert.csv','w')
  f_org = open('rating_org.csv','w')
  for f,r in rating_logs.iteritems():
    num_turns = len(r["Turns"])
    select_num = random.sample(range(1,num_turns),int(num_turns/10))
    for i in select_num:
		tmpdict ={}
		tmpdict["app"] = r["Turns"][i]["Appropriateness"]
		tmpdict["question"]= r["Turns"][i]["You"]
		tmpdict["answer"] = r["Turns"][i]["TickTock"]
		f_ex.write('"'+' '.join(tmpdict["question"])+'",'+ '"'+' '.join(tmpdict["answer"])+'"\n')
		f_org.write('"'+' '.join(tmpdict["question"])+'",'+ '"'+ ' '.join(tmpdict["answer"])+'","'+ tmpdict["app"] +'"\n')
	
rating_logs = readall("/home/ubuntu/zhou/Backend/rating_log/v1")
write_csv(rating_logs)

