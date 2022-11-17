import sys
import json
import random
import timeit
from time import process_time
from pymongo import MongoClient

def updateAnnotation(mongoName,updates):
    '''
    Inputs: mongoName : it should contain the name of the MongoDB
            updates   : details of updates required
                        format: 
                            [[action,point_list],[action,point_list]]
                            where action    : 'insert' 
                                  point_list: [[c,x,y],[c,x,y],...,[c,x,y]]: list of points to be inserted
                                           
                                  action    : 'delete'
                                  point_list: [object_id1,....,object_idn]
    '''
    st = process_time()
    file = mongoName.split('.')[0]
     
    client = MongoClient()
    db = client[file]
    collection = db[file]
    q = 0
    for update in updates:
        if update[0] == 'insert':
            data = [{"point":{"c":p[0],"x":p[1],"y":p[2],"annot_num":p[3]}} for p in update[1]]
            qst = process_time()
            result=db.collection.insert_many(data)   
            est = process_time()
            q += est - qst
            et = process_time()

            return et-st, q,result.inserted_ids
        elif update[0] == 'delete':
            '''
            # Deleting within range: Not possible to mass delete with multiple types of annotations
            # because same point might belong to different annotations 
            crange = [p[0] for p in update[1]]
            xrange1 = [p[1] for p in update[1]]
            yrange1 = [p[2] for p in update[1]]
            annot_range = [p[3] for p in update[1]]
            query = {"point.c":{"$in":crange},"point.x": {"$in" : xrange1},"point.y": {"$in":yrange1},"point.annot_num":{"$in":annot_range} }
            qt = process_time()
            result=db.collection.delete_many(query)  

            eqt = process_time()  
            q += eqt-qt
            '''    
            '''
            # Obtaining object ids using x,y coordinates and class etc, and then deleting in mass 
            # using object ids. 
            # Select query takes time, though delete query is fast  
            obj_id_list = []        
            for p in update[1]:
                query = {"point.c":{"$in":[p[0]]},"point.x": {"$in" : [p[1]]},"point.y": {"$in":[p[2]]},"point.annot_num":{"$in":[p[3]]} }
                qt = process_time()
                result=list(x['_id'] for x in db.collection.find(query))  
                eqt = process_time() 
                q += eqt-qt
                obj_id_list.extend(result)  
            query = {"_id":{"$in":obj_id_list}}
            qt = process_time()
            result=db.collection.delete_many(query)  
            eqt = process_time()  
            print('time for finds: ',q)
            print('time for mass delete: ',eqt-qt)
            q += eqt-qt
            '''
            # Deleting with object ids, received from viewer query
            qst = process_time()
            query = {"_id":{"$in":update[1]}}
            result=db.collection.delete_many(query)   
            est = process_time()
            q += est - qst
            et = process_time()

            return et-st, q, result.deleted_count
        else:
            return -1
    

if __name__=='__main__':
    runno=100
    print('Running ', runno, 'times.')
    point_volume = 16**4
#    print('Running for ',runno,' times.')
#    print('Average CPU time for 2D query on MongoDB on nucleus JSON:',timeit.timeit("updateAnnotation('nuc_location_2',['d',[1,233,400]])",number=runno,globals=globals())/runno)
    iqtime = 0
    ittime = 0
    dqtime = 0
    dttime = 0
    
    for i in range(runno):
        data = []
        for j in range (point_volume):
            x = random.randint(100,90000)
            y = random.randint(100,121000)
            c = 1
            data.append([c,x,y,i])
        t,q,inserted_data = updateAnnotation('nuc_location_2',[['insert',data]])
        iqtime += q
        ittime += t

        
        t,q,deleted_count = updateAnnotation('nuc_location_2',[['delete',inserted_data]])
        dqtime += q
        dttime += t
        

    iqtime /= runno
    ittime /= runno
    dqtime /= runno
    dttime /= runno

    print('For ', point_volume, 'points, average insert time: ', ittime, ' query time: ',iqtime)
    print('For ', deleted_count, 'points, average delete time: ', dttime, ' query time: ',dqtime)