import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np

def load_data(weights_directory):
    files = os.listdir(weights_directory)
    files = sorted(files)

    dic = {}

    for f in files:
        if not f.endswith(".hdf5"):
            continue


        [_,_,_,_,padding,_,units,_,_,_,_,batch,epoch,loss,acc,vLoss,vAcc] = f.split("_")
        lossname = "SimpleRNN_1-layer_"+units+"_"+batch+"_tLoss"
        accname = "SimpleRNN_1-layer_"+units+"_"+batch+"_tAccu"
        vLossname = "SimpleRNN_1-layer_"+units+"_"+batch+"_vLoss"
        vAccname = "SimpleRNN_1-layer_"+units+"_"+batch+"_vAccu"

        if not lossname in dic.keys():
            dic[lossname] = []
        if not accname in dic.keys():
            dic[accname] = []
        if not vLossname in dic.keys():
            dic[vLossname] = []
        if not vAccname in dic.keys():
            dic[vAccname] = []

        dic[lossname].append([epoch,loss])
        dic[accname].append([epoch,acc])
        dic[vLossname].append([epoch,vLoss])
        dic[vAccname].append([epoch,vAcc[:-5]])

    return dic


def plot_data(dic, dest):
    keys = []
    for k in sorted(dic.keys()):
        keys.append(k[:-6])

    keys = sorted(list(set(keys)))

    subplots = len(keys)
    for i in range(subplots):
        plt.subplot(1,2,1)
        plt.axis([0,100,1.5,3.0])
        plt.xticks(np.arange(0,105,5))
        plt.yticks(np.arange(1.5,3.1,0.1))
        plt.grid(axis='y')
        plt.title(keys[i]+" loss")
        plt.xlabel("epoch")
        plt.ylabel("loss")
        tLoss = np.array(dic[keys[i]+"_tLoss"]).T
        vLoss = np.array(dic[keys[i]+"_vLoss"]).T
        plt.plot(tLoss[0],tLoss[1], 'r', label="Train Loss")
        plt.plot(vLoss[0],vLoss[1], 'r--', label="Validation Loss")
        plt.legend()
        
        plt.subplot(1,2,2)
        plt.axis([0,100,0,1])
        plt.xticks(np.arange(0,105,5))
        plt.yticks(np.arange(0,1.05,0.05))
        plt.grid(axis='y')
        plt.title(keys[i]+" accuracy")
        plt.xlabel("epoch")
        plt.ylabel("accuracy")
        tAccu = np.array(dic[keys[i]+"_tAccu"]).T
        vAccu = np.array(dic[keys[i]+"_vAccu"]).T
        plt.plot(tAccu[0], tAccu[1], 'g', label="Train Accuracy")
        plt.plot(vAccu[0], vAccu[1], 'g--', label="Validation Accuracy")
        plt.legend()
        if dest != None:
            plt.savefig(os.path.join(dest,keys[i]+".png"), bbox_inches='tight')
        plt.show()

    plt.show()
