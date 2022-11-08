import json
import timeit
import pickle
from rangeTree2D import constructRangeTree, searchRangeTree2D

def filterJSON(JSONname,x1,x2,y1,y2):
    jsonFile = open('JSONdir/'+JSONname,'r')
    fullJSONdata = json.load(jsonFile)
    inPointAnnotations = fullJSONdata["data"]
    try:
        rangeTree = pickle.load(open('ListDir/'+JSONname[:-4]+'pkl', 'rb'))
    except:
        jsonFile = open('JSONdir/'+JSONname,'r')
        fullJSONdata = json.load(jsonFile)
        inPointAnnotations = fullJSONdata["data"]
        rangeTree = constructRangeTree(inPointAnnotations)
        pickle.dump(rangeTree,open('ListDir/'+JSONname[:-4]+'pkl','wb'))
 
    fullJSONdata["data"] = searchRangeTree2D([x1,y1],[x2,y2],rangeTree)
 
    return [fullJSONdata]

if __name__=='__main__':
    
 #   print(filterJSON('tumor.json',20,1500,20,1500))
 #   print('=================================')
 #   print(filterJSON('nuclear.json',20,1500,20,1500))
    
    print('Average CPU time for 2D range tree search on tumor JSON:',timeit.timeit("filterJSON('tumor.json',20,1500,20,1500)",number=100000,globals=globals()))
    print('Average CPU time for 2D range tree search on nuclear JSON:',timeit.timeit("filterJSON('nuclear.json',20,1500,20,1500)",number=100000,globals=globals()))
    