#!/usr/bin/env python
# coding: utf-8

# University of Wollong (UOW)  
# CSCI991 Project Spring 2019  
# Team B  
# 
# <em>Peng TIAN, pt882@uowmail.edu.au</em>

# # Train a ResNet50 on RxRx1 using local GPU

# tf_upgrade_v2 --intree rxrx/ --outtree rxrx/ --copyotherfiles False
# 
# 
# <strong>References:</strong>
# <ol>
#     <li><a href='https://colab.research.google.com/github/recursionpharma/rxrx1-utils/blob/master/notebooks/training.ipynb'>https://colab.research.google.com/github/recursionpharma/rxrx1-utils/blob/master/notebooks/training.ipynb</a></li>
#     <li><a href='https://www.tensorflow.org/guide/migrate'>https://www.tensorflow.org/guide/migrate</a></li>
# </ol>

# In[1]:


import json
import os
import sys

import tensorflow as tf


# In[2]:


from rxrx.main import main


# In[3]:


MODEL_DIR = 'bucket'
URL_BASE_PATH = 'tfrecords\\random-42'  # windows
# URL_BASE_PATH = 'D:\\_peng\\recursion-cellular-image-classification-1.54 GB'  # windows
num_shards = 1 # 8  # colab uses Cloud TPU v2-8


# In[4]:

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

tf.logging.set_verbosity(tf.logging.INFO)


# In[5]:

# !!! ???
# Ref:
#     https://blog.csdn.net/sinat_36618660/article/details/99778070

main(use_tpu=False,  # True,
     tpu=None,  # tpu_grpc,
     gcp_project=None,
     tpu_zone=None,
     url_base_path=URL_BASE_PATH,
     use_cache=False,
     model_dir=MODEL_DIR,
     train_epochs=3000,
     train_batch_size=6,  # 8,   #  512,
     num_train_images=3000,  # 73030,
     epochs_per_loop=1,
     log_step_count_epochs=1,
     num_cores=num_shards,
     data_format='channels_last',  # main.py line 506, 'For GPU, channels_first will improve performance.'
     transpose_input=True, # assert not transpose_input  # channels_first only for GPU
     tf_precision='float32',  # 'bfloat16', #
     n_classes=1108,  # 1139
     momentum=0.9,
     weight_decay=1e-4,
     base_learning_rate=0.2,
     warmup_epochs=5)


# In[ ]:
