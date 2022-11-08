import json
import timeit

inPointAnnotations = []

def binarySearchOnXMin(x):
    global inPointAnnotations
    low = 0
    high = len(inPointAnnotations) -1
    
    while low < high:
        mid = (low + high)//2
        if mid == low or mid == high:
            break
        if inPointAnnotations[mid][0] < x:    # Element is on right half
            low = mid
        else:                                  # Element is on left half
            high = mid

    return low
    

def binarySearchOnXMax(x):
    global inPointAnnotations
    low = 0
    high = len(inPointAnnotations) -1
    
    while low < high:
        mid = (low + high)//2
        if mid == low or mid == high:
            break
        if inPointAnnotations[mid][0] <= x:    # Element is on right half
            low = mid
        else:                                  # Element is on left half
            high = mid

    return high

def filterJSON(JSONname,x1,x2,y1,y2):
    global inPointAnnotations

    jsonFile = open('JSONdir/'+JSONname,'r')
    fullJSONdata = json.load(jsonFile)
    inPointAnnotations = fullJSONdata["data"]

    xid1=binarySearchOnXMin(x1)
    xid2=binarySearchOnXMax(x2) 
    print('# of total records:',len(fullJSONdata["data"]))
    
    fullJSONdata["data"] = [point for point in inPointAnnotations[xid1:xid2] if point[1] >= y1 and point[1] <= y2]
    print('# of records fetched:',len(fullJSONdata["data"]))
    
    return [fullJSONdata]
  
if __name__=='__main__':
    
    filterJSON('tumor.json',20,1500,20,1500)
    print('=================================')
    filterJSON('nuclear.json',20,1500,20,1500)
        
 #   print('Average CPU time for binary search on x coordinate and linear search on y coordinates of tumor JSON:',timeit.timeit("filterJSON('tumor.json',20,1500,20,1500)",number=100000,globals=globals()))
 #   print('Average CPU time for binary search on x coordinate and linear search on y coordinates of nuclear JSON:',timeit.timeit("filterJSON('nuclear.json',20,1500,20,1500)",number=100000,globals=globals()))