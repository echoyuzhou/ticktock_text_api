#!/usr/bin/etc python

import sys
import socket
import time
import sqlite3
import os

def readfile(fn):
  result = {}
  result["Turns"] = {}
  current_turn = 0
  key_index = 0
  keys = ["Turn", "You", "TickTock", "Appropriateness","Strategy"]
  for l in open(fn):
    if ":" in l:
      key = l.split(":")[0]
      value = ":".join(l.split(":")[1:]).strip()
      if key == "TurkID" or key == "UserID":
        result[key] = value
      else:
        #if keys[key_index%4] != key:
        #  print l
        #  assert(False)
        key_index += 1
        if key == "Turn":
          current_turn = int(value)
          result["Turns"][current_turn] = {}
        elif key in keys[1:]:
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

def get_log(rating_logs,f_r):
  for f,r in rating_logs.iteritems():
    num_turns = len(r["Turns"])
    for i in range(1, num_turns + 1):
      if r["Turns"][i]["Appropriateness"] is not "3" and i > 1:
        f_r.write('" Participant: ' + r["Turns"][i-1]["You"].replace('"','') + '",'+ '" TickTock: ' + r["Turns"][i-1]["TickTock"].replace('"', '') + '",' + ' " Participant: ' + r["Turns"][i]["You"].replace('"', '').replace(',','') + '", \n')


rating_logs = readall("/home/ubuntu/zhou/Backend/rating_log/v2")
f = open('userinput_annotation.csv','w')
get_log(rating_logs,f)

