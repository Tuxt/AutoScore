'''
    Test 003:
        - LSTM
        - Padding + masking
        - Complete dictionary
        - No dropout
'''

import argparse
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

parser = argparse.ArgumentParser(description="Test 003 - 1-layer (SimpleRNN/LSTM) with complete dictionary and padding")
parser.add_argument("DATASET")
parser.add_argument("--layer")
parser.add_argument("--max-timesteps", type=int, default=10)
parser.add_argument("--rnn-units", type=int, default=128)
parser.add_argument("--rnn-activation", default="tanh")
parser.add_argument("--optimizer", default="rmsprop")
parser.add_argument("--batch-size", type=int, default=128)
parser.add_argument("--epochs", type=int, default=100)
parser.add_argument("--verbosity", type=int, default=0)

args = parser.parse_args()


import numpy as np
from keras.models import Sequential
from keras.layers import Masking
from keras.layers import SimpleRNN
from keras.layers import LSTM
from keras.layers import GRU
from keras.layers import Dense
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import datamanager2 as dm
from metrics import Metrics


# Variables and config
weights_dir = 'weights003'
dataset = args.DATASET
layer = args.layer
timesteps = args.max_timesteps
rnn_units = args.rnn_units
rnn_activation = args.rnn_activation
dense_activation = 'softmax'
optimizer = args.optimizer
loss = 'categorical_crossentropy'
metrics = ['accuracy']
batch_size = args.batch_size
epochs = args.epochs
verbosity = args.verbosity



# Load data
X,y,note_to_int,int_to_note = dm.load_data(dataset, time_steps=timesteps, make_dict=True, to_int=True, padding=True)
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
model.add( Masking( mask_value=-1, input_shape=(X.shape[1], X.shape[2]) ) )
if layer == "SimpleRNN":
	model.add( SimpleRNN( units=rnn_units, activation=rnn_activation) )
elif layer == "LSTM":
	model.add( LSTM( units=rnn_units, activation=rnn_activation ) )
elif layer == "GRU":
    model.add( GRU( units=rnn_units, activation=rnn_activation ) )
else:
	print("ERROR: Invalid layer",layer)
	exit(1)
model.add( Dense( y.shape[1], activation=dense_activation) )
model.compile( optimizer=optimizer, loss=loss, metrics=metrics )

print(model.summary())

# Filename: [layer]_1-layer_A-timesteps_B-[activation]-units_[optimizer]_[loss]_D-batch-size_[epoch]_[loss]_[accuracy]_[vLoss]_[vAccuracy].hdf5
filename = weights_dir+"/"+layer+"_1-layer_"+str(timesteps)+"-timesteps_"+str(rnn_units)+"-"+rnn_activation+"-units_"+\
        optimizer+"_"+loss+"_"+str(batch_size)+"-batch-size_{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5"

callback_metric = Metrics(trainX, trainY)
checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='min')
checkpoint = [checkpoint, callback_metric]
if "dataset1" in dataset:
    checkpoint=[callback_metric]

history = model.fit(x=trainX, y=trainY, batch_size=batch_size, epochs=epochs, verbose=verbosity, validation_data=(validationX,validationY), callbacks=checkpoint )

dm.save(history.history, "history/test003_"+layer+"-1-layer_"+str(timesteps)+"-timesteps_"+dataset.split("/")[-1]+"-dataset")
dm.save(callback_metric.train_precisions, "history/test003_train-precision_"+layer+"-1-layer_"+str(timesteps)+"-timesteps_"+dataset.split("/")[-1]+"-dataset")
dm.save(callback_metric.val_precisions, "history/test003_val-precision_"+layer+"-1-layer_"+str(timesteps)+"-timesteps_"+dataset.split("/")[-1]+"-dataset")
dm.save(callback_metric.train_recalls, "history/test003_train-recall_"+layer+"-1-layer_"+str(timesteps)+"-timesteps_"+dataset.split("/")[-1]+"-dataset")
dm.save(callback_metric.val_recalls, "history/test003_val-recall_"+layer+"-1-layer_"+str(timesteps)+"-timesteps_"+dataset.split("/")[-1]+"-dataset")
dm.save(callback_metric.train_f1s, "history/test003_train-fscore_"+layer+"-1-layer_"+str(timesteps)+"-timesteps_"+dataset.split("/")[-1]+"-dataset")
dm.save(callback_metric.val_f1s, "history/test003_val-fscore_"+layer+"-1-layer_"+str(timesteps)+"-timesteps_"+dataset.split("/")[-1]+"-dataset")

print("-"*30)
print("TRAIN DATA: " + str(model.metrics_names))
print(model.evaluate(x=trainX, y=trainY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("VALIDATION DATA: " + str(model.metrics_names))
print(model.evaluate(x=validationX, y=validationY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("TEST DATA: " + str(model.metrics_names))
print(model.evaluate(x=testX, y=testY, batch_size=batch_size, verbose=verbosity))


