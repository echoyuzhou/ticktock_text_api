#!/usr/bin/etc python

import sys
import socket
import time
import sqlite3
import os
import pickle
import pprint

"""
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

for item in gen_response:
    pprint.pprint(item)


def load_pickle_to_db():
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
"""
conn = sqlite3.connect('rs_ratings.db')
c = conn.cursor()
def get_unanswered_list():
    c.execute('''SELECT rowid, Question, Answer, PrevQ, PrevA, IDOne, IDTwo, IDThree FROM responses WHERE IDOne IS NULL OR IDTwo IS NULL OR IDThree IS NULL''')
    return c.fetchall()

def store_response(user_input):
    rowid, turkid, rating = user_input.split('|')
    c.execute('''SELECT * FROM responses WHERE rowid == ?''', (int(rowid),))
    entry = c.fetchone()
    print entry
    if entry[-3] is None:
        c.execute('''UPDATE responses SET RatingOne = ?, IDOne = ? WHERE rowid == ?''', (int(rating), turkid, int(rowid)))
    elif entry[-2] is None:
        c.execute('''UPDATE responses SET RatingTwo = ?, IDTwo = ? WHERE rowid == ?''', (int(rating), turkid, int(rowid)))
    elif entry[-1] is None:
        c.execute('''UPDATE responses SET RatingThree = ?, IDThree = ? WHERE rowid == ?''', (int(rating), turkid, int(rowid)))
    conn.commit()

def fetch_response(turk_id):
    unanswered = get_unanswered_list()
    for entry in unanswered:
        if unicode(turk_id) in entry:
            continue
        else:
            print entry
            print unicode(turk_id)
            res = str(entry[0]) + '|' + entry[1] + '|' + entry[2] + '|' + entry[3] + '|' + entry[4]
            return res
    return '0'

while True:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('localhost', 11432))
    serversocket.listen(5)
    connection, address = serversocket.accept()
    user_input = connection.recv(1024)
    rowid, turkid, rating = user_input.split('|')
    if rating != '0':
        store_response(user_input)
    connection.send(fetch_response(turkid))
    print 'finish sending response'
    serversocket.close()

