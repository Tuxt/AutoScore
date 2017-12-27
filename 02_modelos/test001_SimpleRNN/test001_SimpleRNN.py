'''
    Test 001:
        - SimpleRNN
        - Initial test
'''

import argparse
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

parser = argparse.ArgumentParser(description="Test 001 - 1-layer SimpleRNN with dataset1")
parser.add_argument("DATASET")
parser.add_argument("--padding", action="store_true")
parser.add_argument("--imbalanced-threshold", type=int, default=0)
parser.add_argument("--max-timesteps", type=int, default=10)
parser.add_argument("--rnn-units", type=int, default=128)
parser.add_argument("--rnn-activation", default="tanh")
parser.add_argument("--dropout", type=float, default=0.2)
parser.add_argument("--dense-activation", default="softmax")
parser.add_argument("--optimizer", default="rmsprop")
parser.add_argument("--loss", default="categorical_crossentropy")
parser.add_argument("--batch-size", type=int, default=128)
parser.add_argument("--epochs", type=int, default=20)
parser.add_argument("--verbosity", type=int, default=0)

args = parser.parse_args()

# Variables and config
dataset = args.DATASET
padding = args.padding
imbalanced_threshold = args.imbalanced_threshold
timesteps = args.max_timesteps
rnn_units = args.rnn_units
rnn_activation = args.rnn_activation
dropout = args.dropout
dense_activation = args.dense_activation
optimizer = args.optimizer
loss = args.loss
metrics = ['accuracy']
batch_size = args.batch_size
epochs = args.epochs
verbosity = args.verbosity


import numpy as np
from keras.models import Sequential
from keras.layers import SimpleRNN
from keras.layers import Dropout
from keras.layers import Dense
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import datamanager as dm

# Load data
X,y,note_to_int,int_to_note = dm.load_data(dataset, time_steps=timesteps, make_dict=True, to_int=True, imbalanced_threshold=imbalanced_threshold, padding=padding)
X = np.array(X).reshape(len(X), timesteps, 1)
y = np_utils.to_categorical(y)

# (Train = 0.6   Validation = 0.2)    Test = 0.2
trainX = X[:int(X.shape[0]*0.6)]
trainY = y[:int(y.shape[0]*0.6)]

validationX = X[int(X.shape[0]*0.6) : int(X.shape[0]*0.8)]
validationY = y[int(y.shape[0]*0.6) : int(y.shape[0]*0.8)]

testX = X[int(X.shape[0]*0.8):]
testY = y[int(y.shape[0]*0.8):]

# Make model
model = Sequential()
model.add( SimpleRNN( units=rnn_units, activation=rnn_activation, input_shape=( X.shape[1], X.shape[2] ) ) )
model.add( Dropout( dropout ) )
model.add( Dense( y.shape[1], activation=dense_activation) )
model.compile( optimizer=optimizer, loss=loss, metrics=metrics )

#print(model.summary())

# Filename: SimpleRNN_1-layer_[dataset]_[padding|no-padding]_A-timesteps_B-[activation]-units_C-dropout_[optimizer]_[loss]_D-batch-size_epoch_loss_accuracy_vLoss_vAccuracy.hdf5
filename = "weight001/SimpleRNN_1-layer_"+dataset.split("/")[-1]+("_padding_" if padding else "_no-padding_")+str(timesteps)+"-timesteps_"+str(rnn_units)+"-"+rnn_activation+"-units_"+\
        str(dropout)+"-dropout_"+optimizer+"_"+loss+"_"+str(batch_size)+"-batch-size_{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5"

checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='min')

model.fit(x=trainX, y=trainY, batch_size=batch_size, epochs=epochs, verbose=verbosity, validation_data=(validationX,validationY), callbacks=[checkpoint] )

print("-"*30)
print("TRAIN DATA: " + str(model.metrics_names))
print(model.evaluate(x=trainX, y=trainY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("VALIDATION DATA: " + str(model.metrics_names))
print(model.evaluate(x=validationX, y=validationY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("TEST DATA: " + str(model.metrics_names))
print(model.evaluate(x=testX, y=testY, batch_size=batch_size, verbose=verbosity))


