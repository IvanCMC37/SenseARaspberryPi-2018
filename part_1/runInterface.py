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

    # assign data to related array & string formatting
    for t in temps:
        x =  str(t)
        temp = x[1:len(x)-2]
        print(temp)
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

    yhumids[:]
    # assign data to related array & string formatting
    for h in humids:
        x =  str(h)
        humid = x[1:len(x)-2]
        print(humid)
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

    # assign data to related array
    for d in dates:
        x =  str(d)
        date = x[2:len(x)-3]
        print(date)
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

    #x = [dt.datetime.strptime(y,'%d/%m/%y %H:%M:%S').date() for y in xdates]
    #print(x)
    plt.clf()
    plt.cla()
    plt.close()
    plt.figure(figsize=(20,10))
    #x = np.array([dt.datetime(i[], i[3:4], i[0:1], i,0) for i in xdates])
    x = np.array([dt.datetime(2013, 9, 28, i) for i in  range(len(xdates))])
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%M/%Y %H:%M:%S'))
    #plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())

    #x =[1,2,3,4,5,6,7,8]
    print(len(x))
    print(x)
    y = [2,5,3,6,2,1,6,2]
    z = [4,2,1,5,6,2,1,3]
    plt.grid()
    plt.plot(x,ytemps,'r-o',label = "temperature(C)")
    #start, end = plt.gca().get_xlim()
    #plt.gca().xaxis.set_ticks(np.arange(start, end, 5))
    #plt.plot( x,yhumids,'g-',label ="humidity(%)")
    #plt.gcf().autofmt_xdate()
    plt.legend(loc='upper right')
    plt.ylabel('Value')
    plt.xlabel('Date Time')
    plt.savefig('static/temp.png')
    
    return render_template('temp.html', temp = "static/temp.png")

# define route of showing humidity graph
# @app.route("/humid")
# def plotHumid():
#     # fetch latest data
#     fetchTempData()
#     fetchHumidData()
#     z =[1,2,3,4,5,6,7,8]
#     plt.figure()
#     plt.plot(z,yhumids,marker='o')
#     #plt.gcf().autofmt_xdate()
#     plt.ylabel('Humidity (%)')
#     plt.xlabel('Date Time')
#     plt.savefig('static/humid.png')
#     return render_template('humid.html', humid = "static/humid.png")
    

host = os.popen('hostname -I').read()
#port set to a non privileged port above 1024
app.run(host='192.168.1.12', port=5000, debug=False)