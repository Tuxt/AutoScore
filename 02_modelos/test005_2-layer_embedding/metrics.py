

import numpy as np
from keras.callbacks import Callback
from sklearn.metrics import precision_recall_fscore_support



class Metrics(Callback):

    def __init__(self, train_data, train_target):
        self.train_data = train_data
        self.train_target = train_target
        self.train_precisions = []
        self.train_recalls = []
        self.train_f1s = []
        self.val_precisions = []
        self.val_recalls = []
        self.val_f1s = []

    def on_epoch_end(self, epoch, logs={}):
        # Get predictions
        train_predict = self.model.predict(self.train_data)
        train_target = self.train_target
        val_predict = self.model.predict(self.validation_data[0])
        val_target = self.validation_data[1]

        # Get best elements
        train_predict = np.argmax(train_predict, axis=1)
        train_target = np.argmax(train_target, axis=1)
        val_predict = np.argmax(val_predict, axis=1)
        val_target = np.argmax(val_target, axis=1)

        # Get metrics
        #print("TARGET:")
        #print(train_target)
        #print(train_predict)
        train_p, train_r, train_f, _ = precision_recall_fscore_support(train_target, train_predict)
        val_p, val_r, val_f, _ = precision_recall_fscore_support(val_target, val_predict)
        
        # Mean
        train_p = np.mean(train_p)
        train_r = np.mean(train_r)
        train_f = np.mean(train_f)
        val_p = np.mean(val_p)
        val_r = np.mean(val_r)
        val_f = np.mean(val_f)

        # Save data
        self.train_precisions.append(train_p)
        self.train_recalls.append(train_r)
        self.train_f1s.append(train_f)
        self.val_precisions.append(val_p)
        self.val_recalls.append(val_r)
        self.val_f1s.append(val_f)
        print(
            "EPOCH:", str(epoch),
            "\nloss:", str(logs['loss']), "\t\t— val_loss:", str(logs['val_loss']),
            "\nacc:", str(logs['acc']), "\t\t— val_acc:", str(logs['val_acc']),
            "\nprecision:", str(train_p), "\t— val_precision:", str(val_p),
            "\nrecall:", str(train_r), "\t— val_recall:", str(val_r),
            "\nf-measure:", str(train_f), "\t— val_f-measure:", str(val_f)
            )
        return