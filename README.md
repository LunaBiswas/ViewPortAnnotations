# ViewPortAnnotations
Filter in annotataions within a view port.


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
  
  4.1 Create python virtual environment:      python3 -m venv venv

  4.2 Activate the virtual environment:       source venv/bin/activate
  
  4.3 Install Flask by running:               source venv/bin/activate

  4.4
  


**Source**           : filterJSONWeb xBinary.py

**Inputs**           : JSON file name, (x,y) coordinates of the top left and bottom right corners of the viewport.

**Outputs**          : A list containing the total execution time in seconds, and the filtered JSON file.

**Technologies used**: Python, Flask, HTML.

**Logic**            : Reads the JSON file, finds first occurrence of minimum x coordinate and last occurrence of maximum x occurrence, then does binary                          search for y range within the x range found.

**Time complexity**  : O(log n + k) for n number of point annotations in the JSON file and k records found within the min and max x coordinates.

**Space complexity** : O(n) 

