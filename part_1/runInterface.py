#!/usr/bin/env python3
import os
import sqlite3 as lite
from flask import Flask, request, render_template, send_file
import base64, io
import datetime as dt
import matplotlib
# dont use windows backend by default
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np



# using flask
app = Flask(__name__, template_folder='views')

# define database path
dbname = '/home/pi/SenseARaspberryPi/db/database.bieber'

# array objects for ploting the graph later
xdates = []
ytemps = []
yhumids = []

# function to fetch all temp data from database table
def fetchTempData():
    # setting up database
    conn=lite.connect(dbname)
    curs=conn.cursor()

    # fetch the data
    curs.execute("SELECT temp FROM SenseHat_data")
    temps = curs.fetchall()

    ytemps.clear()
    # assign data to related array & string formatting
    for t in temps:
        x =  str(t)
        temp = x[1:len(x)-2]
        ytemps.append(float(temp))
    
    # close the connection
    conn.close()

# function to fetch all humidity data from database table
def fetchHumidData():
    # setting up database
    conn=lite.connect(dbname)
    curs=conn.cursor()

    # fetch the data
    curs.execute("SELECT humidity FROM SenseHat_data")
    humids = curs.fetchall()

    yhumids.clear()
    # assign data to related array & string formatting
    for h in humids:
        x =  str(h)
        humid = x[1:len(x)-2]
        yhumids.append(float(humid))
    
    # close the connection
    conn.close()

# function to fetch all time data from database table
def fetchTimeData():
    # setting up database
    conn=lite.connect(dbname)
    curs=conn.cursor()

    # fetch the data
    curs.execute("SELECT timestamp FROM SenseHat_data")
    dates = curs.fetchall()

    xdates.clear()
    # assign data to related array
    for d in dates:
        x =  str(d)
        date = x[2:len(x)-3]
        xdates.append(date)
    
    # close the connection
    conn.close()

# define route of showing temperature graph
@app.route("/")
def plotTemp():
    # fetch latest data
    fetchTempData()
    fetchTimeData()
    fetchHumidData()

    # split uup date data in even manner
    x = np.array([dt.datetime(int(xdates[i][6:8]), int(xdates[0][3:5]), int(xdates[i][0:2]),int(xdates[i][9:11]),i ) for i in  range(len(xdates))])

    # plot the graph
    plt.figure(figsize=(20,10))
    plt.grid()
    plt.plot(x,ytemps,'r-o',label = "temperature(C)")
    plt.plot(x,yhumids,'g-*',label ="humidity(%)")
    plt.legend(loc='upper right')
    plt.ylabel('Value')
    plt.xlabel('Date Time')
    plt.savefig('static/dataGraph.png')
    
    return render_template('index.html', data = "static/dataGraph.png")
    
host = os.popen('hostname -I').read()
#port set to a non privileged port above 1024
app.run(host='192.168.1.12', port=5000, debug=False)