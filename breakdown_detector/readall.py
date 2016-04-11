import os
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
  writelist =[]
  for f,r in rating_logs.iteritems():
    num_turns = len(r["Turns"])
    for i in range(1, num_turns + 1):
		tmpdict ={}
		tmpdict["question"]= r["Turns"][i]["You"]
		tmpdict["answer"] = r["Turns"][i]["TickTock"]
		tmpdict["app_value"]=r["Turns"][i]["Appropriateness"]
		tmpdict["user_id"]=r["TurkID"]
		#tmpdict["aSentId"]=2016
		writelist.append(tmpdict)
  return writelist


