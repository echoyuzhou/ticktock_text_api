#!/usr/bin/env python

from os import listdir, walk
from os.path import isfile, join
import re
import pickle
import pprint
import csv
import gensim
import numpy
import nltk
from itertools import izip_longest
import string

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

def tt_switch_length(convo):
    tot_dist = 0
    tot_switch = 0
    swi_idx = -1

    for x in range(0, len(convo)):
        if len(convo[x]['Strategy']) == 1 and convo[x]['Strategy'][0] == 'switch':
            if swi_idx != -1:
                tot_dist += x - swi_idx
                tot_switch += 1
            swi_idx = x

    return float(tot_dist) / (tot_switch + 1)

def cosine_sim(vec1, vec2):
    return numpy.dot(vec1, vec2) / (numpy.linalg.norm(vec1) * numpy.linalg.norm(vec2))

def word2vec_similarity(convo, model):
    similarity_sums = [0.0, 0.0, 0.0, 0.0]
    prev_vec_1 = None
    prev_vec_2 = None
    for idx in range(0, len(convo)):
        tmp1 = nltk.word_tokenize(convo[idx]['You'])
        tmp2 = nltk.word_tokenize(convo[idx]['TickTock'])

        cur_vec_1 = []
        for word in tmp1:
            try:
                cur_vec_1 += [model[word]]
            except:
                pass
        if len(cur_vec_1) == 0:
            continue

        cur_vec_2 = []
        for word in tmp2:
            try:
                cur_vec_2 += [model[word]]
            except:
                pass
        if len(cur_vec_2) == 0:
            continue

        cur_vec_1 = sum(cur_vec_1)
        cur_vec_2 = sum(cur_vec_2)

        if prev_vec_1 == None:
            prev_vec_1 = cur_vec_1
            prev_vec_2 = cur_vec_2
        else:
            similarity_sums[0] += cosine_sim(prev_vec_1, cur_vec_1)
            similarity_sums[1] += cosine_sim(prev_vec_2, cur_vec_2)
            similarity_sums[2] += cosine_sim(cur_vec_1, cur_vec_2)
            similarity_sums[3] += cosine_sim(prev_vec_2, cur_vec_1)
            prev_vec_1 = cur_vec_1
            prev_vec_2 = cur_vec_2

    print similarity_sums
    return map(lambda x : x / (len(convo) + 1), similarity_sums)

def strat_count(convo):
    strat_list = ['init', 'switch', 'continue', 'end']
    count_list = [0 for x in strat_list]
    for resp in convo:
        for idx in range(0, len(strat_list)):
            if strat_list[idx] in resp['Strategy']:
                count_list[idx] += 1
    return map(lambda x : float(x) / (len(convo) + 1), count_list)

def keyword_count(convo):
    keywords = ['sense', 'something', 'else', 'how', 'what', 'who', 'when', 'where', 'why']
    count_list = [0 for x in keywords]
    exclude = set(string.punctuation)
    for response in convo:
        bare = (''.join(ch for ch in ((response['TickTock'] + ' ' + response['You'])) if ch not in exclude)).lower().split()
        for word in bare:
            for idx in range(0, len(keywords)):
                if keywords[idx] == word:
                    count_list[idx] += 1
    return count_list




def extract_features(convo):
    #word2vec disbaled since not all words are in the model.
    word2vec_model = gensim.models.Word2Vec.load('/tmp/word2vec_100_break')
    word2vec_scores = word2vec_similarity(convo, word2vec_model)
    strat_scores = strat_count(convo)
    response_num = len(convo)
    swi_len = tt_switch_length(convo)
    keyword_scores = keyword_count(convo)
    return [response_num, swi_len] + strat_scores + keyword_scores + word2vec_scores


def get_convolist():
    data_file = open('depth_data.csv')
    data_csv = csv.reader(data_file, delimiter=',')
    file_list = [{'name' : row[0].strip(), 'label' : int(row[1])} for row in data_csv]
    log_root = '/home/ubuntu/zhou/Backend/rating_log/'
    count = 0
    print len(file_list)
    for root, subdirs, files in walk(log_root):
        for f in files:
            for item in file_list:
                if f == item['name']:
                    if 'path' not in item.keys():
                        item['path'] = join(root, f)
                        count += 1
    for item in file_list:
        if 'path' not in item.keys():
            print item['name']
    print count
    for item in file_list:
        item['convo'] = extract_convo(item['path'])
    return file_list

def extract_convo(path):
    themeList = ['music', 'movies', 'board games', 'sports', 'politcs']
    responseList = []
    with open(path, 'r') as log:
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
    return responseList

def create_learnable(convolist):
    feature_list = []
    label_list = []
    for convo in convolist:
        feature_list.append(extract_features(convo['convo']))
        label_list.append(convo['label'])
    return feature_list, label_list



if __name__ == "__main__":
    f_list, l_list = create_learnable(get_convolist())
    pickle.dump(f_list, open('features.pkl', 'wb'))
    pickle.dump(l_list, open('labels.pkl', 'wb'))
