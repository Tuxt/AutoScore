import pickle
from keras.models import load_model
from datamanager import load
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from vocabulary import Vocabulary as Voc

class Generator:
    
    def __init__(self,
        model_file = 'model/model.h5',
        dictionaries = ('model/note2int', 'model/int2note')):
        self.model = load_model(model_file)
        self.graph = tf.get_default_graph()
        self.note2int = load(dictionaries[0])
        self.int2note = load(dictionaries[1])

    # Validation for selected value
    # Return:
    # - False: new_value is invalid
    # - True: new_value is valid
    # - ']': new_value must be ']' (close chord)
    def _validPrediction(self, input_data, new_value):
        if len(input_data) == 0:
            return True
        input_data = np.vectorize(self.int2note.get)(input_data)
        new_value = self.int2note.get(new_value)
        # Check consecutive multipliers
        if new_value in Voc.MULS and not(input_data[-1] in Voc.NOTES_WITH_SILENCE):
            return False

        # Get chords symbols
        opened = sum( [ step == '[' for step in input_data ] )
        closed = sum( [ step == ']' for step in input_data ] )

        # Check if new_value is chord
        if new_value == '[' and opened > closed:
            return False
        if new_value == ']' and opened <= closed:
            return False

        # Check if chord opened (max 3 notes)
        if opened > closed and new_value != ']':
            # Index of last '['
            input_data = input_data.tolist()
            last_open = len(input_data) - 1 - input_data[::-1].index('[')
            # Last part: inside chord
            last_part = input_data[last_open:]
            num_notes = sum( [ step in Voc.NOTES for step in last_part ] )
            # If new value is 4th note, close chord
            if num_notes >= 3 and new_value in Voc.NOTES_WITH_SILENCE:
                return ']'
        return True

    # Select a valid value
    def _selValue(self, input_data, result, stop=10):
        new_value = np.random.choice( np.arange(0,result.shape[1]), p=result[0] )
        validation = self._validPrediction(input_data, new_value)
        if (not validation) and (stop >= 1):
            new_value = self._selValue(input_data, result, stop-1)
        elif validation == ']':
                new_value = self.note2int.get(validation)
        return new_value

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
        with self.graph.as_default():
            result = self.model.predict(data)
        if get_best:
            new_value = np.argmax(result[0])
        else:
            new_value = self._selValue(input_data, result)


        # Append new data
        input_data = np.append(input_data, new_value)

        return input_data


    def predict(self, input_data, get_best=True, steps=1):
        # Translate input_data notes to ints
        input_data = input_data.split()
        if len(input_data) > 0:
            input_data = np.vectorize(self.note2int.get)(input_data)

        for _ in range(steps):
            input_data = self._predictOne(input_data, get_best)

        # Translate ints to notes
        if len(input_data) > 0:
            input_data = np.vectorize(self.int2note.get)(input_data)
        return ' '.join(input_data)+' '
