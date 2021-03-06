import datamanager as dm

history_dir = 'history/'

history1 = dm.load(history_dir + 'GRU256_GRU64_GRU512_BATCH32_EMBEDDING20')['history']
history2 = dm.load(history_dir + 'GRU256_GRU64_GRU512_BATCH32_EMBEDDING40')['history']
history3 = dm.load(history_dir + 'GRU256_GRU64_GRU512_BATCH32_EMBEDDING60')['history']
history4 = dm.load(history_dir + 'GRU256_GRU64_GRU512_BATCH32_EMBEDDING80')['history']
history5 = dm.load(history_dir + 'GRU256_GRU64_GRU512_BATCH32_EMBEDDING100')['history']

from matplotlib import pyplot as plt
import numpy as np

# Loss plot:
plt.subplot(121)
plt.axis([0,19,0,2.8])
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.grid(axis='x')
plt.grid(axis='y')
plt.xticks(np.arange(0,20,2))
plt.yticks(np.arange(0,2.9,0.2))

plt.plot(history1['loss'],      color='#000000', linestyle='-',  label='Train loss GRU(256)-GRU(64)-GRU(512) Embedding-20')
plt.plot(history1['val_loss'],  color='#000000', linestyle='--', label='Validation loss GRU(256)-GRU(64)-GRU(512) Embedding-20')
plt.plot(history2['loss'],      color='#0000ff', linestyle='-',  label='Train loss GRU(256)-GRU(64)-GRU(512) Embedding-40')
plt.plot(history2['val_loss'],  color='#0000ff', linestyle='--', label='Validation loss GRU(256)-GRU(64)-GRU(512) Embedding-40')
plt.plot(history3['loss'],      color='#00ff00', linestyle='-',  label='Train loss GRU(256)-GRU(64)-GRU(512) Embedding-60')
plt.plot(history3['val_loss'],  color='#00ff00', linestyle='--', label='Validation loss GRU(256)-GRU(64)-GRU(512) Embedding-60')
plt.plot(history4['loss'],      color='#00ffff', linestyle='-',  label='Train loss GRU(256)-GRU(64)-GRU(512) Embedding-80')
plt.plot(history4['val_loss'],  color='#00ffff', linestyle='--', label='Validation loss GRU(256)-GRU(64)-GRU(512) Embedding-80')
plt.plot(history5['loss'],      color='#ff0000', linestyle='-',  label='Train loss GRU(256)-GRU(64)-GRU(512) Embedding-100')
plt.plot(history5['val_loss'],  color='#ff0000', linestyle='--', label='Validation loss GRU(256)-GRU(64)-GRU(512) Embedding-100')

plt.legend()


# Accuracy plot:
plt.subplot(122)
plt.axis([0,19,0,1])
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.grid(axis='y')
plt.grid(axis='x')
plt.xticks(np.arange(0,20,2))
plt.yticks(np.arange(0,1.05,0.05))

plt.plot(history1['acc'],      color='#000000', linestyle='-',  label='Train accuracy GRU(256)-GRU(64)-GRU(512) Embedding-20')
plt.plot(history1['val_acc'],  color='#000000', linestyle='--', label='Validation accuracy GRU(256)-GRU(64)-GRU(512) Embedding-20')
plt.plot(history2['acc'],      color='#0000ff', linestyle='-',  label='Train accuracy GRU(256)-GRU(64)-GRU(512) Embedding-40')
plt.plot(history2['val_acc'],  color='#0000ff', linestyle='--', label='Validation accuracy GRU(256)-GRU(64)-GRU(512) Embedding-40')
plt.plot(history3['acc'],      color='#00ff00', linestyle='-',  label='Train accuracy GRU(256)-GRU(64)-GRU(512) Embedding-60')
plt.plot(history3['val_acc'],  color='#00ff00', linestyle='--', label='Validation accuracy GRU(256)-GRU(64)-GRU(512) Embedding-60')
plt.plot(history4['acc'],      color='#00ffff', linestyle='-',  label='Train accuracy GRU(256)-GRU(64)-GRU(512) Embedding-80')
plt.plot(history4['val_acc'],  color='#00ffff', linestyle='--', label='Validation accuracy GRU(256)-GRU(64)-GRU(512) Embedding-80')
plt.plot(history5['acc'],      color='#ff0000', linestyle='-',  label='Train accuracy GRU(256)-GRU(64)-GRU(512) Embedding-100')
plt.plot(history5['val_acc'],  color='#ff0000', linestyle='--', label='Validation accuracy GRU(256)-GRU(64)-GRU(512) Embedding-100')

plt.legend()

plt.show()
exit()
