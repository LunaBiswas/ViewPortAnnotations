import os
import sys
import json
from time import process_time
from pymongo import MongoClient, GEO2D

def updateMongoDB(filename):
    print(filename)
    jsonFile = open(filename,'r')
    fullJSONdata = json.load(jsonFile)
    pointAnnotations = fullJSONdata["data"]
    fullJSONdata.pop("data")
    file = fullJSONdata["label_name"][0]["name"]
#    print(file)
 
#    file=filename
    client = MongoClient()
    db = client[file]
    collection = db[file]
 #   db.collection.drop()

    db.collection.create_index(
    [("point", GEO2D)],
    min=0,max=sys.maxsize
    )

    result=db.collection.insert_one(
    {'header':fullJSONdata}
    )

    data = [{"point":p} for p in pointAnnotations]
    result=db.collection.insert_many(data)    

    return 0


def createBSONfromJSON(JSONname):
    inputs = JSONname.split('.')
    if len(inputs) == 1: # input is a directory name
        for filename in os.listdir('JSONdir/'+JSONname):
            updateMongoDB('JSONdir/'+JSONname+'/'+filename)
    else:                # input is a file name
        updateMongoDB('JSONdir/'+JSONname)
#        updateMongoDB(inputs[0])
    return 0

if __name__ == '__main__':
    for arg in sys.argv[1:]: 
        createBSONfromJSON(arg)