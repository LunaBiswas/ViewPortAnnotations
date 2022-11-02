import json
from flask import Flask, render_template, request
from time import process_time

app = Flask(__name__)

@app.get("/")
def showForm():
    return render_template("form.html")

@app.post("/")
def filterJSON():
    # Receive search values from the client form POST request
    JSONname = request.form.get('fname')
    x1 = int(request.form.get('x1'))
    x2 = int(request.form.get('x2'))
    y1 = int(request.form.get('y1'))
    y2 = int(request.form.get('y2'))

    # Load json data from json directory
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
    # Filter annotation data to be in range [(x1,y1),(x2,y2)]
    fullJSONdata["data"] = [point for point in inPointAnnotations if point[0] >= x1 and point[0] <= x2 and point[1] >= y1 and point[1] <= y2]

  #  outFileName = JSONname[:-5] + '_' + str(x1) + '_' + str(y1) + '_' + str(x2) + '_' + str(y2) + '.json'
  #  with open('JSONdir/'+outFileName, 'w') as file:
  #      file.write(json.dumps(fullJSONdata))
    return [fullJSONdata]
  