import sys
import json
import timeit
import random
from time import process_time
from pymongo import MongoClient

import ast
import create_zarr
import fetch_zarr
import create_rtree
import fetch_rtree
import fetch_heatmap
import config

def filterJSONRTree(x,y):

    st = process_time()
    ALL_NUCLEI_PTS = fetch_zarr.read_zarr(config.zarr_dir)

    req = {
    "base_tiles":"2001V401001_55",
    "zoom":40,
    "annotation_data":[
        {
            "top":y,
            "left":x,
            "width":1500,
            "height":2000,
            "id":"mask_id_1"
        }
    ]
    }

    res,qt = fetch_rtree.filter_rtree(req, ALL_NUCLEI_PTS, config.rtree_idx_path)
    et = process_time()

    return [res,len(res["annotation_data_list"])*16,qt,et-st]

def filterJSONHeatmap(x,y):

    st = process_time()
    req = {
    "base_tiles":"2001V401001_55",
    "zoom":40,
    "annotation_data":[
        {
            "top":y,
            "left":x,
            "width":1500,
            "height":2000,
            "id":"mask_id_1"
        }
    ],
    "grid_row": 100,
    "grid_col": 100
    }
    
    res,t = fetch_heatmap.get_heatmap(req, config.rtree_idx_path)
    et = process_time()

    return [res,len(res["annotation_data_list"])*16,t,et-st]

def filterJSONzArray(x,y):

    st = process_time()
    ALL_NUCLEI_PTS = fetch_zarr.read_zarr(config.zarr_dir)

    req = {
    "base_tiles":"2001V401001_55",
    "zoom":40,
    "annotation_data":[
        {
            "top":y,
            "left":x,
            "width":1500,
            "height":2000,
            "id":"mask_id_1"
        }
    ],
    "grid_row": 100,
    "grid_col": 100
    }
    
    res,t = fetch_zarr.filter_zarr(req, ALL_NUCLEI_PTS)
    et = process_time()

    return [res,len(res["annotation_data_list"])*16,t,et-st]

def filterJSONMongoDB(dbname,x1,x2,y1,y2):
    stt = process_time()

    file = dbname.split('.')[0]
 
    client = MongoClient()
    db = client[file]
    collection = db[file]

    try:
        fullJSONdata = list(db.collection.find({'header.status': "success" } ).limit(1))[0]['header']
        xrange1 = [x for x in range(x1,x2+1)]
        yrange1 = [y for y in range(y1,y2+1)]
        st = process_time()
        fullJSONdata["data"] = list(x['point'] for x in db.collection.find({"point.c":{"$in":[1]},"point.x": {"$in" : xrange1},"point.y": {"$in":yrange1} }))
        et = process_time()
        print(f"MongoDB: query time: {int(((et-st)* 10**3))} ms")
    except:
        sys.exit('Please create MongoDB '+dbname+ ' by running buildMongoDB.py')
    ett = process_time()

    return [fullJSONdata,len(fullJSONdata["data"]),et-st,ett-stt]

if __name__=='__main__':
    
    repeatNo=10
    
    print("Running ", repeatNo," times.")

    time_average = 0
    time_average1 = 0
    time_average2 = 0
    time_average3 = 0

    query_average = 0
    query_average1 = 0
    query_average2 = 0
    query_average3 = 0

    for i in range(repeatNo):
  #      x,y=83508,53480

        
        x = random.randint(100,90000)
        y = random.randint(100,121000)
        
        _,n,q,t = filterJSONMongoDB('nuc_location_new1',x,x+1500,y,y+2000)
 #       t=timeit.timeit("filterJSONMongoDB('nuc_location_new1',x,x+1500,y,y+2000)",number=1,globals=globals())
        print(n, 'Annotations fetched from range:[(',x,',',y,')(',x+1500,',',y+2000,')] from MongoDB in time ',t)
        print("\n")
        time_average += t
        query_average += q

        _,n,q,t = filterJSONRTree(x,y)
  #      t=timeit.timeit("filterJSONRTree(x,y)",number=1,globals=globals())
        print(n, 'Annotations fetched from range:[(',x,',',y,')(',x+1500,',',y+2000,')] from RTree in time ',t)
        print("\n")
        time_average1 += t
        query_average1 += q
    
        _,n,q,t = filterJSONHeatmap(x,y)
  #      t=timeit.timeit("filterJSONHeatmap(x,y)",number=1,globals=globals())
        print(n, 'Annotations fetched from range:[(',x,',',y,')(',x+1500,',',y+2000,')] from RTree using hitmap in time ',t)
        print("\n")
        time_average2 += t
        query_average2 += q

        _,n,q,t = filterJSONzArray(x,y)
 #       t=timeit.timeit("filterJSONzArray(x,y)",number=1,globals=globals())
        print(n, 'Annotations fetched from range:[(',x,',',y,')(',x+1500,',',y+2000,')] from z array in time ',t)
        print("\n")
        time_average3 += t
        query_average3 += q

    time_average /= repeatNo
    time_average1 /= repeatNo
    time_average2 /= repeatNo
    time_average3 /= repeatNo

    query_average /= repeatNo
    query_average1 /= repeatNo
    query_average2 /= repeatNo
    query_average3 /= repeatNo
    
    print('Average CPU time for 2D query on MongoDB on nucleus JSON:',time_average, " query time: ",query_average)
    print('Average CPU time for 2D query on RTree on nucleus JSON:',time_average1, " query time: ",query_average1)
    print('Average CPU time for 2D query using hitmap on RTree on nucleus JSON:',time_average2, " query time: ",query_average2)
    print('Average CPU time for 2D query on z array on nucleus JSON:',time_average3, " query time: ",query_average3)