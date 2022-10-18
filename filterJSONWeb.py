import json
from flask import Flask, render_template, request
from time import process_time

app = Flask(__name__)

@app.get("/")
def showForm():
    return render_template("form.html")

#/JSONname>/<x1>/<y1>/<x2>/<y2>
@app.post("/")
#def filterJSON(JSONname,x1,y1,x2,y2):
def filterJSON():
    t1_start = process_time()
    JSONname = request.form.get('fname')
    x1 = int(request.form.get('x1'))
    x2 = int(request.form.get('x2'))
    y1 = int(request.form.get('y1'))
    y2 = int(request.form.get('y2'))
#    x1, y1, x2, y2 = list(map(int,[postData[x1],postData[y1],postData[x2],postData[y2]]))
    jsonFile = open('JSONdir/'+JSONname,'r')
    fullJSONdata = json.load(jsonFile)
    inPointAnnotations = fullJSONdata["data"]
    '''
    outPointAnnotations = [] 
    for point in inPointAnnotations:
        if point[0] >= x1 and point[0] <= x2 and point[1] >= y1 and point[1] <= y2:
            outPointAnnotations.append(point)
    '''
    #outPointAnnotations = list(filter(lambda point: point[0] >= x1 and point[0] <= x2 and point[1] >= y1 and point[1] <= y2,inPointAnnotations))
    outPointAnnotations = [point for point in inPointAnnotations if point[0] >= x1 and point[0] <= x2 and point[1] >= y1 and point[1] <= y2]
    fullJSONdata["data"] = outPointAnnotations

    outFileName = JSONname[:-5] + '_' + str(x1) + '_' + str(y1) + '_' + str(x2) + '_' + str(y2) + '.json'
    with open('JSONdir/'+outFileName, 'w') as file:
        file.write(json.dumps(fullJSONdata))
    t1_stop = process_time()
    return "Elapsed time during the whole program in seconds:"+ str(t1_stop-t1_start)+'\n'
  