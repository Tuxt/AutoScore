import pickle
import numpy as np

def load_data(data_file, make_dict=False, to_int=False, time_steps=10, imbalanced_threshold=0, padding=False):
    with open(data_file) as f:
        lines = f.read().splitlines()

    X = []
    y = []

    # Imbalanced data threshold checking
    if imbalanced_threshold != 0:
        # Count words
        counter = {}
        for line in lines:
            for word in line.split():
                counter[word] = counter.get(word,0) + 1
        
        # Select words to delete
        del_words = [ k for k,v in counter.items() if v < imbalanced_threshold ]

        # Delete words
        filtered_lines = []
        for line in lines:
            filtered_words = []
            for word in line.split():
                if not word in del_words:
                    filtered_words.append(word)
            filtered_lines.append(" ".join(filtered_words))

        lines = filtered_lines

    # Make dataset sequences
    if padding:
        for line in lines:
            words = line.split()
            for i in range( 1, len(words) ):
                X.append( words[ 0 if i < time_steps else i-time_steps : i ] )
                y.append( words[i] )
    else:
        for line in lines:
            words = line.split()
            for i in range( len(words) - time_steps ):
                X.append( words[ i : i+time_steps ] )
                y.append( words[ i+time_steps ] )

    if make_dict or to_int:
        values = [item for sublist in X for item in sublist]
        values = sorted( set( values + y ) )
        note_to_int = {}
        int_to_note = {}
        if padding:
            note_to_int["z"] = 0
            int_to_note[0] = "z"
            for i,n in enumerate(values,1):
                note_to_int[n] = i
                int_to_note[i] = n
        else:
            for i,n in enumerate(values):
                note_to_int[n] = i
                int_to_note[i] = n

        if make_dict and not to_int:
            return X, y, note_to_int, int_to_note
        
        intX = [ [ note_to_int[note] for note in sequence ] for sequence in X ]
        intY = [ note_to_int[note] for note in y ]

        if padding:
            from keras.preprocessing.sequence import pad_sequences
            intX = pad_sequences(intX, maxlen=time_steps)

        if make_dict:
            return intX, intY, note_to_int, int_to_note
        else:
            return intX, intY

    return X,y

def save(dic, name):
    with open('model/' + name + '.pkl', 'wb+') as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)

def load(name):
    with open('model/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

