#!/usr/bin/etc python

import sys
import socket
import time
import sqlite3
import os
'''
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
         # print l
         # assert(False)
        key_index += 1
        if key == "Turn":
          current_turn = int(value)
          result["Turns"][current_turn] = {}
        elif key in keys[1:]:
          result["Turns"][current_turn][key] = value
        else:
          assert(False)
  return result
'''

def readfile(fn):
  result = {}
  result["Turns"] = {}
  current_turn = 0
  key_index = 0
  keys = ["Turn", "You", "TickTock", "Appropriateness", "Strategy"]
  for l in open(fn):
    if ":" in l:
      key = l.split(":")[0]
      value = ":".join(l.split(":")[1:]).strip()
      if key == "TurkID" or key == "UserID":
        result[key] = value
      else:
       # if keys[key_index%5] != key:
       #   print l
       #   assert(False)
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

def get_log(rating_logs):
  inapp = 0
  inte = 0
  app = 0
  ttl = 0
  for f,r in rating_logs.iteritems():
    num_turns = len(r["Turns"])
    for i in range(1, num_turns + 1):
      if r["Turns"][i]["Appropriateness"] == "1":
	inapp = inapp + 1
      if r["Turns"][i]["Appropriateness"] == "2":
	inte = inte + 1
      if r["Turns"][i]["Appropriateness"] == "3":
	app = app + 1
        #print str(inapp)
      ttl = ttl+1
  return inapp, inte, app, ttl
        #yield "Participant: " + r["Turns"][i-1]["You"] + "<br>\nTickTock: " + r["Turns"][i-1]["TickTock"] + "<br>\n Participant: " + r["Turns"][i]["You"]


rating_logs = readall("/home/ubuntu/zhou/Backend/rating_log/")
#print rating_logs
inapp, inte, app, ttl = get_log(rating_logs)
print "the number of inapproprate turns"
print str(inapp), float(inapp)/float(ttl)
print "the number of interpretable turns"
print str(inte), float(inte)/float(ttl)
print "the number of appropriate nurns"
print str(app), float(app)/float(ttl)
print "the total number of turns"
print str(ttl)
percent = float(inapp)/float(ttl)*100
print "the percent of inapproprate responses in this version: "
print "%.2f" %percent

