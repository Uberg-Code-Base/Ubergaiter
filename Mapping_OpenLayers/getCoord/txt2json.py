import json
  
  
# the file to be converted to 
# json format
filename = 'coords.txt'
  
# dictionary where the lines from
# text will be stored
dict1 = {}
  
# creating dictionary
with open(filename) as fh:
  
    for line in fh:
  
        # reads each line and trims of extra the spaces 
        # and gives only the valid words
        command, description = line.strip().split(None, 1)
  
        dict1[command] = description.strip()
  
# creating json file
# the JSON file is named as test1
out_file = open("test1.geojson", "w")
#out_file2 = open("test2.json", "w")
first = """
    {
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
                                                                                    
    "features": [
    { "type": "Feature", "properties": { "name": "Stukely" }, "geometry": { "type": "LineString", "coordinates": """

out_file.write(first)
##json
#json.dump(dict1, out_file2, indent = 4, sort_keys = False)
#out_file2.close()
myfile = open("test2.json", "r")
mylist = myfile.readlines()
mytext = ""
for items in mylist:
    mytext = mytext + items +"\n"
myfile.close()
mytext = mytext[1:]
myfile = open("test3.json", "w")
myfile.write(mytext)
myfile.close()

out_file.write(mytext)
out_file.write('}}]}')
out_file.close()