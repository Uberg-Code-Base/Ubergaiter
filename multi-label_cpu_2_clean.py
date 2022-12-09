import tensorboard
from datetime import datetime
import os
import cv2
import numpy as np
import tensorflow as tf
####



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


from keras.preprocessing import image
import keras
#####
#Encoding and Split data into Train/Test Sets
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer


#Tensorflow Keras CNN Model
from sklearn.metrics import classification_report,confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Activation, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop
from tensorflow.keras import backend as K
from tensorflow.keras.regularizers import l2

#Plot Images
import matplotlib.pyplot as plt

folder_dir = '/Volumes/Seagate/Steven/OneDrive/SortaSorted_TrainSet2_full'

######################
train_image = []
labelsArray = []
init ='he_normal'

################################
data = []
labels = []
y =[]
SIZE = 256 #Crop the image to 128x128

for folder in os.listdir(folder_dir):
    print(folder)
    labelsArray.append(str(folder))
    print(labelsArray)
    for file in os.listdir(os.path.join(folder_dir, folder)):
        if file.endswith("png") and str(file[0]) != '.':
            print(file)
            img = cv2.imread(os.path.join(folder_dir, folder, file))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = cv2.resize(img_rgb, (SIZE,SIZE))
            data.append(im)
            myl = 0
            rob = 0
            elo = 0
            rich = 0
            crisp = 0
            amp = 0
            grami = 0
            utri = 0
            sparg = 0
            cera = 0
            erio = 0
            valli = 0
            het = 0
            cal = 0
            nuph = 0
            stuck = 0
            chara = 0
            sagi = 0
            prael = 0
            zost = 0
            niet = 0
            blur = 0
            other = 0
            sand = 0
            label = [myl,rob,elo,rich,crisp,amp,grami,utri,sparg,cera,erio,valli,het,cal,nuph,stuck,chara,sagi,prael,zost,niet,blur,other,sand]
           
            for i in range(len(legend)):
                if str(folder) == legend[i]:
                    label[i] = 1
            labels.append(label)
        else:
            continue

############
data_arr = np.array(data)
y = np.array(labels)
############
X = data_arr/255
##
lb = LabelBinarizer()
labelsLB = lb.fit_transform(legend)
############

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=10)

############ lets tweak the cnn  - more layers and more 
chanDim = -1
model = Sequential()
print("added Sequential")
model.add(Conv2D(filters = 64, kernel_size = (3,3),kernel_initializer=init,kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu', input_shape = (SIZE,SIZE,3)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(BatchNormalization(axis=chanDim))

model.add(Conv2D(filters = 128, kernel_size = (3,3),kernel_initializer=init,kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(filters = 128, kernel_size = (3,3),kernel_initializer=init,kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(Conv2D(filters = 256, kernel_size = (5,5), strides=(2,2),kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(Dropout(0.25))
model.add(BatchNormalization(axis=chanDim))
#######
model.add(Conv2D(filters = 256, kernel_size = (5,5),kernel_initializer=init,kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(filters = 512, kernel_size = (7,7),kernel_initializer=init,kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(Dropout(0.25))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(filters = 1024, kernel_size = (7,7), kernel_initializer=init,strides=(2,2),kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(BatchNormalization(axis=chanDim))
model.add(Conv2D(filters = 512, kernel_size = (5,5),kernel_initializer=init,kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(Dropout(0.25))
model.add(BatchNormalization(axis=chanDim))
model.add(Conv2D(filters = 256, kernel_size = (3,3),kernel_initializer=init,kernel_regularizer=l2(0.0005),padding = 'Same',activation ='relu'))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(pool_size=(2,2)))
print("added Conv2D")

model.add(Flatten())
model.add(Dense(1024, activation='relu',kernel_initializer=init))
model.add(Dense(512, activation='relu'))

model.add(Dense(64, activation='relu'))
model.add(BatchNormalization())

model.add(Dropout(rate=0.25))
model.add(Dense(24, activation = "sigmoid"))
print("added Flatten, Dense and Dropout")

############################

datagen = ImageDataGenerator(
        rotation_range=20,
        zoom_range = 0.20,
        width_shift_range=0.3,
        height_shift_range=0.3,
        horizontal_flip=True,
        vertical_flip=True)

datagen.fit(X_train)
print("fitted X_train")

############################
dateTimeNow = datetime.now().strftime("%Y%m%d-%H%M%S")
model.summary()
epochs=60  
model.compile(optimizer=Adam(learning_rate=0.0001, decay=1e-4 / epochs),loss='binary_crossentropy',metrics=['accuracy'])
print("compiled")
modelName = 'trainset2Full_multi_2_' + dateTimeNow
log_dir = "/Users/pierre/Ubergaiter/Recog/Plant1_v2_large/logs/fit_" + modelName + '_' + dateTimeNow
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

batch_size=16
  
H = model.fit(datagen.flow(X_train,y_train, batch_size=batch_size),
                              epochs = epochs,
                              validation_data = (X_test,y_test),
                              verbose = 1,
                              steps_per_epoch=len(X_train) // batch_size,
                              callbacks=[tensorboard_callback])
print("fitted history")

model.save('/Users/pierre/Ubergaiter/Recog/Plant1_v2_large/saved_model_/' + modelName)

fileNowName = 'train_' + str(modelName) + '_stats'+ '.txt'
f = open(fileNowName, "a")
#testing
print("[INFO] printing graph...")

N = epochs
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy on Dataset")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig('Plot : ' + modelName + '.png')

target_names = [f"class{i}" for i in range(len(y_test.argmax(axis=1)))]
print(y_test.argmax(axis=1))
print("[INFO] evaluating network...")
predictions = model.predict(x=X_test, batch_size=16)
print(predictions)
y_pred = np.argmax(predictions, axis=1)
print(len(y_pred))
print(y_pred)
print(y_test.argmax(axis=1))
report = classification_report(y_test.argmax(axis=1),
	y_pred)
print(report)
f.write(report)
print(report)

##############################
