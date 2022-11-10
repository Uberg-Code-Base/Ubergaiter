path= '/Volumes/Seagate/Steven/OneDrive/AcquisitionFolder/*.png'
copyPath = '/Volumes/Seagate/Steven/OneDrive/RemainingToID/'
import os
import glob

   


fileNames = []
for filePath in glob.glob(path):
    fileName = os.path.basename(filePath) 
    fileNames.append(fileName)


file = open("fileNames.txt", "a")


# Saving the array in a text file
content = str(fileNames)
file.write(content)
file.close()
