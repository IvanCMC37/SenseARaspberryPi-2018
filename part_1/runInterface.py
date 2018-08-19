#!/usr/bin/env python3
import os
import sqlite3 as lite
from flask import Flask, request, render_template, send_file
import matplotlib
# dont use windows backend by default
matplotlib.use('Agg')
import base64, io
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

app = Flask(__name__, template_folder='views')
dbname = '/home/pi/SenseARaspberryPi/db/database.bieber'
@app.route("/")
def plotTemp():
    conn=lite.connect(dbname)
    xdates =[]
    ytemps =[]
    curs=conn.cursor()
    curs.execute("SELECT temp FROM SenseHat_data")
    tempData_ = curs.fetchall()
    for d in tempData_:
        x =  str(d)
        temp = x[1:len(x)-2]
        print(temp)
        ytemps.append(temp)
    curs.execute("SELECT timestamp FROM SenseHat_data")
    dates = curs.fetchall()
    for d in dates:
        x =  str(d)
        date = x[2:len(x)-3]
        xdates.append(date)
        print(date)
    print(xdates)
    x = [dt.datetime.strptime(y,'%m/%d/%Y %H:%M:%S').date() for y in xdates]

    plt.figure()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.grid()
    plt.plot(x,ytemps,marker='o')
    plt.gcf().autofmt_xdate()
    plt.ylabel('Temperature (C)')
    plt.xlabel('Date')
    plt.savefig('static/temp.png')
    conn.close()
    return render_template('temp.html', temp = "static/temp.png")

@app.route("/humid")
def plotHumid():
    plt.figure()
    plt.plot([18,28,1,4])
    plt.ylabel('goooy numbers')
    plt.savefig('static/humid.png')
    return render_template('humid.html', humid = "static/humid.png")
    

host = os.popen('hostname -I').read()
#port set to a non privileged port above 1024
app.run(host='192.168.1.12', port=5000, debug=False)