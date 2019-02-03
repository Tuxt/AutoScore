'''
    Test 007:
        - Units tuning
'''

from keras.models import Sequential
from keras.layers import Dense, GRU
from keras.callbacks import ModelCheckpoint, EarlyStopping

import datamanager as dm

from hyperas import optim
from hyperopt import Trials, STATUS_OK, tpe
from hyperas.distributions import choice, uniform, conditional

import time
import os

def data():
    x_train = dm.load("dataset/X_train")
    y_train = dm.load("dataset/y_train")
    x_val = dm.load("dataset/X_val")
    y_val = dm.load("dataset/y_val")
    return x_val,y_val,x_val,y_val

def make_model(x_train, y_train, x_val, y_val):
    weights_dir = 'weights'
    history_dir = 'history'
    
    numgrulayers = {{choice(['three'])}}
    numgrulayers = conditional(numgrulayers)


    model = Sequential()
    model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', input_shape=(x_train.shape[1],x_train.shape[2]), return_sequences=True ))
    model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', return_sequences=True ))
    if numgrulayers == 'five':
        model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', return_sequences=True ))
        model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', return_sequences=True ))
    elif numgrulayers == 'six':
        model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', return_sequences=True ))
        model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', return_sequences=True ))
        model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', return_sequences=True ))
    model.add(GRU(units={{choice([32,64,128,256,512])}}, activation='tanh', return_sequences=False ))
    model.add(Dense(y_train.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    if numgrulayers == 'three':
        filename = weights_dir+'/' + \
                numgrulayers + '_' + \
                str(space['units']) + '_' + \
                str(space['units_1']) + '_' + \
                str(space['units_7']) + '_' + \
                str(space['batch_size']) + \
                '_{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5'
    elif numgrulayers == 'five':
        filename = weights_dir+'/' + \
                numgrulayers + '_' + \
                str(space['units']) + '_' + \
                str(space['units_1']) + '_' + \
                str(space['units_2']) + '_' + \
                str(space['units_3']) + '_' + \
                str(space['units_7']) + '_' + \
                str(space['batch_size']) + \
                '_{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5'
    elif numgrulayers == 'six':
        filename = weights_dir+'/' + \
                numgrulayers + '_' + \
                str(space['units']) + '_' + \
                str(space['units_1']) + '_' + \
                str(space['units_4']) + '_' + \
                str(space['units_5']) + '_' + \
                str(space['units_6']) + '_' + \
                str(space['units_7']) + '_' + \
                str(space['batch_size']) + \
                '_{epoch:03d}_{loss:.4f}_{acc:.4f}_{val_loss:.4f}_{val_acc:.4f}.hdf5'

    checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='min')
    earlystopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=3, verbose=0, mode='auto')
    callbacks = [checkpoint,earlystopping]
    
    result = model.fit(x_train, y_train, batch_size={{choice([32,64,128])}}, epochs=20,verbose=6, validation_data=(x_val, y_val), callbacks=callbacks)

    parameters = space
    parameters['history'] = result.history
    if numgrulayers == 'three':
        dm.save(parameters, history_dir + '/' + \
            numgrulayers + '_' + \
            str(space['units']) + '_' + \
            str(space['units_1']) + '_' + \
            str(space['units_7']) + '_' + \
            str(space['batch_size']))
    elif numgrulayers == 'five':
        dm.save(parameters, history_dir + '/' + \
            numgrulayers + '_' + \
            str(space['units']) + '_' + \
            str(space['units_1']) + '_' + \
            str(space['units_2']) + '_' + \
            str(space['units_3']) + '_' + \
            str(space['units_7']) + '_' + \
            str(space['batch_size']))
    elif numgrulayers == 'six':
        dm.save(parameters, history_dir + '/' + \
            numgrulayers + '_' + \
            str(space['units']) + '_' + \
            str(space['units_1']) + '_' + \
            str(space['units_4']) + '_' + \
            str(space['units_5']) + '_' + \
            str(space['units_6']) + '_' + \
            str(space['units_7']) + '_' + \
            str(space['batch_size']))

    loss,acc = model.evaluate(x_val,y_val, verbose=0)
    print("Test loss: "+str(loss)+"\tTest acc: " +str(acc))
    return {'status': STATUS_OK, 'model':model, 'loss':loss, 'acc':acc }


if __name__ == '__main__':
    weights_dir = 'weights'
    history_dir = 'history'
    if not os.path.exists(weights_dir):
        os.makedirs(weights_dir)
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    
    trials = Trials()
    
    best_run, best_model = optim.minimize(model=make_model,
                data=data,
                algo=tpe.suggest,
                max_evals=5,
                trials=trials)
    print("BEST MODEL:")
    print(best_model.summary())
    print("BEST_RUN:")
    print(best_run)
    




