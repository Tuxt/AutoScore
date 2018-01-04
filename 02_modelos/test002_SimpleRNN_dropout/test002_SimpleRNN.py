'''
    Test 002:
        - SimpleRNN
        - Padding + masking
        - Complete dictionary
'''

import argparse
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

parser = argparse.ArgumentParser(description="Test 002 - 1-layer SimpleRNN with complete dictionary and padding")
parser.add_argument("DATASET")
parser.add_argument("--max-timesteps", type=int, default=10)
parser.add_argument("--rnn-units", type=int, default=128)
parser.add_argument("--rnn-activation", default="tanh")
parser.add_argument("--dropout1", type=float, default=0.2)
parser.add_argument("--dropout2", type=float, default=0.2)
parser.add_argument("--recurrent-dropout", type=float, default=0.2)
parser.add_argument("--optimizer", default="rmsprop")
parser.add_argument("--batch-size", type=int, default=128)
parser.add_argument("--epochs", type=int, default=100)
parser.add_argument("--verbosity", type=int, default=0)

args = parser.parse_args()

# Variables and config
weights_dir = 'weights002'
dataset = args.DATASET
timesteps = args.max_timesteps
rnn_units = args.rnn_units
rnn_activation = args.rnn_activation
dropout1 = args.dropout1
dropout2 = args.dropout2
recurrent_dropout = args.recurrent_dropout
dense_activation = 'softmax'
optimizer = args.optimizer
loss = 'categorical_crossentropy'
metrics = ['accuracy']
batch_size = args.batch_size
epochs = args.epochs
verbosity = args.verbosity


import numpy as np
from keras.models import Sequential
from keras.layers import Masking
from keras.layers import SimpleRNN
from keras.layers import Dropout
from keras.layers import Dense
from keras.utils import np_utils
from keras.constraints import max_norm
from keras.callbacks import ModelCheckpoint
import datamanager2 as dm

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
if dropout1:
	model.add( Dropout( dropout1 ) )
if dropout1 or dropout2 or recurrent_dropout:
	model.add( SimpleRNN( units=rnn_units, activation=rnn_activation, recurrent_dropout=recurrent_dropout, kernel_constraint=max_norm(3.) ) )
else:
	model.add( SimpleRNN( units=rnn_units, activation=rnn_activation, recurrent_dropout=recurrent_dropout ) )
if dropout2:
	model.add( Dropout( dropout2 ) )
model.add( Dense( y.shape[1], activation=dense_activation) )
model.compile( optimizer=optimizer, loss=loss, metrics=metrics )

#print(model.summary())

# Filename: SimpleRNN_1-layer_A-timesteps_B-[activation]-units_C-dropout1_D-dropout2_E-recurrent-dropout_[optimizer]_[loss]_D-batch-size_epoch_loss_accuracy_vLoss_vAccuracy.hdf5
filename = weights_dir+"/SimpleRNN_1-layer_"+str(timesteps)+"-timesteps_"+str(rnn_units)+"-"+rnn_activation+"-units_"+\
        str(dropout1)+"-dropout1_"+str(dropout2)+"-dropout2_"+str(recurrent_dropout)+"-recurrent-dropout_"+\
        optimizer+"_"+loss+"_"+str(batch_size)+"-batch-size_{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5"

checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='min')

history = model.fit(x=trainX, y=trainY, batch_size=batch_size, epochs=epochs, verbose=verbosity, validation_data=(validationX,validationY), callbacks=[checkpoint] )

dm.save(history.history, "history/test002_"+str(dropout1)+"-dr1_"+str(dropout2)+"-dr2_"+str(recurrent_dropout)+"-rnndrop")

print("-"*30)
print("TRAIN DATA: " + str(model.metrics_names))
print(model.evaluate(x=trainX, y=trainY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("VALIDATION DATA: " + str(model.metrics_names))
print(model.evaluate(x=validationX, y=validationY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("TEST DATA: " + str(model.metrics_names))
print(model.evaluate(x=testX, y=testY, batch_size=batch_size, verbose=verbosity))


