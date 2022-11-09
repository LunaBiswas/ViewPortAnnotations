# ViewPortAnnotations
Filter in annotataions within a view port.


** Query from MongoDB using selective query on compound index **

**Process**          :

1. Keep JSON file in directory ./JSONdir, if it is a single JSON file. If there are multiple files pertaining to the same WSI, keep the JSON directory inside ./JSONdir

2. Load JSON data to Mongo DB and create indices, by running following command in terminal

              python3 buildMongoDB.py <name of file or directory>
  
3. Modify x and y ranges and name of MongoDB in line 32 of filterJSONMongoDB1.py
    
4. Query from MongoDB by running following command in terminal
  
              python3 filterJSONMongoDB1.py

5. To query from MongoDB from a client using REST API,
  
  5.1 Create python virtual environment:      python3 -m venv venv

  5.2 Activate the virtual environment:       source venv/bin/activate
  
  5.3 Install Flask by running:               pip install Flask

  5.4 Start the server:                       Start the server: export FLASK_APP=filterJSONWeb.py; flask run     
      Access API from http://127.0.0.1:5000. 
    
  


**Source**           : filterJSONWebMongoDBGeo2D.py, filterJSONMongoDB.py

**Inputs**           : MongoDB name, (x,y) coordinates of the top left and bottom right corners of the viewport.

**Outputs**          : The filtered JSON file.

**Technologies used**: Python, Flask, HTML.

**Index**            : A GEO2D index is created in MongoDB for x and y coordinates as points.

**Query**            : $geoWithin , $box query

------------------------------------------------------------------------------------------------------------------------------
**Source**           : filterJSONWeb Linear.py

**Inputs**           : JSON file name, (x,y) coordinates of the top left and bottom right corners of the viewport.

**Outputs**          : A list containing the total execution time in seconds, and the filtered JSON file.

**Technologies used**: Python, Flask, HTML.

**Logic**            : Reads the JSON file, does linear search on the data and writes records within the x and y range, to output.

**Time complexity**  : O(n) for n number of point annotations in the JSON file

**Space complexity** : O(n) 

-------------------------------------------------------------------------------------------------------------------------------

**Source**           : filterJSONWeb xBinary.py

**Inputs**           : JSON file name, (x,y) coordinates of the top left and bottom right corners of the viewport.

**Outputs**          : A list containing the total execution time in seconds, and the filtered JSON file.

**Technologies used**: Python, Flask, HTML.

**Logic**            : Reads the JSON file, finds first occurrence of minimum x coordinate and last occurrence of maximum x occurrence, then does binary                          search for y range within the x range found.

**Time complexity**  : O(log n + k) for n number of point annotations in the JSON file and k records found within the min and max x coordinates.

**Space complexity** : O(n) 

-------------------------------------------------------------------------------------------------------------------------------

**Source**           : filterJSONRangeTree.py, rangeTree2D.py

**Inputs**           : JSON file name, (x,y) coordinates of the top left and bottom right corners of the viewport.

**Outputs**          : JSON file with annotations filtered in within the (x,y) coordinates.

**Technologies used**: Python.

**Logic**            : Reads the JSON file, creates a 2D range tree using Python list and stores the list in pickle format. In case a range tree for the JSON is already there, finds records with (x,y) range from the range tree.

**Time complexity**  : 

                       Construction: O(n (log n)^2)

                       Query: O(log n*log m + k) for n number of point annotations in the JSON file, m number of y nodes in the x interval and k records found within the interval.

**Space complexity** : O(n log n) 

-------------------------------------------------------------------------------------------------------------------------------

** Query from MongoDB using Geo2D index **

**Process**          :

1. Keep JSON file in directory ./JSONdir, if it is a single JSON file. If there are multiple files pertaining to the same WSI, keep the JSON directory inside ./JSONdir

2. Load JSON data to Mongo DB and create GEO2D index, by running following command in terminal

              python3 createBSON.py <name of file or directory>
  
3. Modify x and y ranges and name of MongoDB in line 28 of filterJSONMongoDB.py
    
4. Query from MongoDB by running following command in terminal
  
              python3 filterJSONMongoDB.py

5. To query from MongoDB from a client,
  
  5.1 Keep viewportForm.html in direcrory ./templates
  
  5.2 Create python virtual environment:      python3 -m venv venv

  5.3 Activate the virtual environment:       source venv/bin/activate
  
  5.4 Install Flask by running:               pip install Flask

  5.5 Start the server:                       Start the server: export FLASK_APP=filterJSONWebMongoDBGeo2D.py; flask run     
      Access API from http://127.0.0.1:5000. 
      Enter name of MongoDB in the file name field.
  


**Source**           : filterJSONWebMongoDBGeo2D.py, filterJSONMongoDB.py

**Inputs**           : MongoDB name, (x,y) coordinates of the top left and bottom right corners of the viewport.

**Outputs**          : The filtered JSON file.

**Technologies used**: Python, Flask, HTML.

**Index**            : A GEO2D index is created in MongoDB for x and y coordinates as points.

**Query**            : $geoWithin , $box query
