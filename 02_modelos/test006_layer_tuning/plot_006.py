import datamanager as dm

history_dir = 'history_GRU-128-tanh_rmsprop_128-batch_25-epochs/'

history1 = dm.load(history_dir + '1-layer_test006_loss_acc')
history2 = dm.load(history_dir + '2-layer_test006_loss_acc')
history3 = dm.load(history_dir + '3-layer_test006_loss_acc')
history4 = dm.load(history_dir + '4-layer_test006_loss_acc')
history5 = dm.load(history_dir + '5-layer_test006_loss_acc')
history6 = dm.load(history_dir + '6-layer_test006_loss_acc')
history7 = dm.load(history_dir + '7-layer_test006_loss_acc')
history8 = dm.load(history_dir + '8-layer_test006_loss_acc')
history9 = dm.load(history_dir + '9-layer_test006_loss_acc')
history10 = dm.load(history_dir + '10-layer_test006_loss_acc')

from matplotlib import pyplot as plt
import numpy as np

# Loss plot:
plt.subplot(221)
plt.axis([0,24,0,2.8])
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.grid(axis='y')
plt.xticks(np.arange(0,25,2))
plt.yticks(np.arange(0,2.9,0.2))

plt.plot(history1['loss'],      color='#000000', linestyle='-',  label='Train Loss: 1 GRU layer')
plt.plot(history1['val_loss'],  color='#000000', linestyle='--', label='Validation Loss: 1 GRU layer')
plt.plot(history2['loss'],      color='#0000ff', linestyle='-',  label='Train Loss: 2 GRU layer')
plt.plot(history2['val_loss'],  color='#0000ff', linestyle='--', label='Validation Loss: 2 GRU layer')
plt.plot(history3['loss'],      color='#00ff00', linestyle='-',  label='Train Loss: 3 GRU layer')
plt.plot(history3['val_loss'],  color='#00ff00', linestyle='--', label='Validation Loss: 3 GRU layer')
plt.plot(history4['loss'],      color='#00ffff', linestyle='-',  label='Train Loss: 4 GRU layer')
plt.plot(history4['val_loss'],  color='#00ffff', linestyle='--', label='Validation Loss: 4 GRU layer')
plt.plot(history5['loss'],      color='#ff0000', linestyle='-',  label='Train Loss: 5 GRU layer')
plt.plot(history5['val_loss'],  color='#ff0000', linestyle='--', label='Validation Loss: 5 GRU layer')

plt.legend()


plt.subplot(223)
plt.axis([0,24,0,2.8])
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.grid(axis='y')
plt.xticks(np.arange(0,25,2))
plt.yticks(np.arange(0,2.9,0.2))

plt.plot(history6['loss'],      color='#ff00ff', linestyle='-',  label='Train Loss: 6 GRU layer')
plt.plot(history6['val_loss'],  color='#ff00ff', linestyle='--', label='Validation Loss: 6 GRU layer')
plt.plot(history7['loss'],      color='#ffff00', linestyle='-',  label='Train Loss: 7 GRU layer')
plt.plot(history7['val_loss'],  color='#ffff00', linestyle='--', label='Validation Loss: 7 GRU layer')
plt.plot(history8['loss'],      color='#bbbbbb', linestyle='-',  label='Train Loss: 8 GRU layer')
plt.plot(history8['val_loss'],  color='#bbbbbb', linestyle='--', label='Validation Loss: 8 GRU layer')
plt.plot(history9['loss'],      color='#4488cc', linestyle='-',  label='Train Loss: 9 GRU layer')
plt.plot(history9['val_loss'],  color='#4488cc', linestyle='--', label='Validation Loss: 9 GRU layer')
plt.plot(history10['loss'],     color='#cc8844', linestyle='-',  label='Train Loss: 10 GRU layer')
plt.plot(history10['val_loss'], color='#cc8844', linestyle='--', label='Validation Loss: 10 GRU layer')

plt.legend()


# Accuracy plot:
plt.subplot(222)
plt.axis([0,24,0,1])
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.grid(axis='y')
plt.xticks(np.arange(0,25,2))
plt.yticks(np.arange(0,1.05,0.05))

plt.plot(history1['acc'],      color='#000000', linestyle='-',  label='Train Accuracy: 1 GRU layer')
plt.plot(history1['val_acc'],  color='#000000', linestyle='--', label='Validation Accuracy: 1 GRU layer')
plt.plot(history2['acc'],      color='#0000ff', linestyle='-',  label='Train Accuracy: 2 GRU layer')
plt.plot(history2['val_acc'],  color='#0000ff', linestyle='--', label='Validation Accuracy: 2 GRU layer')
plt.plot(history3['acc'],      color='#00ff00', linestyle='-',  label='Train Accuracy: 3 GRU layer')
plt.plot(history3['val_acc'],  color='#00ff00', linestyle='--', label='Validation Accuracy: 3 GRU layer')
plt.plot(history4['acc'],      color='#00ffff', linestyle='-',  label='Train Accuracy: 4 GRU layer')
plt.plot(history4['val_acc'],  color='#00ffff', linestyle='--', label='Validation Accuracy: 4 GRU layer')
plt.plot(history5['acc'],      color='#ff0000', linestyle='-',  label='Train Accuracy: 5 GRU layer')
plt.plot(history5['val_acc'],  color='#ff0000', linestyle='--', label='Validation Accuracy: 5 GRU layer')

plt.legend()


plt.subplot(224)
plt.axis([0,24,0,1])
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.grid(axis='y')
plt.xticks(np.arange(0,25,2))
plt.yticks(np.arange(0,1.05,0.05))
plt.plot(history6['acc'],      color='#ff00ff', linestyle='-',  label='Train Accuracy: 6 GRU layer')
plt.plot(history6['val_acc'],  color='#ff00ff', linestyle='--', label='Validation Accuracy: 6 GRU layer')
plt.plot(history7['acc'],      color='#ffff00', linestyle='-',  label='Train Accuracy: 7 GRU layer')
plt.plot(history7['val_acc'],  color='#ffff00', linestyle='--', label='Validation Acurracy: 7 GRU layer')
plt.plot(history8['acc'],      color='#bbbbbb', linestyle='-',  label='Train Accuracy: 8 GRU layer')
plt.plot(history8['val_acc'],  color='#bbbbbb', linestyle='--', label='Validation Accuracy: 8 GRU layer')
plt.plot(history9['acc'],      color='#4488cc', linestyle='-',  label='Train Accuracy: 9 GRU layer')
plt.plot(history9['val_acc'],  color='#4488cc', linestyle='--', label='Validation Accuracy: 9 GRU layer')
plt.plot(history10['acc'],     color='#cc8844', linestyle='-',  label='Train Accuracy: 10 GRU layer')
plt.plot(history10['val_acc'], color='#cc8844', linestyle='--', label='Validation Accuracy: 10 GRU layer')

plt.legend()

plt.show()
exit()
