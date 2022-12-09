import tensorboard
import datetime
# Clear any logs from previous runs
# !rm -rf ./logs/ 
import os
import cv2
import numpy as np
import tensorflow as tf
####

# import pandas as pd
# from tqdm import tqdm





from keras.preprocessing import image
import keras
#####
#Encoding and Split data into Train/Test Sets
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

#Tensorflow Keras CNN Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Activation, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop


import matplotlib.pyplot as plt
folder_dir = '/Volumes/Seagate/Steven/OneDrive/SortaSorted_TrainSet2_full'

######################
train_image = []

################################
data = []
label = []
y =[]
SIZE = 128 #Crop the image to 128x128

for folder in os.listdir(folder_dir):
    for file in os.listdir(os.path.join(folder_dir, folder)):
        if file.endswith("png") and str(file[0]) != '.':
            print(file)
            # 
            img = cv2.imread(os.path.join(folder_dir, folder, file))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = cv2.resize(img_rgb, (SIZE,SIZE))
            data.append(im)
            if str(folder) == 'Nothing'or str(folder) == 'Nothing_Recipient':
                label.append('Nothing')
            else:
                label.append('Something')
        else:
            continue

############
data_arr = np.array(data)
label_arr = np.array(label)
############
encoder = LabelEncoder()
y = encoder.fit_transform(label_arr)
y = to_categorical(y,2)
X = data_arr/255
##

############

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=10)

############

model = Sequential()
print("added Sequential")
model.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'Same',activation ='relu', input_shape = (SIZE,SIZE,3)))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(filters = 128, kernel_size = (3,3),padding = 'Same',activation ='relu'))
model.add(Conv2D(filters = 128, kernel_size = (3,3),padding = 'Same',activation ='relu'))
model.add(Conv2D(filters = 128, kernel_size = (3,3),padding = 'Same',activation ='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
print("added Conv2D")

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(2, activation = "softmax"))
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


model.compile(optimizer=Adam(lr=0.0001),loss='categorical_crossentropy',metrics=['accuracy'])
print("compiled")

log_dir = "/Users/pierre/Ubergaiter/Recog/Plant1_v2_large/logs/fit" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

batch_size=16
epochs=50    
history = model.fit_generator(datagen.flow(X_train,y_train, batch_size=batch_size),
                              epochs = epochs,
                              validation_data = (X_test,y_test),
                              verbose = 1,
                              callbacks=[tensorboard_callback])
print("fitted history")

model.save('/Users/pierre/Ubergaiter/Recog/Plant1_v2_large/saved_model_/biggerModel5_TrainSet2_Nothing_Something')


##############################
