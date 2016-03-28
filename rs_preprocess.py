#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
import re
from itertools import izip_longest
import pickle
import pprint

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


def accumulate_responses(cumulative=False):
    logRoot = '/home/ubuntu/zhou/Backend/rating_log/'
    logRoot2 = logRoot + 'processed_log/'
    logSuffix = re.compile('rating.*\.txt')
    ignoreList = []
    if isfile(join(logRoot, '.preprocess_ignore')):
        tmp = open(join(logRoot, '.preprocess_ignore'))
        ignoreList = [line.rstrip('\n') for line in tmp.readlines()]
        tmp.close()

    logFiles = [f for f in listdir(logRoot) if isfile(join(logRoot, f)) and re.match(logSuffix, f) and (f not in ignoreList or cumulative)]
    logFiles2 = [f for f in listdir(logRoot2) if isfile(join(logRoot2, f)) and re.match(logSuffix, f) and (f not in ignoreList or cumulative)]
    results1 = extract_convos(path=logRoot, arr=logFiles)
    results2 = extract_convos(path=logRoot2, arr=logFiles2)
    results1 += results2
    picklef = open(join(logRoot, 'conversation_list.pickle'), 'wb');
    pickle.dump(results1, picklef, pickle.HIGHEST_PROTOCOL)
    picklef.close()
    if not cumulative:
        tmp = open(join(logRoot, '.preprocess_ignore'), 'a')
        for f in (logFiles + logFiles2):
            tmp.write(f + '\n')
        tmp.close()

    picklef = open(join(logRoot, 'conversation_list.pickle'), 'rb');
    test = pickle.load(picklef)
    picklef.close()
    for item in test:
        pprint.pprint(item)

def extract_convos(path, arr):
    themeList = ['music', 'movies', 'board games', 'sports', 'politcs']
    convoList = []
    for f in arr:
        with open(join(path, f), 'r') as log:
            responseList = []
            lines = log.readlines()
            lines = [x.rstrip('\n') for x in lines]
            turkID = lines[0].replace('TurkID: ', '')
            userID = lines[1].replace('UserID: ', '')
            theme = [lines[4].split(' ')[-1]]
            approNum = 0
            inapproNum = 0
            for response in grouper(lines[2:], 6):
                resDict = {}
                resDict['TurkID'] = turkID
                resDict['UserID'] = userID
                resDict['Turn'] = int(response[0].replace('Turn: ', ''))
                resDict['You'] = response[1].replace('You: ', '')
                resDict['TickTock'] = response[2].replace('TickTock: ', '')

                resDict['Appropriateness'] = int(response[3].replace('Appropriateness: ', ''))
                if resDict['Appropriateness'] < 3:
                    inapproNum = inapproNum + 1
                else:
                    approNum = approNum + 1
                resDict['PrevInappro'] = inapproNum
                resDict['PrevAppro'] = approNum

                resDict['Strategy'] = [x.strip() for x in response[4].replace('[', '').replace(']', '').replace('\'', '').replace('Strategy: ', '').split(',')]
                stratNum = len(resDict['Strategy'])
                if 'new' in resDict['Strategy'] or 'switch' in resDict['Strategy'] and (stratNum == 1 or ('anaphora' in resDict['Strategy'] and stratNum == 1)):
                    theme = resDict['TickTock'].split(' ')[-1]
                    if theme == 'games':
                        theme = 'board games'
                resDict['Theme'] = theme
                if resDict['Theme'] in themeList:
                    responseList += [resDict]
            for x in range(0, len(responseList)):
                if x == 0:
                    responseList[x]['PrevResp'] = []
                else:
                    responseList[x]['PrevResp'] = list(responseList[x - 1]['PrevResp']) + [responseList[x - 1]['You'], responseList[x - 1]['TickTock']]
            convoList.append(responseList)

    return convoList
if __name__ == "__main__":
    accumulate_responses(True)
