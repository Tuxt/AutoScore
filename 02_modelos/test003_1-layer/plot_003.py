import datamanager2 as dm
test003_srnn50antiguo = dm.load('history/test003/test003_SimpleRNN-1-layer_50-timesteps_dataset1_clean.abc-dataset')
test003_srnn50nuevo = dm.load('history/test003/test003_SimpleRNN-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_srnn100nuevo = dm.load('history/test003/test003_SimpleRNN-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_lstm50nuevo = dm.load('history/test003/test003_LSTM-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_lstm100nuevo = dm.load('history/test003/test003_LSTM-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_gru50nuevo = dm.load('history/test003/test003_GRU-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_gru100nuevo = dm.load('history/test003/test003_GRU-1-layer_100-timesteps_archivo_salida_arreglado-dataset')

from matplotlib import pyplot as plt
import numpy as np

# Loss plot:
plt.subplot(121)
plt.axis([0,19,0.,2.8])
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.grid(axis='y')
plt.xticks(np.arange(0,20,2))
plt.yticks(np.arange(0,2.9,0.2))
plt.plot(test003_srnn50antiguo['loss'], 'b', label='Train Loss: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50antiguo['val_loss'], 'b--', label='Validation Loss: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50nuevo['loss'], 'g', label='Train Loss: SimpleRNN 50-ts')
plt.plot(test003_srnn50nuevo['val_loss'], 'g--', label='Validation Loss: SimpleRNN 50-ts')
plt.plot(test003_srnn100nuevo['loss'], 'r', label='Train Loss: SimpleRNN 100-ts')
plt.plot(test003_srnn100nuevo['val_loss'], 'r--', label='Validation Loss: SimpleRNN 100-ts')
plt.plot(test003_lstm50nuevo['loss'], 'c', label='Train Loss: LSTM 50-ts')
plt.plot(test003_lstm50nuevo['val_loss'], 'c--', label='Validation Loss: LSTM 50-ts')
plt.plot(test003_lstm100nuevo['loss'], 'm', label='Train Loss: LSTM 100-ts')
plt.plot(test003_lstm100nuevo['val_loss'], 'm--', label='Validation Loss: LSTM 100-ts')
plt.plot(test003_gru50nuevo['loss'], 'y', label='Train Loss: GRU 50-ts')
plt.plot(test003_gru50nuevo['val_loss'], 'y--', label='Validation Loss: GRU 50-ts')
plt.plot(test003_gru100nuevo['loss'], 'k', label='Train Loss: GRU 100-ts')
plt.plot(test003_gru100nuevo['val_loss'], 'k--', label='Validation Loss: GRU 100-ts')
plt.legend()


# Accuracy plot:
plt.subplot(122)
plt.axis([0,19,0,1])
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.grid(axis='y')
plt.xticks(np.arange(0,20,2))
plt.yticks(np.arange(0,1.05,0.05))
plt.plot(test003_srnn50antiguo['acc'], 'b', label='Train Accuracy: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50antiguo['val_acc'], 'b--', label='Validation Accuracy: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50nuevo['acc'], 'g', label='Train Accuracy: SimpleRNN 50-ts')
plt.plot(test003_srnn50nuevo['val_acc'], 'g--', label='Validation Accuracy: SimpleRNN 50-ts')
plt.plot(test003_srnn100nuevo['acc'], 'r', label='Train Accuracy: SimpleRNN 100-ts')
plt.plot(test003_srnn100nuevo['val_acc'], 'r--', label='Validation Accuracy: SimpleRNN 100-ts')
plt.plot(test003_lstm50nuevo['acc'], 'c', label='Train Accuracy: LSTM 50-ts')
plt.plot(test003_lstm50nuevo['val_acc'], 'c--', label='Validation Accuracy: LSTM 50-ts')
plt.plot(test003_lstm100nuevo['acc'], 'm', label='Train Accuracy: LSTM 100-ts')
plt.plot(test003_lstm100nuevo['val_acc'], 'm--', label='Validation Accuracy: LSTM 100-ts')
plt.plot(test003_gru50nuevo['acc'], 'y', label='Train Accuracy: GRU 50-ts')
plt.plot(test003_gru50nuevo['val_acc'], 'y--', label='Validation Accuracy: GRU 50-ts')
plt.plot(test003_gru100nuevo['acc'], 'k', label='Train Accuracy: GRU 100-ts')
plt.plot(test003_gru100nuevo['val_acc'], 'k--', label='Validation Accuracy: GRU 100-ts')
plt.legend()

plt.show()


# Precision plot:
# Load data
test003_srnn50antiguo_precision = dm.load('history/test003/test003_train-precision_SimpleRNN-1-layer_50-timesteps_dataset1_clean.abc-dataset')
test003_srnn50nuevo_precision = dm.load('history/test003/test003_train-precision_SimpleRNN-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_srnn100nuevo_precision = dm.load('history/test003/test003_train-precision_SimpleRNN-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_lstm50nuevo_precision = dm.load('history/test003/test003_train-precision_LSTM-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_lstm100nuevo_precision = dm.load('history/test003/test003_train-precision_LSTM-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_gru50nuevo_precision = dm.load('history/test003/test003_train-precision_GRU-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_gru100nuevo_precision = dm.load('history/test003/test003_train-precision_GRU-1-layer_100-timesteps_archivo_salida_arreglado-dataset')

test003_srnn50antiguo_val_precision = dm.load('history/test003/test003_val-precision_SimpleRNN-1-layer_50-timesteps_dataset1_clean.abc-dataset')
test003_srnn50nuevo_val_precision = dm.load('history/test003/test003_val-precision_SimpleRNN-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_srnn100nuevo_val_precision = dm.load('history/test003/test003_val-precision_SimpleRNN-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_lstm50nuevo_val_precision = dm.load('history/test003/test003_val-precision_LSTM-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_lstm100nuevo_val_precision = dm.load('history/test003/test003_val-precision_LSTM-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_gru50nuevo_val_precision = dm.load('history/test003/test003_val-precision_GRU-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_gru100nuevo_val_precision = dm.load('history/test003/test003_val-precision_GRU-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
# Plot data
plt.subplot(131)
plt.axis([0,19,0,1])
plt.title('Precision')
plt.xlabel('epochs')
plt.ylabel('precision')
plt.grid(axis='y')
plt.xticks(np.arange(0,20,2))
plt.yticks(np.arange(0,1.05,0.05))
plt.plot(test003_srnn50antiguo_precision, 'b', label='Train Precision: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50antiguo_val_precision, 'b--', label='Validation Precision: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50nuevo_precision, 'g', label='Train Precision: SimpleRNN 50-ts')
plt.plot(test003_srnn50nuevo_val_precision, 'g--', label='Validation Precision: SimpleRNN 50-ts')
plt.plot(test003_srnn100nuevo_precision, 'r', label='Train Precision: SimpleRNN 100-ts')
plt.plot(test003_srnn100nuevo_val_precision, 'r--', label='Validation Precision: SimpleRNN 100-ts')
plt.plot(test003_lstm50nuevo_precision, 'c', label='Train Precision: LSTM 50-ts')
plt.plot(test003_lstm50nuevo_val_precision, 'c--', label='Validation Precision: LSTM 50-ts')
plt.plot(test003_lstm100nuevo_precision, 'm', label='Train Precision: LSTM 100-ts')
plt.plot(test003_lstm100nuevo_val_precision, 'm--', label='Validation Precision: LSTM 100-ts')
plt.plot(test003_gru50nuevo_precision, 'y', label='Train Precision: GRU 50-ts')
plt.plot(test003_gru50nuevo_val_precision, 'y--', label='Validation Precision: GRU 50-ts')
plt.plot(test003_gru100nuevo_precision, 'k', label='Train Precision: GRU 100-ts')
plt.plot(test003_gru100nuevo_val_precision, 'k--', label='Validation Precision: GRU 100-ts')
plt.legend()


# Recall plot:
# Load data
test003_srnn50antiguo_recall = dm.load('history/test003/test003_train-recall_SimpleRNN-1-layer_50-timesteps_dataset1_clean.abc-dataset')
test003_srnn50nuevo_recall = dm.load('history/test003/test003_train-recall_SimpleRNN-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_srnn100nuevo_recall = dm.load('history/test003/test003_train-recall_SimpleRNN-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_lstm50nuevo_recall = dm.load('history/test003/test003_train-recall_LSTM-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_lstm100nuevo_recall = dm.load('history/test003/test003_train-recall_LSTM-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_gru50nuevo_recall = dm.load('history/test003/test003_train-recall_GRU-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_gru100nuevo_recall = dm.load('history/test003/test003_train-recall_GRU-1-layer_100-timesteps_archivo_salida_arreglado-dataset')

test003_srnn50antiguo_val_recall = dm.load('history/test003/test003_val-recall_SimpleRNN-1-layer_50-timesteps_dataset1_clean.abc-dataset')
test003_srnn50nuevo_val_recall = dm.load('history/test003/test003_val-recall_SimpleRNN-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_srnn100nuevo_val_recall = dm.load('history/test003/test003_val-recall_SimpleRNN-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_lstm50nuevo_val_recall = dm.load('history/test003/test003_val-recall_LSTM-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_lstm100nuevo_val_recall = dm.load('history/test003/test003_val-recall_LSTM-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_gru50nuevo_val_recall = dm.load('history/test003/test003_val-recall_GRU-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_gru100nuevo_val_recall = dm.load('history/test003/test003_val-recall_GRU-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
# Plot data
plt.subplot(132)
plt.axis([0,19,0,1])
plt.title('Recall')
plt.xlabel('epochs')
plt.ylabel('recall')
plt.grid(axis='y')
plt.xticks(np.arange(0,20,2))
plt.yticks(np.arange(0,1.05,0.05))
plt.plot(test003_srnn50antiguo_recall, 'b', label='Train Recall: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50antiguo_val_recall, 'b--', label='Validation Recall: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50nuevo_recall, 'g', label='Train Recall: SimpleRNN 50-ts')
plt.plot(test003_srnn50nuevo_val_recall, 'g--', label='Validation Recall: SimpleRNN 50-ts')
plt.plot(test003_srnn100nuevo_recall, 'r', label='Train Recall: SimpleRNN 100-ts')
plt.plot(test003_srnn100nuevo_val_recall, 'r--', label='Validation Recall: SimpleRNN 100-ts')
plt.plot(test003_lstm50nuevo_recall, 'c', label='Train Recall: LSTM 50-ts')
plt.plot(test003_lstm50nuevo_val_recall, 'c--', label='Validation Recall: LSTM 50-ts')
plt.plot(test003_lstm100nuevo_recall, 'm', label='Train Recall: LSTM 100-ts')
plt.plot(test003_lstm100nuevo_val_recall, 'm--', label='Validation Recall: LSTM 100-ts')
plt.plot(test003_gru50nuevo_recall, 'y', label='Train Recall: GRU 50-ts')
plt.plot(test003_gru50nuevo_val_recall, 'y--', label='Validation Recall: GRU 50-ts')
plt.plot(test003_gru100nuevo_recall, 'k', label='Train Recall: GRU 100-ts')
plt.plot(test003_gru100nuevo_val_recall, 'k--', label='Validation Recall: GRU 100-ts')
plt.legend()


# F-measure plot:
# Load data
test003_srnn50antiguo_f1 = dm.load('history/test003/test003_train-fscore_SimpleRNN-1-layer_50-timesteps_dataset1_clean.abc-dataset')
test003_srnn50nuevo_f1 = dm.load('history/test003/test003_train-fscore_SimpleRNN-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_srnn100nuevo_f1 = dm.load('history/test003/test003_train-fscore_SimpleRNN-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_lstm50nuevo_f1 = dm.load('history/test003/test003_train-fscore_LSTM-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_lstm100nuevo_f1 = dm.load('history/test003/test003_train-fscore_LSTM-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_gru50nuevo_f1 = dm.load('history/test003/test003_train-fscore_GRU-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_gru100nuevo_f1 = dm.load('history/test003/test003_train-fscore_GRU-1-layer_100-timesteps_archivo_salida_arreglado-dataset')

test003_srnn50antiguo_val_f1 = dm.load('history/test003/test003_val-fscore_SimpleRNN-1-layer_50-timesteps_dataset1_clean.abc-dataset')
test003_srnn50nuevo_val_f1 = dm.load('history/test003/test003_val-fscore_SimpleRNN-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_srnn100nuevo_val_f1 = dm.load('history/test003/test003_val-fscore_SimpleRNN-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_lstm50nuevo_val_f1 = dm.load('history/test003/test003_val-fscore_LSTM-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_lstm100nuevo_val_f1 = dm.load('history/test003/test003_val-fscore_LSTM-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
test003_gru50nuevo_val_f1 = dm.load('history/test003/test003_val-fscore_GRU-1-layer_50-timesteps_archivo_salida_arreglado-dataset')
test003_gru100nuevo_val_f1 = dm.load('history/test003/test003_val-fscore_GRU-1-layer_100-timesteps_archivo_salida_arreglado-dataset')
# Plot data
plt.subplot(133)
plt.axis([0,19,0,1])
plt.title('F-measure')
plt.xlabel('epochs')
plt.ylabel('f-measure')
plt.grid(axis='y')
plt.xticks(np.arange(0,20,2))
plt.yticks(np.arange(0,1.05,0.05))
plt.plot(test003_srnn50antiguo_f1, 'b', label='Train F-measure: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50antiguo_val_f1, 'b--', label='Validation F-measure: SimpleRNN 50-ts (antiguo)')
plt.plot(test003_srnn50nuevo_f1, 'g', label='Train F-measure: SimpleRNN 50-ts')
plt.plot(test003_srnn50nuevo_val_f1, 'g--', label='Validation F-measure: SimpleRNN 50-ts')
plt.plot(test003_srnn100nuevo_f1, 'r', label='Train F-measure: SimpleRNN 100-ts')
plt.plot(test003_srnn100nuevo_val_f1, 'r--', label='Validation F-measure: SimpleRNN 100-ts')
plt.plot(test003_lstm50nuevo_f1, 'c', label='Train F-measure: LSTM 50-ts')
plt.plot(test003_lstm50nuevo_val_f1, 'c--', label='Validation F-measure: LSTM 50-ts')
plt.plot(test003_lstm100nuevo_f1, 'm', label='Train F-measure: LSTM 100-ts')
plt.plot(test003_lstm100nuevo_val_f1, 'm--', label='Validation F-measure: LSTM 100-ts')
plt.plot(test003_gru50nuevo_f1, 'y', label='Train F-measure: GRU 50-ts')
plt.plot(test003_gru50nuevo_val_f1, 'y--', label='Validation F-measure: GRU 50-ts')
plt.plot(test003_gru100nuevo_f1, 'k', label='Train F-measure: GRU 100-ts')
plt.plot(test003_gru100nuevo_val_f1, 'k--', label='Validation F-measure: GRU 100-ts')
plt.legend()

plt.show()
