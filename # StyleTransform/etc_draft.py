# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 17:08:31 2018

@author: Franc
"""

import os
os.chdir('C:/Users/Franc/Desktop/Dir/Competitions/#Kaggle/#Salt')
         
import sys
sys.path.append('code')

import pandas as pd

import pickle
from pathlib import Path
#from glob import glob

def generate_metadata():
    train_ids = [os.path.splitext(x)[0] for x in os.listdir('data/train/images')]
    test_ids = [os.path.splitext(x)[0] for x in os.listdir('data/test/images')]
    meta_data = pd.DataFrame({'id':train_ids+test_ids,
                              'is_train':[1]*len(train_ids)+[0]*len(test_ids)})
    
    meta_depth = pd.read_csv('data/depths.csv')
    meta_data = meta_data.merge(meta_depth, on=['id'], how = 'left')
    
    meta_mask = pd.read_csv('data/train.csv')
    meta_data = meta_data.merge(meta_mask, on=['id'], how = 'left').\
        sort_values(['is_train','id']).reset_index(drop=True)

    meta_data['path_img'] = \
        sorted(Path('data/test/images').glob('*.png')) + \
        sorted(Path('data/train/images').glob('*.png'))
    meta_data['path_msk'] = \
        [None]*len(test_ids) + \
        sorted(Path('data/train/masks').glob('*.png'))
    return meta_data

def from_pickle(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj

def to_pickle(filename, obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, -1)

#@ipy.interact(idx = ipy.IntSlider(min=0,max=len(train_img_paths)),value=10,step=1)
#def plot(idx):
#    img = Image.open(train_img_paths[idx])
#    mask = Image.open(train_msk_paths[idx])
#    fig, axs = plt.subplots(1,2, figsize=(6,3))
#    axs[0].imshow(img)
#    axs[1].imshow(mask)
#    plt.show()  

#def mean_iou(y_true, y_pred):
#    prec = []
#    for t in np.arange(0.5, 1.0, 0.05):
#        y_pred_ = tf.to_int32(y_pred > t)
#        score, up_opt = tf.metrics.mean_iou(y_true, y_pred_, 2)
#        K.get_session().run(tf.local_variables_initializer())
#        with tf.control_dependencies([up_opt]):
#            score = tf.identity(score)
#        prec.append(score)
#    return K.mean(K.stack(prec), axis=0)


