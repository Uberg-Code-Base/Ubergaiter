import os
import shutil

dest_dir = '/Volumes/Seagate/Steven/OneDrive/SortaSorted_LocsLess/'

folder_dir = '/Volumes/Seagate/Steven/OneDrive/SortaSorted_TrainSet2_Full/'

valid_dir = '/Volumes/Seagate/Steven/OneDrive/SortaSorted_LocsLess_ValidationSet'


def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1 #change to k += len(sub) to not search overlapping results
    return result

count = 0

for folder in os.listdir(folder_dir):
    folder = folder + '/'
    path = os.path.join(folder_dir, folder)
    destPath = os.path.join(dest_dir, folder )
    validPath = os.path.join(valid_dir, folder )
# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
    # os.mkdir(validPath)
    # print("Directory '% s' created" % destPath)
    for file in os.listdir(os.path.join(folder_dir, folder)):
        if file.endswith("png"):
            orig_pathFile = os.path.join(folder_dir, folder, file)
            #print(orig_pathFile)
            dest_path_File = os.path.join(dest_dir, folder, file)
            valid_path_File = os.path.join(valid_dir, folder, file)
            bromptonFind = find_all(str(file), '-72')
            otherFind = find_all(str(file), '_N')
            count = count + 1
            # print(str(bromptonFind) + ' - ' + str(otherFind))
            if (len(bromptonFind) > 0 or len(otherFind) > 0):
                shutil.copyfile(orig_pathFile, valid_path_File)
                print(count)
            else: 
                shutil.copyfile(orig_pathFile, dest_path_File)
                print(count)


