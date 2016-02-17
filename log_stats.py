#!/usr/bin/etc python
import sys
import time
import os
import json
import numpy

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

def get_log(rating_logs):
  writelist =[]	
  num_turns_all = []
  for f,r in rating_logs.iteritems():
    num_turns = len(r["Turns"])
    num_turns_all.append([num_turns,r["TurkID"]])
    for i in range(1, num_turns + 1):
      #if r["Turns"][i]["Appropriateness"] == "3":
		tmpdict ={}
		tmpdict["question"]= r["Turns"][i]["You"]
		tmpdict["answer"] = r["Turns"][i]["TickTock"]
		tmpdict["app"] = int(r["Turns"][i]["Appropriateness"])
		writelist.append(tmpdict)
    #writelist.append(tmpdict)
  return writelist, num_turns_all

rating_logs = readall("/home/ubuntu/zhou/Backend/rating_log/v1")
writelist, num_turns_all = get_log(rating_logs)
print 'the number of turns in total'
print numpy.sum([item[0] for item in num_turns_all])
print 'the number of turkers particpated int he study:'
print len(set(item[1] for item in num_turns_all))
print 'the mean number of conversation length'
print numpy.mean([float(item[0]) for item in num_turns_all])
print 'the std of the conversation length'
print numpy.std([float(item[0]) for item in num_turns_all])
