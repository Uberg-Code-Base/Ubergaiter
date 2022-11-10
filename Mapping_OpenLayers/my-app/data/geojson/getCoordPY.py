path= '/Volumes/Seagate/Steven/OneDrive/SortaSorted/Elodae/*.png'

import os
import glob
import numpy as np
import arrayFiles

class coordinate: 
    def __init__(self, lon, lat): 
        self.lon = lon 
        self.lat = lat
   


pngfiles = []
coordsObj = []
coordsArr = []
coordsArrFull = []
for filePath in glob.glob(path):
    fileName = os.path.basename(filePath) 

# arrayOfFiles = arrayFiles.getFiles()

# for file in arrayOfFiles:
    # if len(fileName) > 110:
       # print(fileName)
    # fileName = file[1]
    # fileID = file[0]
    try:
        Node='_M'
        index=fileName.index(Node)# fetching index of node
        file2 = fileName[index+2::]
        file3 = file2.split('_')
        lon = file3[0]
        print ("lon "+ lon)
        #latitude
        Node='_N'
        index=fileName.index(Node)# fetching index of node
        file2 = fileName[index+2::]
        file3 = file2.split('_')
        lat = file3[0]

        #timestamp
        Node='_T'
        index=fileName.index(Node)# fetching index of node
        file2 = fileName[index+2::]
        file3 = file2.split('.')
        timestampGPS = file3[0]

        #Lake
        listName = fileName.split("_")
        lakeName = listName[0]
        
        #DateTime + Timestamp from Raspberry Pi
        dateTime = listName[2]
        timestampPi = listName[3]

        #placeholder for list of detected plants
        plants = []

        coords = []
        coordsFull = []
        coords.append(float(lat))
        coords.append(float(lon))
        
        coordsFull.append(str(lakeName))
        coordsFull.append(float(lat))
        coordsFull.append(float(lon))
        coordsFull.append(str(dateTime))
        coordsFull.append(str(timestampPi))
        coordsFull.append(timestampGPS)
        coordsFull.append(fileName)
        coordsFull.append(plants)
        #coordsFull.append(fileID)

        coordsArr.append(coords)

        coordsArrFull.append(coordsFull)
        coordsObj.append( coordinate(lon, lat) )
    except:
        a = 0

# for i in range(len(coordsObj)):
#     print (coordsObj[i].lon + ' ' + coordsObj[i].lat)
coordinatesWithoutDuplicates = []
for i in coordsArr:
    if i not in coordinatesWithoutDuplicates:
        coordinatesWithoutDuplicates.append(i)

# print((coordinatesWithoutDuplicates))
# for i in range (len(coordsArr)):
#     print(coordsArr[i])

# data_dict = {
#     'lake': 'sum(num_users) AS actives',
#     'table': '1_day_actives',
#     'where_clause': 'country = "US"',
#     'order_by_clause': 'actives',
#     'group_by_clause': 'actives'
# }

file = open("coords.txt", "a")


# Saving the array in a text file
content = str(coordinatesWithoutDuplicates)
file.write(content)
file.close()

file = open("coordsFull.txt", "a")


# Saving the array in a text file
content = str(coordsArrFull)
file.write(content)
file.close()

file = open("coordsFullNoList.txt", "a")
def is_file_empty_4(fileX):
    with open("coordsFullNoList.txt", 'r') as read_obj:
        # read first character
        one_char = read_obj.read(1)
        # if not fetched then file is empty
        if not one_char:
           return True
    return False
if not is_file_empty_4(file):
    file.write(',')


# Saving the array in a text file
for i in range(len(coordsArrFull)):
    content = coordsArrFull[i]
    file.write(str(content))
    file.write(',\n')

# content = coordsArrFull[len(coordsArrFull)-1]
# file.write(str(content))
# file.write('\n')

file.close()

file = open("coordsNoList.txt", "a")

def is_file_empty_3(fileX):
    with open("coordsNoList.txt", 'r') as read_obj:
        # read first character
        one_char = read_obj.read(1)
        # if not fetched then file is empty
        if not one_char:
           return True
    return False

if not is_file_empty_3(file):
    file.write(',')
# Saving the array in a text file
for i in range(len(coordinatesWithoutDuplicates)-1):
    content = coordinatesWithoutDuplicates[i]
    file.write(str(content))
    file.write(',\n')

# content = coordinatesWithoutDuplicates[len(coordinatesWithoutDuplicates)-1]
# file.write(str(content))
# file.write('\n')

file.close()

out_file = open("path.geojson", "w")
#out_file2 = open("test2.json", "w")
first = """{
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
                                                                                    
    "features": 
        [
            { "type": "Feature", "properties": { "name": "Stukely" }, "geometry": 
                { 
                    "type": "LineString", "coordinates": \n"""


out_file.write(first)
#out_file.write(str(coordinatesWithoutDuplicates))
###########
coordsUptoDate = open("coordsNoList.txt", "r")
# print(str(coordsUptoDate))
count = 0
out_file.write('\t\t\t\t\t\t[\n')
for line in coordsUptoDate:
    if line.strip():
        print(line)
        out_file.write("\t\t\t\t\t\t\t" + line)
        count += 1

out_file.write('\t\t\t\t\t\t]')
#out_file.write -> make it take the appended txt file instead.. another night

#########
out_file.write('\n\t\t\t\t}\n\t\t\t}\n\t\t]\n}')
out_file.close()