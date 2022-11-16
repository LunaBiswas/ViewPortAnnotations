import sys
import json
import timeit
from time import process_time
from pymongo import MongoClient

def filterJSON(mongoName,x1,x2,y1,y2,crange=[1]):
    '''
    Inputs: mongoName : it should contain the name of the MongoDB
            x1,x2     : the min and max range of x coordinate for the viewport
            y1,y2     : the min and max range of y coordinate for the viewport
            crange    : list containing the values of the class (the third value in JSON data [x,y,c] )
                        defaulted to [1], as only 1 is present in the test data for nucleus WSI
    '''
    file = mongoName.split('.')[0]
     
    client = MongoClient()
    db = client[file]
    collection = db[file]

    fullJSONdata = list(db.collection.find({'header.status': "success" }).limit(1))[0]['header']
    xrange1 = [x for x in range(x1,x2+1)]
    yrange1 = [x for x in range(y1,y2+1)]
    fullJSONdata["data"] = list(x['point'] for x in db.collection.find({"point.c": {'$in' : crange},"point.x": {'$in' : xrange1},"point.y": {'$in' : yrange1}}))
 
    return [fullJSONdata]

if __name__=='__main__':
    runno=1
    print('Running for ',runno,' times.')
    print('Average CPU time for 2D query on MongoDB on nucleus JSON:',timeit.timeit("filterJSON('nuc_location_new1',26000,26020,52000,52020)",number=runno,globals=globals())/runno)
