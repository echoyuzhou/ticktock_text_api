import sqlite3
import pprint
import socket
import os
from random import shuffle



def get_need_rating(c):
    c.execute('''SELECT rowid, PrevHist, Response FROM fullconvoresponses WHERE IDOne IS NULL OR IDTwo IS NULL OR IDThree IS NULL''')
    return c.fetchall()

def store_response(c, conn, rowid, turkid, rating):
    print rowid, turkid, rating
    c.execute('''SELECT IDOne, IDTwo, IDThree FROM fullconvoresponses WHERE rowid == ?''', (int(rowid),))
    entry = c.fetchone()
    print entry
    if entry[0] is None:
        print 'Entered zerot choirce'
        c.execute('''UPDATE fullconvoresponses SET RatingOne = ?, IDOne = ? WHERE rowid == ?''', (int(rating), turkid, int(rowid)))
    elif entry[1] is None:
        print 'Entered fiest choirce'
        c.execute('''UPDATE fullconvoresponses SET RatingTwo = ?, IDTwo = ? WHERE rowid == ?''', (int(rating), turkid, int(rowid)))
    elif entry[2] is None:
        print 'Entered 2nd choirce'
        c.execute('''UPDATE fullconvoresponses SET RatingThree = ?, IDThree = ? WHERE rowid == ?''', (int(rating), turkid, int(rowid)))
    c.execute('''SELECT IDOne, IDTwo, IDThree FROM fullconvoresponses WHERE rowid == ?''', (int(rowid),))
    print c.fetchone()
    conn.commit()


def fetch_response(c, turk_id):
    unanswered = get_need_rating(c)
    shuffle(unanswered)
    for entry in unanswered:
        if unicode(turk_id) in entry:
            continue
        else:
            c.execute('''SELECT Question, Answer FROM responses WHERE rowid == ?''', (int(entry[2]),))
            qa = c.fetchone()
            res = str(entry[0]) + '|' + entry[1] + '|' + qa[0] + '|' + qa[1]
            return res
    return '0'

if __name__ == "__main__":
    conn = sqlite3.connect('rs_ratings.db')
    c = conn.cursor()
    c.execute('''SELECT Response, PrevHist FROM fullconvoresponses''')
    prevs = c.fetchall()
    for item in prevs:
        c.execute('''SELECT Question, Answer FROM responses WHERE rowid == ?''',(item[0],))
        print item
        print c.fetchone()

    while True:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('localhost', 11532))
        serversocket.listen(5)
        connection, address = serversocket.accept()
        user_input = connection.recv(1024)
        print user_input
        rowid, turkid, rating = user_input.split('|')
        if rating != '0':
            store_response(c, conn, rowid, turkid, rating)
        connection.send(fetch_response(c, turkid))
        print 'finish sending response'
        serversocket.close()

