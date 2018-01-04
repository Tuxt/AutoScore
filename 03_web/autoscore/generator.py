import pickle
from keras.models import load_model
from datamanager import load
import numpy as np
from keras.preprocessing.sequence import pad_sequences

class Generator:
    
    def __init__(self,
        model_file='model/model.h5',
        dictionaries=('model/note2int', 'model/int2note')):
        self.model = load_model(model_file)
        self.note2int = load(dictionaries[0])
        self.int2note = load(dictionaries[1])

    def _predictOne(self, input_data, get_best=True):
        # Pad data
        data = np.reshape(input_data,
            (1,len(input_data), self.model.input_shape[2]))
        data = pad_sequences(data,
            maxlen=self.model.input_shape[1],
            value=self.model.layers[0].mask_value)

        # Reshape data
        shape = (1, self.model.input_shape[1], self.model.input_shape[2])
        data = data[-shape[1]:].reshape(shape)
        
        # Generate value
        result = self.model.predict(data)
        if get_best:
            new_value = np.argmax(result[0])
        else:
            new_value = np.random.choice( np.arange(0,result.shape[1]), p=result[0] )

        # Append new data
        input_data = np.append(input_data, new_value)

        return input_data


    def predict(self, input_data, get_best=True, steps=1):
        # Translate input_data notes to ints
        input_data = input_data.split()
        if input_data != []:
            input_data = np.vectorize(self.note2int.get)(input_data)

        for _ in range(steps):
            input_data = self._predictOne(input_data, get_best)

        # Translate ints to notes
        if input_data != []:
            input_data = np.vectorize(self.int2note.get)(input_data)
        return ' '.join(input_data)+' '
