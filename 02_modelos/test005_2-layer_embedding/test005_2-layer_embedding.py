'''
    Test 005:
    	- 2 layer RNN + Embedding
'''

import argparse
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

parser = argparse.ArgumentParser(description="Test 005 - 2-layer (SimpleRNN/LSTM/GRU) with embedding")
parser.add_argument("DATASET")
parser.add_argument("--embedding-output-dim", type=int, default=5)
parser.add_argument("--rnn-layer1")
parser.add_argument("--rnn-units1", type=int, default=128)
parser.add_argument("--rnn-activation1", default="tanh")
parser.add_argument("--rnn-layer2")
parser.add_argument("--rnn-units2", type=int, default=128)
parser.add_argument("--rnn-activation2", default="tanh")
parser.add_argument("--max-timesteps", type=int, default=10)
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
from keras.layers import Embedding
from keras.layers import Reshape
from keras.layers import Dense
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import datamanager2 as dm
from metrics import Metrics
import time
import os


# Variables and config
dataset = args.DATASET
embedding_output_dim = args.embedding_output_dim
rnn_layer1 = args.rnn_layer1
rnn_units1 = args.rnn_units1
rnn_activation1 = args.rnn_activation1
rnn_layer2 = args.rnn_layer2
rnn_units2 = args.rnn_units2
rnn_activation2 = args.rnn_activation2
timesteps = args.max_timesteps
dense_activation = 'softmax'
optimizer = args.optimizer
loss = 'categorical_crossentropy'
metrics = ['accuracy']
batch_size = args.batch_size
epochs = args.epochs
verbosity = args.verbosity
weights_dir = 'weights005_' + rnn_layer1 + '-' + str(rnn_units1) + '_' + rnn_layer2 + '-' + str(rnn_units2) + '_' + str(embedding_output_dim) + '-embedding'
if not os.path.exists(weights_dir):
    os.makedirs(weights_dir)
history_dir = 'history_' + rnn_layer1 + '-' + str(rnn_units1) + '_' + rnn_layer2 + '-' + str(rnn_units2) + '_' + str(embedding_output_dim) + '-embedding'
if not os.path.exists(history_dir):
    os.makedirs(history_dir)


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
model.add( Embedding( y.shape[1], embedding_output_dim, input_shape=(X.shape[1], X.shape[2] ) ) )
model.add( Reshape( ( X.shape[1], embedding_output_dim ) , input_shape=(X.shape[1], X.shape[2], embedding_output_dim ) ) )
if rnn_layer1 == "SimpleRNN":
	model.add( SimpleRNN( units=rnn_units1, activation=rnn_activation1, return_sequences=True) )
elif rnn_layer1 == "LSTM":
	model.add( LSTM( units=rnn_units1, activation=rnn_activation1, return_sequences=True ) )
elif rnn_layer1 == "GRU":
    model.add( GRU( units=rnn_units1, activation=rnn_activation1, return_sequences=True ) )
else:
	print("ERROR: Invalid rnn-layer1",layer)
	exit(1)

if rnn_layer2 == "SimpleRNN":
	model.add( SimpleRNN( units=rnn_units2, activation=rnn_activation2) )
elif rnn_layer2 == "LSTM":
	model.add( LSTM( units=rnn_units2, activation=rnn_activation2 ) )
elif rnn_layer2 == "GRU":
    model.add( GRU( units=rnn_units2, activation=rnn_activation2 ) )
else:
	print("ERROR: Invalid rnn-layer2",layer)
	exit(1)

model.add( Dense( y.shape[1], activation=dense_activation) )
model.compile( optimizer=optimizer, loss=loss, metrics=metrics )

print(model.summary())

# Filename: [layer]_1-layer_A-timesteps_B-[activation]-units_[optimizer]_[loss]_D-batch-size_[epoch]_[loss]_[accuracy]_[vLoss]_[vAccuracy].hdf5
filename = weights_dir+"/{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5"

callback_metric = Metrics(trainX, trainY)
checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='min')
checkpoint = [checkpoint, callback_metric]

start = time.time()
history = model.fit(x=trainX, y=trainY, batch_size=batch_size, epochs=epochs, verbose=verbosity, validation_data=(validationX,validationY), callbacks=checkpoint )
end = time.time()

dm.save(history.history, history_dir + "/test005_loss_acc")
dm.save(callback_metric.train_precisions, history_dir + "/test005_train-precision")
dm.save(callback_metric.val_precisions, history_dir + "/test005_val-precision")
dm.save(callback_metric.train_recalls, history_dir + "/test005_train-recall")
dm.save(callback_metric.val_recalls, history_dir + "/test005_val-recall")
dm.save(callback_metric.train_f1s, history_dir + "/test005_train-fscore")
dm.save(callback_metric.val_f1s, history_dir + "/test005_val-fscore")

print("-"*30)
print("TRAIN DATA: " + str(model.metrics_names))
print(model.evaluate(x=trainX, y=trainY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("VALIDATION DATA: " + str(model.metrics_names))
print(model.evaluate(x=validationX, y=validationY, batch_size=batch_size, verbose=verbosity))
print("-"*30)
print("TEST DATA: " + str(model.metrics_names))
print(model.evaluate(x=testX, y=testY, batch_size=batch_size, verbose=verbosity))

print(str(epochs) + ' epochs in '+ str(end-start) + ' seconds')


