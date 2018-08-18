import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

host = os.popen('hostname -I').read()
app.run(host=host, port=80, debug=False)