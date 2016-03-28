#!/usr/bin/env python
import pickle
import sys
import galbackend_online
import rs_preprocess
import pprint
from time import sleep
import sqlite3

def get_alternative_responses():
    rs_preprocess.accumulate_responses()
    galbackend_online.InitLogging()
    galbackend_online.InitResource('v3')
    oov_state =1
    name_entity_state =1
    anaphra_state =1
    short_answer_state=1
    previous_history ={}
    word2vec_ranking_state =1
    tfidf_state =1
    user_list =[]
    theme = {}

    strategyDict = {
        'continue' : (True, 0),
        'switch' : (False, 0),
        'end' : (False, 1),
        'init' : (False, 2),
        'joke' : (False, 3),
        'more' : (False, 4),
    }

    conversations = []
    logRoot = '/home/ubuntu/zhou/Backend/rating_log/'
    with open(logRoot + 'conversation_list.pickle', 'rb') as f:
        conversations = pickle.load(f)

    badResponses = []
    for item in conversations:
        for response in item:
            if response['Appropriateness'] < 3:
                badResponses.append(response)

    testResponses = []
    for response in badResponses:
        for k in strategyDict.keys():
            if not k in response['Strategy']:
                try:
                    theme, strategy, altered_response, previous_history, word2vec = galbackend_online.get_response(
                             response['You'],
                             "0",
                             {"0" : response['PrevResp']},
                             {"0" : response['Theme']},
                             oov_state,
                             name_entity_state,
                             short_answer_state,
                             anaphra_state,
                             word2vec_ranking_state,
                             tfidf_state,
                             strategyDict[k])
                    alteredDict = {}
                    for y in response.keys():
                        alteredDict[y] = response[y]
                    alteredDict['TickTock'] = altered_response
                    alteredDict['Strategy'] = [k]
                    alteredDict['PrevResp'] = list(response['PrevResp'])
                    response['PrevResp'] = response['PrevResp'][:-2]
                    testResponses.append(alteredDict)
                except:
                    pass

    tmpickle = open('test_responses.pickle', 'wb')
    pickle.dump(testResponses, tmpickle, pickle.HIGHEST_PROTOCOL)
    tmpickle.close()
    return testResponses

def load_pickle_to_db():
    conn = sqlite3.connect('rs_ratings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses(
        Question TEXT NOT NULL,
        Answer TEXT NOT NULL,
        TurkID TEXT NOT NULL,
        UserID TEXT NOT NULL,
        PrevAppro INTEGER NOT NULL,
        PrevInappro INTEGER NOT NULL,
        Turn INTEGER NOT NULL,
        PrevQ TEXT NOT NULL,
        PrevA TEXT NOT NULL,
        Theme TEXT NOT NULL,
        Strategy TEXT NOT NULL,
        RatingOne INTEGER,
        RatingTwo INTEGER,
        RatingThree INTEGER,
        IDOne TEXT,
        IDTwo TEXT,
        IDThree TEXT)
    ''')
    conn.commit()
    gen_file = open('test_responses.pickle', 'rb')
    gen_response = pickle.load(gen_file)
    gen_file.close()
    for response in gen_response:
        prevQ = ''
        prevA = ''
        if len(response['PrevResp']) >= 4:
            prevQ = response['PrevResp'][-4]
            prevA = response['PrevResp'][-3]
        query_info = (response['You'], response['TickTock'], response['TurkID'], response['UserID'], response['PrevAppro'], response['PrevInappro'], response['Turn'], prevQ, prevA, response['Theme'], response['Strategy'][0])
        c.execute('''
            INSERT INTO responses VALUES (?,?,?,?,?,?,?,?,?,?,?,NULL,NULL,NULL,NULL,NULL,NULL)
        ''', query_info)
    conn.commit()

if __name__ == '__main__':
    while True:
        get_alternative_responses()
        load_pickle_to_db()
