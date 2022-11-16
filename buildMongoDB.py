import os
import sys
import json
from typing import Collection
from pymongo import MongoClient

def updateAnnotations(file, firstBool,insert_data=False):

    dbname = 'Nucleus'
    client = MongoClient()
    db = client[dbname]
    collection = db[dbname]
#    db.collection.drop()

    if insert_data == True:
        jsonFile = open(file,'r')
        fullJSONdata = json.load(jsonFile)
        pointAnnotations = fullJSONdata["data"]

        if firstBool == True:
            fullJSONdata.pop("data")
            header = db.collection.insert_one(
            {'header':fullJSONdata}
            )
            firstBool = False

        data = [{"point":{"c":p[2],"x":p[0],"y":p[1]}} for p in pointAnnotations]
        result=db.collection.insert_many(data)    

    return db, Collection, firstBool

def buildIndex(db, collection):
    
    db.collection.create_index(
        [("point.c", 1),
         ("point.x", 1),
         ("point.y", 1)
        ]
    )
    
    db.collection.create_index(
    [("header.status", 1)]
    )
    
    db.collection.create_index(
        "header", sparse=True
    )
    
    return 0

def createDB(dir):
    firstBool = True
    for filename in os.listdir('JSONdir/'+dir):
        db, collection, firstBool = updateAnnotations('JSONdir/'+dir+'/'+filename,firstBool,True)
        
    buildIndex(db, collection)
    return 0
 
if __name__ == '__main__':
    for arg in sys.argv[1:]: 
        createDB(arg)