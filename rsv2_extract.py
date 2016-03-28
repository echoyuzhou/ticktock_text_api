import sqlite3
import pickle
import pprint
from os import listdir
from os.path import isfile, join
from rs_preprocess import extract_convos
import re


def make_conversation_list():
    logRoot = '/home/ubuntu/zhou/Backend/rating_log/'
    logRoot2 = logRoot + 'processed_log/'
    logSuffix = re.compile('rating.*\.txt')
    logFiles = [f for f in listdir(logRoot) if isfile(join(logRoot, f)) and re.match(logSuffix, f)]
    logFiles2 = [f for f in listdir(logRoot2) if isfile(join(logRoot2, f)) and re.match(logSuffix, f)]
    results1 = extract_convos(path=logRoot, arr=logFiles)
    results2 = extract_convos(path=logRoot2, arr=logFiles2)
    return results1 + results2
def main():
    conn = sqlite3.connect('rs_ratings.db')
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS fullconvoresponses(
            Response INTEGER REFERENCES response(rowid),
            PrevHist TEXT,
            RatingOne INTEGER,
            RatingTwo INTEGER,
            RatingThree INTEGER,
            IDOne TEXT,
            IDTwo TEXT,
            IDThree TEXT
            )
        ''')

    c.execute('''SELECT Question, Turn, TurkID, UserID, rowid FROM responses WHERE RatingOne IS NOT NULL and RatingTwo IS NOT NULL and RatingThree IS NOT NULL LIMIT 60''')
    responses = c.fetchall()
    print len(responses)
    convos = make_conversation_list()
    propertyList = ['You', 'TickTock', 'TurkID', 'UserID']
    for series in convos:
        for resDict in series:
            for response in responses:
                if resDict['You'] == response[0] and resDict['Turn'] == response[1]:
                    c.execute('''SELECT * FROM fullconvoresponses WHERE Response == ?''', (response[4],))
                    if c.fetchone() == None:
                        storeText = "|".join(map(lambda x : x.replace("|", ""), resDict['PrevResp']))
                        c.execute('INSERT INTO fullconvoresponses (Response, PrevHist) VALUES (?, ?)', (response[4], storeText))
    conn.commit()

if __name__ == '__main__':
    main()
