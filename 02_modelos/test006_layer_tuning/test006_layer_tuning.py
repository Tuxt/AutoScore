'''
    Test 006:
        - Layer tuning (GRU-128 units)
'''

import argparse
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def numlayer_type(x):
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError("Min value is 1")
    return x


parser = argparse.ArgumentParser(description="Test 006 - Layer tuning")
parser.add_argument("--rnn-units", type=int, default=128)
parser.add_argument("--rnn-activation", default="tanh")
parser.add_argument("--optimizer", default="rmsprop")
parser.add_argument("--batch-size", type=int, default=128)
parser.add_argument("--epochs", type=int, default=100)
parser.add_argument("--min-layers", type=numlayer_type, default=1)
parser.add_argument("--max-layers", type=numlayer_type, default=1)
parser.add_argument("--verbosity", type=int, default=0)

args = parser.parse_args()


import numpy as np
from keras.models import Sequential
from keras.layers import Masking
from keras.layers import GRU
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
import datamanager as dm
#from metrics import Metrics
import time
import os


# Variables and config
rnn_units = args.rnn_units
rnn_activation = args.rnn_activation
dense_activation = 'softmax'
optimizer = args.optimizer
loss = 'categorical_crossentropy'
metrics = ['accuracy']
batch_size = args.batch_size
epochs = args.epochs
max_layers = args.max_layers
min_layers = args.min_layers
verbosity = args.verbosity

weights_dir = 'weights006_GRU-' + str(rnn_units) + '-' + rnn_activation + '_' + optimizer + '_' + str(batch_size) + '-batch_' + str(epochs) + '-epochs'
if not os.path.exists(weights_dir):
    os.makedirs(weights_dir)
history_dir = 'history_GRU-' + str(rnn_units) + '-' + rnn_activation + '_' + optimizer + '_' + str(batch_size) + '-batch_' + str(epochs) + '-epochs'
if not os.path.exists(history_dir):
    os.makedirs(history_dir)


# Load data
X_train = dm.load("dataset/X_train")
y_train = dm.load("dataset/y_train")
X_val = dm.load("dataset/X_val")
y_val = dm.load("dataset/y_val")
X_test = dm.load("dataset/X_test")
y_test = dm.load("dataset/y_test")


for i in range(min_layers, max_layers+1):
    # Make model
    model = Sequential()
    counter = i
    while counter > 0:
        if counter == 1 and counter == i:
            model.add( GRU( units=rnn_units, activation=rnn_activation, input_shape=(X_train.shape[1], X_train.shape[2]) ) )
        elif counter == 1:
            model.add( GRU( units=rnn_units, activation=rnn_activation ) )
        elif counter == i:
            model.add( GRU( units=rnn_units, activation=rnn_activation, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2]) ) )
        else:
            model.add( GRU( units=rnn_units, activation=rnn_activation, return_sequences=True ) )
        counter-=1
    model.add( Dense( y_train.shape[1], activation=dense_activation ) )
    model.compile( optimizer=optimizer, loss=loss, metrics=metrics )
    print('TEST: ' + str(i) + '-layer GRU')
    print(model.summary())
    filename = weights_dir+'/'+str(i)+'-layer_{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5'
    checkpoint = [ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='min')]
    start = time.time()
    history = model.fit( x=X_train, y=y_train, batch_size=batch_size, epochs=epochs, verbose=verbosity, validation_data=(X_val,y_val), callbacks=checkpoint )
    end = time.time()
    
    # Save results
    dm.save(history.history, history_dir + '/' + str(i) + '-layer_test006_loss_acc')
    
    print("-"*30)
    print("TRAIN DATA: " + str(model.metrics_names))
    print(model.evaluate(x=X_train, y=y_train, batch_size=batch_size, verbose=verbosity))
    print("-"*30)
    print("VALIDATION DATA: " + str(model.metrics_names))
    print(model.evaluate(x=X_val, y=y_val, batch_size=batch_size, verbose=verbosity))
    print("-"*30)
    print("TEST DATA: " + str(model.metrics_names))
    print(model.evaluate(x=X_test, y=y_test, batch_size=batch_size, verbose=verbosity))
    
    print(str(epochs) + ' epochs in '+ str(end-start) + ' seconds')
    print('-'*30)
    print('-'*30)
    print('\n\n')


