import sqlite3
import pprint

conn = sqlite3.connect('rs_ratings.db')
c = conn.cursor()

c.execute('''SELECT * FROM fullconvoresponses''')

x = c.fetchall()
pprint.pprint(x)
