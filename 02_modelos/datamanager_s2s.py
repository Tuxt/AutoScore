import pickle
import numpy as np

def load_data(data_file, padding=False, start_token='<start>', stop_token='<stop>'):
    with open(data_file) as f:
        lines = f.read().splitlines()


    phrases = []
    inputs = []
    targets = []
    for line in lines:
        compases = line.split(' | ')
        phrases += compases


        for i in range(len(compases) - 1):
            inputs.append(compases[i])
            targets.append(start_token + ' ' + compases[i+1] + ' ' + stop_token)
    phrases = [ phrase.split() for phrase in phrases ]
    

    # Get sets of words
    words = set(word for phrase in phrases for word in phrase)
    encoder_words = sorted(words)
    decoder_words = [start_token, stop_token] + sorted(words)

    # Get num of words
    num_encoder_words = len(encoder_words)
    num_decoder_words = len(decoder_words)

    # Get max sequence lengths
    encoder_timesteps = max(np.vectorize(len) (phrases))
    decoder_timesteps = encoder_timesteps + 2

    # Dictionaries
    encoder_note2int = dict((word, index) for index, word in enumerate(encoder_words))
    decoder_note2int = dict((word, index) for index, word in enumerate(decoder_words))



    encoder_input = np.zeros( ( len(inputs), encoder_timesteps, num_encoder_words ), dtype='float32' )
    decoder_input = np.zeros( ( len(inputs), decoder_timesteps, num_decoder_words ), dtype='float32' )
    decoder_target = np.zeros( ( len(inputs), decoder_timesteps, num_decoder_words ), dtype='float32' )
    
    for i, (input_val, target_val) in enumerate(zip(inputs, targets)):
        for t, word in enumerate(input_val.split()):
            encoder_input[i, t, encoder_note2int[word]] = 1.0
        for t, word in enumerate(target_val.split()):
            decoder_input[i, t, decoder_note2int[word]] = 1.0
            if t > 0:
                # Skip start token
                decoder_target[i, t - 1, decoder_note2int[word]] = 1.0

    return encoder_input, decoder_input, decoder_target, encoder_note2int, decoder_note2int

    

def save(dic, name):
    with open(name + '.pkl', 'wb+') as f:
        pickle.dump(dic, f, pickle.HIGHEST_PROTOCOL)

def load(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


# AUX
def shuffle(x,y):
    index = [ i for i in range(len(x)) ]
    np.random.shuffle(index)
    return np.array(x)[index], np.array(y)[index]
