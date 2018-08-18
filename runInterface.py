#!/usr/bin/env python3
import os
from flask import Flask, request, render_template, send_file
import matplotlib
# dont use windows backend by default
matplotlib.use('Agg')
from matplotlib import pyplot as plt 
import base64, io

app = Flask(__name__, template_folder='templates')

@app.route("/")
def plotGraph():

    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.savefig('static/graph.png')
    return render_template('index.html', url = 'static/graph.png')

host = os.popen('hostname -I').read()
#port set to a non privileged port above 1024
app.run(host='192.168.1.4', port=5000, debug=False)