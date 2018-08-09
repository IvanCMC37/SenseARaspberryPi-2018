import sqlite3 as lite
import sys
con = lite.connect('database.bieber')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp REAL, humidity REAL)")
