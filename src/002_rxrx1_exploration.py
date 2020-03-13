#!/usr/bin/env python
# coding: utf-8

# University of Wollong (UOW)  
# CSCI991 Project Spring 2019  
# Team B  
# 
# <em>Peng TIAN, pt882@uowmail.edu.au</em>

# # Explore RxRx1 Dataset
# 
# <br/>
# <br/>
# 
# <a href='https://www.kaggle.com/c/recursion-cellular-image-classification/'>Recursion Cellular Image Classification</a> is a competition on kaggle<sup>[1]</sup>. The <a href='https://www.kaggle.com/c/recursion-cellular-image-classification/data'>RxRx1 dataset</a> can be downloarded from kaggle <sup>[3]</sup>. More information about the biology of this dataset is provided by <a href='https://www.rxrx.ai/'>RXRX.AI</a><sup>[2]</sup>.
# 
# There are 4 types of cell - HUVEC,RPE,HEPG2 and U2OS.
# 
# For every type of cell, there are several experiments which are separate into train dataset and test dataset.
# 
# For each experiments, 4 384-well plate <sup>[5]</sup> (A-P × 1-24) is used. However, the wells which on the border are abandoned - i.e. just resarching B02 to O23 (B-O × 2-23 = 308). For each well, 2 6-channel image sites are released. 3 types of well are positive_control, negative_control and treatment.
# 
# Each channel is a 512×512 gray image. Each well has 6-channel × 2-sites = 12 images.
# 
# For train dataset, the values of sirna are given. For test dataset, the values of sirna are NaN which need to be predicted.
# 
# <br/>
# <br/>
# 
# <strong>Biboliagraph:</strong>
# <ol>
#     <li><a href='https://www.kaggle.com/c/recursion-cellular-image-classification/'>https://www.kaggle.com/c/recursion-cellular-image-classification</a></li>
#     <li><a href='https://www.rxrx.ai/'>https://www.rxrx.ai</a></li>
#     <li><a href='https://www.kaggle.com/c/recursion-cellular-image-classification/data'>https://www.kaggle.com/c/recursion-cellular-image-classification/data</a></li>
#     <li><a href='https://colab.research.google.com/github/recursionpharma/rxrx1-utils/blob/master/notebooks/visualization.ipynb'>https://colab.research.google.com/github/recursionpharma/rxrx1-utils/blob/master/notebooks/visualization.ipynb</a></li>
#     <li><a href='https://en.wikipedia.org/wiki/Microplate'>https://en.wikipedia.org/wiki/Microplate</a></li>
# </ol>

# In[1]:


import sys
import os
import numpy as np
import pandas as pd
from pandas import DataFrame

import matplotlib.pyplot as plt

# get_ipython().run_line_magic('matplotlib', 'inline')  # just for jupyter notebook


# In[2]:


import rxrx.io as rio


# In[3]:


# Ref:
#     rxrx/io.py, line: 14, 15

LOCAL_IMAGES_BASE_PATH = 'D:\\_peng\\recursion-cellular-image-classification'  # windows
DEFAULT_METADATA_BASE_PATH = LOCAL_IMAGES_BASE_PATH


# In[4]:


# train.csv, train_controls.csv, test.csv, test_controls.csv

md = rio.combine_metadata(base_path=DEFAULT_METADATA_BASE_PATH)


# In[5]:


md.info


# In[6]:


md.head()


# <strong>Cell Type</strong>

# In[7]:


md['cell_type'].value_counts()


# <strong>Experiments for training and testing</strong>

# In[8]:


md[md['sirna'].notnull()]['cell_type'].value_counts()  #  train dataset has value of sirna


# In[9]:


md[md['sirna'].isnull()]['cell_type'].value_counts()  # test dataset


# <strong>Plate</strong>

# In[10]:


md['plate'].value_counts()


# <strong>Well</strong>

# In[11]:


DataFrame(md['well'].value_counts()).sort_index()


# <strong>Site</strong>

# In[12]:


md['site'].value_counts()


# <strong>Image</strong>

# In[13]:


# pixel_stats.csv
# row 1-6
# train set, experiment HEPG2-01, plate 1, well B02, site 1

t = rio.load_site('train', 'HEPG2-01', 1, 'B02', 1, base_path=LOCAL_IMAGES_BASE_PATH)

t.shape


# In[14]:


img = t[:, :, 0]  # channel 1

img.shape


# In[15]:


plt.figure(figsize=(8, 8))
plt.axis('off')

_ = plt.imshow(img, cmap='gray')


# In[16]:


print('mean\t\t', 'std\t\t', 'median\t', 'min\t', 'max')
print('{0:.8f} \t {1:.8f} \t {2:.1f} \t {3:d} \t {4:d}'.format(np.mean(img),
                                                               np.std(img), np.median(img), np.min(img), np.max(img)))


# <em>Pixel statistics are provied in  pixel_stats.csv :</em>

# In[17]:


# pixel_stats.csv

df_pixel_stats = pd.read_csv(os.path.join(DEFAULT_METADATA_BASE_PATH, 'pixel_stats.csv'))

df_pixel_stats.head(n=12)


# <strong>Train dataset and test dataset</strong>

# In[18]:


md_train = md[md['sirna'].notnull()]


# In[19]:


md_train


# In[20]:


md_test = md[md['sirna'].isnull()]


# In[21]:


md_test


# In[22]:


DataFrame(md_train['experiment'].value_counts()).sort_index()


# In[23]:


DataFrame(md_test['experiment'].value_counts()).sort_index()


# <em id='training_testing'>Summary of train dataset and test dataset in aspect of experiments:</em>
# 
# |cell |train|test|
# |----:|:--:|:--:|
# |HEPG |HEPG2-01 ... HEPG2-11|HEPG2-08 ... HEPG2-11|
# |HUVEC|HUVEC-01 ... HUVEC-24|HUVEC-11 ... HUVEC-24|
# |RPE  |RPE-01 ... RPE-11|RPE-08 ... RPE-11|
# |U2OS |U2OS-01 ... U2OS-05|U2OS-04 ... U2OS-05|

# In[ ]:




