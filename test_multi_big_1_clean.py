from datetime import datetime
# Clear any logs from previous runs
import os
import cv2
import numpy as np
import tensorflow as tf
import keras
#Encoding and Split data into Train/Test Sets
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

#Tensorflow Keras CNN Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Activation, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop

#Plot Images
import matplotlib.pyplot as plt

folder_dir = '/Volumes/Seagate/Steven/OneDrive/SortaSorted_Trainset2_Validation2_1'
######################
modelName ='/Users/pierre/Ubergaiter/Recog/Plant1_v2_large/saved_model_/trainset2Full_multi_2_20221204-004824'
model = keras.models.load_model(modelName)

Myriophyllum = [[], [], [], []]
Nothing = [[], [], [], []]
P_Ampliforus = [[], [], [], []]
P_Zosteriformis = [[], [], [], []]
P_Richardsonii = [[], [], [], []]
P_Robbinsii = [[], [], [], []]
Sand = [[], [], [], []]



myl_1_0 = 'Myriophyllum'
rob_2_1 =  'P_Robbinsii'
elo_3_2 =  'Elodae' 
rich_4_3 =  'P_Richardsonii'
crisp_5_4 =  '5' 
amp_6_5 = 'P_Ampliforus'
grami_7_6 =  '7'      ##### sort grami-zost prob   i think all grami are zost
utri_8_7 = '8' 
sparg_9_8=  '9' 
cera_a_9 = 'a' 
erio_b_10 = 'b' 
valli_c_11 =  'c' 
het_d_12 = 'd' 
cal_e_13 = 'e' 
nuph_h_14 = 'h' 
stuck_l_15 =  'l' 
chara_j_16 =  'j' 
sagi_k_17 = 'k' 
prael_m_18 =  'm' 
zost_n_19 = 'P_Zosteriformis'
niet_i_20 = 'Nothing'
blur_o_21 = 'f' 
other_g_22 =  'g' 
sand_p_23 = 'Sand'

legend = [myl_1_0,rob_2_1, elo_3_2, rich_4_3, crisp_5_4, amp_6_5,grami_7_6,utri_8_7,sparg_9_8,cera_a_9,erio_b_10,valli_c_11, het_d_12,cal_e_13,nuph_h_14,stuck_l_15, chara_j_16,sagi_k_17,prael_m_18, zost_n_19,niet_i_20,blur_o_21,other_g_22,sand_p_23] 
data = []
label = []
fileNames = []
goodAnswers = []
SIZE = 256 #Crop the image to 128x128

for folder in os.listdir(folder_dir):
    print(folder)
    for file in os.listdir(os.path.join(folder_dir, folder)):
        if file.endswith("png") and str(file[0]) != '.':
            print(file)
            fileNames.append(file)
            img = cv2.imread(os.path.join(folder_dir, folder, file))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = cv2.resize(img_rgb, (SIZE,SIZE))
            data.append(im)
            goodAnswers.append(folder)
        else:
            continue

############
data_arr = np.array(data)

############

X = data_arr/255

myVars = locals()
for i in range(len(X)):  
    classes = np.array(legend)
    proba = model.predict(X)[i]
    top_1 = np.argsort((proba))[:-4:-1]
    print(top_1)
    predicted = classes[top_1[0]]
    print(predicted)
    categ = goodAnswers[i]
    print(categ)
    if(categ == predicted):
        print("yes")
        print('real: ' + categ)
        print('predicted: ' + predicted)
        myVars[categ][0].append(1)
        myVars[categ][1].append(fileNames[i])
        myVars[categ][2].append('_')
        myVars[categ][3].append(predicted + ', ' + categ)
        print(str(i) + ' of ' + str(len(X)) + 'pics')


        
    else:
        print("no")
        print('real: ' + categ)
        print('predicted: ' + predicted)
        myVars[categ][0].append(0)
        myVars[categ][1].append('_')
        myVars[categ][2].append(fileNames[i])
        myVars[categ][3].append(predicted + ', ' + categ)
        print(str(i) + ' of ' + str(len(X)) + 'pics')

# # ################## categories percentages 
Myriophyllum_Confidence = 100 * (Myriophyllum[0].count(1) / len(Myriophyllum[0]))
Nothing_Confidence = 100 * (Nothing[0].count(1) / len(Nothing[0]))
P_Ampliforus_Confidence = 100 * (P_Ampliforus[0].count(1) / len(P_Ampliforus[0]))
P_Zosteriformis_Confidence = 100 * (P_Zosteriformis[0].count(1) / len(P_Zosteriformis[0]))
P_Richardsonii_Confidence = 100 * (P_Richardsonii[0].count(1) / len(P_Richardsonii[0]))
P_Robbinsii_Confidence = 100 * (P_Robbinsii[0].count(1) / len(P_Robbinsii[0]))
Sand_Confidence = 100 * (Sand[0].count(1) / len(Sand[0]))

print('savingToFile...')
dateTimeNow = datetime.now().strftime("%Y%m%d-%H%M%S")
fileNowName = 'conf_multi_big_1_' + dateTimeNow + '.txt'
f = open(fileNowName, "a")
dims = model.input_shape[1:3] # -> (height, width)
f.write('###########################\n')
f.write('Confidence Level File - Ubergaiter Acquisitions Files TrainSet1\n\n')
f.write('__________Setup____________\n')
f.write('Model name: '+ modelName +'\n\n')
f.write('Model shape: ' + str(model.input_shape)+'\n')
f.write('Dims: '+ str(dims)+'\n')
f.write('Tensorflow version ' + str(tf.__version__)+'\n')
f.write('Keras version ' + str(keras.__version__)+'\n')

dateTimeObj = datetime.now()
f.write('Tested on ' + str(dateTimeObj))
f.write('\n')
f.write('___________________________\n\n')

f.write('List of confidence levels from a one-quarter size validation set\n\n')
f.write('\n')
f.write('Myriophyllum Confidence Level: ' + str(Myriophyllum_Confidence) + '%___________\n')
f.write('\n')
f.write('Nothing(emptiness) Confidence Level: ' + str(Nothing_Confidence) + '%___________\n')
f.write('\n')
f.write('Potamogeton Ampliforus Confidence Level: ' + str(P_Ampliforus_Confidence) + '%___________\n')
f.write('\n')
f.write('Potamogeton Richardsonii Confidence Level: ' + str(P_Richardsonii_Confidence) + '%___________\n')
f.write('\n')
f.write('Potamogeton Robbinsii Confidence Level: ' + str(P_Robbinsii_Confidence) + '%___________\n')
f.write('\n')
f.write('Potamogeton Zosteriformis Confidence Level: ' + str(P_Zosteriformis_Confidence) + '%___________\n')
f.write('\n')
f.write('Sand Confidence Level: ' + str(Sand_Confidence) + '%___________\n')
f.write('\n')

f.write('\n')
f.write('\n')
f.write('___________________________\n\n')
f.write('\n')
f.write('List of non-recognized pictures\n\n')
f.write('\n')
f.write('Myriophyllum = ')
f.write(str(Myriophyllum[2]))
f.write('\n')
f.write('Nothing = ') 
f.write(str(Nothing[2]))
f.write('\n')
f.write('P_Ampliforus = ')
f.write(str(P_Ampliforus[2]))
f.write('\n')
f.write('P_Richardsonii = ')
f.write(str(P_Richardsonii[2]))
f.write('\n')
f.write('P_Robbinsii = ')
f.write(str(P_Robbinsii[2]))
f.write('\n')
f.write('P_Zosteriformis(Zost) = ')
f.write(str(P_Zosteriformis[2]))
f.write('\n')
f.write('Sand = ')
f.write(str(Sand[2]))
f.write('\n')
f.write('\n')
f.write('\n')
f.write('___________________________\n\n')
f.write('\n')
f.write('List of recognized pictures\n\n')
f.write('\n')
f.write('Myriophyllum = ')
f.write(str(Myriophyllum[1]))
f.write('\n')
f.write('Nothing = ') 
f.write(str(Nothing[1]))
f.write('\n')
f.write('P_Ampliforus = ')
f.write(str(P_Ampliforus[1]))
f.write('\n')
f.write('P_Richardsonii = ')
f.write(str(P_Richardsonii[1]))
f.write('\n')
f.write('P_Robbinsii = ')
f.write(str(P_Robbinsii[1]))
f.write('\n')
f.write('P_Zosteriformis(Zost) = ')
f.write(str(P_Zosteriformis[1]))
f.write('\n')
f.write('Sand = ')
f.write(str(Sand[1]))
f.write('\n')
f.write('___________________________\n\n')
f.write('\n')
f.write('List of predictions\n\n')
f.write('\n')
f.write('Myriophyllum = ')
f.write(str(Myriophyllum[3]))
f.write('\n')
f.write('Nothing = ') 
f.write(str(Nothing[3]))
f.write('\n')
f.write('P_Ampliforus = ')
f.write(str(P_Ampliforus[3]))
f.write('\n')
f.write('P_Richardsonii = ')
f.write(str(P_Richardsonii[3]))
f.write('\n')
f.write('P_Robbinsii = ')
f.write(str(P_Robbinsii[3]))
f.write('\n')
f.write('P_Zosteriformis(Zost) = ')
f.write(str(P_Zosteriformis[3]))
f.write('\n')
f.write('Sand = ')
f.write(str(Sand[3]))
f.write('\n')
f.write('\n')
dateTimeObj = datetime.now()
f.write('Finished validating on ' + str(dateTimeObj))
f.write('\n')
f.write('____END____\n\n')



f.write('###########################')

f.close()