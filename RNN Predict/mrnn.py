# Naive LSTM to learn three-char window to one-char mapping
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.utils import np_utils

import pandas as pd

#----------------------------------------------preprocessing--------------------------------------------------------#
file = pd.read_csv('rnn3.csv')
dim = np.arange(59).astype(str)
length = 59


fileTrain = file.sample(frac=0.8, replace=True)
fileTest = file.sample(frac=0.2, replace=True)

#train
labelTrain = fileTrain[str(length)].values.astype(int)
labelTrain = np_utils.to_categorical(labelTrain, 102)
dataTrain1 = np.asarray(fileTrain[dim].values/101)
dataTrain = np.reshape(dataTrain1, (len(dataTrain1), 1, length ))

#test
labelTest = fileTest[str(length )].values.astype(int)
labelTest = np_utils.to_categorical(labelTest, 102)
dataTest1 = np.asarray(fileTest[dim].values/101)
dataTest = np.reshape(dataTest1, (len(dataTest1), 1, length ))

print("----------------input----------------")
print(dataTrain)
print(labelTrain)

#----------------------------------------------train--------------------------------------------------------#
model = Sequential()
model.add(LSTM(256, return_sequences=True,
               input_shape=(dataTrain.shape[1], dataTrain.shape[2])))  # returns a sequence of vectors of dimension 32
model.add(Dropout(0.5))
model.add(LSTM(256, return_sequences=True))  # returns a sequence of vectors of dimension 32
model.add(Dropout(0.5))
model.add(LSTM(256))  # return a single vector of dimension 32
model.add(Dropout(0.5))
model.add(Dense(102, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(dataTrain, labelTrain, nb_epoch=1000, batch_size=64)



#--------------------------------------predict and evaluation--------------------------------------------------#
print("----------------predict----------------")
output = model.predict_classes(dataTest, batch_size=64, verbose=0)
print(output)
# Final evaluation of the model
scores = model.evaluate(dataTest, labelTest, verbose=0)
print("----------------score----------------")
print("Accuracy: %.2f%%" % (scores[1]*100))