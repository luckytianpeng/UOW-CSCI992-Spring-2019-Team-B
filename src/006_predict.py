# Peng TIAN
# 2020-05-08

import json
import os
import sys
import pprint
import warnings

# Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# warnings.filterwarnings("ignore")


import pandas as pd
import numpy as np
import tensorflow as tf
# WARNING:tensorflow: ... is deprecated and will be removed in a future version.
# import tensorflow.python.util.deprecation as deprecation
# deprecation._PRINT_DEPRECATION_WARNINGS = False


from tensorflow.contrib import predictor


# sys.path.append('../')
import rxrx.io as rio


metadata_path = '../small_recursion-cellular-image-classification/metadata'
image_path = '../small_recursion-cellular-image-classification/images'
# Ref:
#   https://stackoverflow.com/questions/46098863/how-to-import-an-saved-tensorflow-model-train-using-tf-estimator-and-predict-on
pred = predictor.from_saved_model('D:/_20200313_/_peng/PycharmProjects/csci992/bucket/saved_model/1584067643')  # ('bucket/saved_model/1589202794')

# t = t.astype('float32')
# t = t*(1.0/255.0)

stat = {}

train = pd.read_csv(os.path.join(metadata_path, 'train.csv'))
for r in range(0, train.shape[0]):
    # t = rio.load_site('train', 'HEPG2-01', 1, 'B05', 1, base_path='../small_recursion-cellular-image-classification/images')  # main.py, line 391,
    t = rio.load_site('train', train.loc[r]['experiment'], 1, train.loc[r]['well'], 1, base_path=image_path)
    # t = np.ones((1, 512 * 512 * 6))  # np.zeros((1, 512 * 512 * 6))
    # t = t.reshape(512, 512, 6)
    # print(t.dtype)
    # t = t.astype('float32')
    # print(t.dtype)
    # t = t*(1.0/255.0)
    tt = np.expand_dims(t, axis=0)  ## np.array(t).reshape(1, 512, 512, 6)  #
    predictions = pred({'feature': tt})
    # pprint.pprint(predictions)
    print(train.loc[r]['experiment'], ',',
          1, ',',
          train.loc[r]['well'], ',',
          1, ',',
          train.loc[r]['sirna'], ',',
          predictions['classes'][0])
    stat[predictions['classes'][0]] = stat.get(predictions['classes'][0], 0) + 1

print(stat)
#
# https://stackoverflow.com/questions/41488279/neural-network-always-predicts-the-same-class
# https://github.com/keras-team/keras/issues/2975
#     yanaxu333 commented on Oct 3, 2018:
#         In my case, the reason why I get the same output class is that I did set epoch=1.
#         when change epoch to 10 or more, it works
