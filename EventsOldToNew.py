import sqlite3 as lite
from SQL import *



def get():
    con = lite.connect('EventsOld.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Events')
        out = cur.fetchall()
    for i in out:
        print i

        save_event('2015-08-02 23:10:00',
                   i[4],
                   i[5],
                   i[3],i[2],i[1],
                   i[6])
        print(i)

try:
    create_events()
except:
    pass
get()








