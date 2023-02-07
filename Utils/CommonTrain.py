import matplotlib.pyplot as plt
import numpy as np

def save_loss(key, history, file_name):
    plt.figure()
    plt.plot(history.history['val_loss'], 'r', label='Val Loss')
    plt.plot(history.history['loss'], 'b', label='Loss')
    plt.title('loss_'+key)
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.savefig(file_name)
    return plt

def save_accuracy(key, history, file_name):
    plt.figure()
    plt.plot(history.history['val_accuracy'], 'r', label='Val Accuracy')
    plt.plot(history.history['accuracy'], 'b', label='Accuracy')
    plt.title('accuracy_'+key)
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.savefig(file_name)
    return plt

from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn import metrics
def save_roc(key, df_val, df_tr, x_train, selected_columns, file_name):
    #### get the ROC curves
    fpr = {}
    tpr = {}
    auc1 = {}
    plt.figure(figsize=(10,10))

    fpr, tpr, threshold = roc_curve(df_tr['y_train'], df_tr['train_predict'], sample_weight=df_tr['w_train_raw'])
    # bug? hotfix
    sorted_index = np.argsort(fpr)
    fpr = np.array(fpr)[sorted_index]
    auc1 = metrics.auc(fpr, tpr)
    plt.plot(tpr,fpr,label='train, auc = %.1f%%'%(auc1*100.))
    
    fpr1, tpr1, threshold = roc_curve(df_val['y_test'], df_val['test_predict'], sample_weight=df_val['w_test_raw'])
    # bug? hotfix
    sorted_index = np.argsort(fpr1)
    fpr1 = np.array(fpr1)[sorted_index]
    auc2 = metrics.auc(fpr1, tpr1)
    plt.plot(tpr1,fpr1,label='test, auc = %.1f%%'%(auc2*100.))
    
    # variables' roc
    for i in range(8):
        fpr2, tpr2, threshold = roc_curve(df_tr['y_train'], x_train[:,i], sample_weight=df_tr['w_train_raw'])
        # bug? hotfix
        sorted_index = np.argsort(fpr2)
        fpr2 = np.array(fpr2)[sorted_index]
        auc3 = metrics.auc(fpr2, tpr2)
        plt.plot(tpr2,fpr2,label=selected_columns[i].replace('_pre', '')+', auc = %.1f%%'%(auc3*100.))
    
    plt.semilogy()
    plt.title('roc_'+key, fontsize=18)
    plt.xlabel('Signal Efficiency', fontsize=18)
    plt.ylabel('Background Efficiency', fontsize=18)
    plt.ylim(0.0001,1)
    plt.grid(True)
    plt.legend(loc='lower right', prop={'size': 15})
    plt.savefig(file_name)
    
    
    return plt, tpr, fpr, auc1, tpr1, fpr1, auc2

from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn import metrics
def dump_roc(key, y, predict, dic_predict_sort, sample_weight=None, channel='', version=''):
    #### get the ROC curves
    fpr = {}
    tpr = {}
    auc1 = {}
    plt.figure(figsize=(10,10))

    fpr, tpr, threshold = roc_curve(y[:,0], predict[:,dic_predict_sort['TT'].columns.get_loc('score')], sample_weight=predict[:,dic_predict_sort['TT'].columns.get_loc('weight')])
    # bug? hotfix
    sorted_index = np.argsort(fpr)
    fpr = np.array(fpr)[sorted_index]
    auc1 = metrics.auc(fpr, tpr)
    plt.plot(tpr,fpr,label='train, auc = %.1f%%'%(auc1*100.))
    
    return tpr, fpr, auc1    