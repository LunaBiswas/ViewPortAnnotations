import sys
import json
import timeit
from time import process_time
from pymongo import MongoClient, GEO2D

def filterJSON(JSONname,x1,x2,y1,y2):
#    time_start1 = process_time()
    file = JSONname.split('.')[0]
 
    client = MongoClient()
    db = client[file]
    collection = db[file]

    try:
       fullJSONdata = list(db.collection.find({'header': { '$exists': True } } ))[0]['header']
       fullJSONdata["data"] = list(x['point'] for x in db.collection.find({"point":{"$geoWithin":{"$box":[[x1,y1],[x2,y2]]}}}))
    except:
       sys.exit('Please create MongoDB for '+JSONname+ ' by running createBSON.py')

    return [fullJSONdata]

if __name__=='__main__':
    runno=1
    print('Running for ',runno,' times.')
    
    print('Average CPU time for 2D query on MongoDB on tumor JSON:',timeit.timeit("filterJSON('tumor.json',15000,50000,100,400)",number=runno,globals=globals())/runno)
#    print('Average CPU time for 2D query on MongoDB on nuclear JSON:',timeit.timeit("filterJSON('nuc_location',26000,26020,52000,52020)",number=runno,globals=globals())/runno)