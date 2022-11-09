import os
import sys
import json
from time import process_time
from pymongo import MongoClient
from flask import Flask, render_template, request

app = Flask(__name__)

@app.get("/")
def showForm():
    return render_template("WSIviewportForm.html")

@app.post("/")
def filterJSON():

    # retrieve input variable values 
    file = request.form.get('fname').split('.')[0]                            # Get MongoDB file name from POST request
    x1,y1 = list(map(int,list(map(request.form.get,['x1','y1']))))            # Get top left corner of the viewport from POST request
    xrange1 = [x for x in range(x1,x1+1500)]                                  # Viewport size is around 1500 pixels x 2000 pixels
    yrange1 = [x for x in range(y1,y1+2000)]
    crange = [request.form.get('class')]
    print('crange=',crange)                     

    # connect to MongoDB
    client = MongoClient()
    db = client[file]
    collection = db[file]

    fullJSONdata = list(db.collection.find({'header.status': "success" }).limit(1))[0]['header']
    fullJSONdata["data"] = list(x['point'] for x in db.collection.find({"point.c": {'$in' : crange},"point.x": {'$in' : xrange1},"point.y": {'$in' : yrange1}}))
    
    return [fullJSONdata]