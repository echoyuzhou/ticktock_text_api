import sqlite3
import pprint
conn = sqlite3.connect('rs_ratings.db')
c = conn.cursor()
for item in c.execute('''SELECT * FROM responses'''):
    pprint.pprint(item)

