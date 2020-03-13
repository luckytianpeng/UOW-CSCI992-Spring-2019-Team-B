#!/usr/bin/env python
# coding: utf-8

# University of Wollong (UOW)  
# CSCI991 Project Spring 2019  
# Team B  
# 
# <em>Peng TIAN, pt882@uowmail.edu.au</em>

# # Split the original train data set to new train and new test data set
# 
# <strong>Why?</strong>
# 
# <em>We do not have the labels for test dataset. We need labels for <strong>validation and testing</strong> of our model.</em>
# <br/>
# <br/>
# <br/>

# According to <a href='002_rxrx1_exploration.ipynb#training_testing'>002_rxrx1_exploration.ipynb</a><sup>[1]</sup>:
# 
# <em>Original train and test date set:</em>
# 
# |cell |train|test|
# |----:|:--:|:--:|
# |HEPG |HEPG2-01 ... HEPG2-11|HEPG2-08 ... HEPG2-11|
# |HUVEC|HUVEC-01 ... HUVEC-24|HUVEC-11 ... HUVEC-24|
# |RPE  |RPE-01 ... RPE-11|RPE-08 ... RPE-11|
# |U2OS |U2OS-01 ... U2OS-05|U2OS-04 ... U2OS-05|
# 
# <strong>Spliting strategy:</strong>
# 
# |cell |train|test|
# |----:|:--:|:--:|
# |HEPG |HEPG2-01 ... HEPG2-05|HEPG2-06, HEPG2-07|
# |HUVEC|HUVEC-01 ... HUVEC-07|HUVEC-08 ... HUVEC-10|
# |RPE  |RPE-01 ... RPE-05|RPE-06, RPE-07|
# |U2OS |U2OS-01, U2OS-02|U2OS-03|
#          
#          
# <strong>References:</strong>
# 
# <ol>
#     <li><a href='002_rxrx1_exploration.ipynb'>002_rxrx1_exploration.ipynb</a></li>
# </ol>

# In[1]:


import sys
import os
import pandas as pd


# In[2]:


import rxrx.io as rio


# In[3]:


TRAIN = ['HEPG2-01', 'HEPG2-02', 'HEPG2-03', 'HEPG2-04', 'HEPG2-05',
         'HUVEC-01', 'HUVEC-02', 'HUVEC-03', 'HUVEC-04', 'HUVEC-05', 'HUVEC-06', 'HUVEC-07',
         'RPE-01', 'RPE-02', 'RPE-03', 'RPE-04', 'RPE-05',
         'U2OS-01', 'U2OS-02']


# In[4]:


# Ref:
#     rxrx/io.py, line: 14, 15

LOCAL_IMAGES_BASE_PATH = 'D:\\_peng\\recursion-cellular-image-classification'  # windows
DEFAULT_METADATA_BASE_PATH = LOCAL_IMAGES_BASE_PATH


# <strong>sample_submission.csv</strong>

# In[5]:


df_sample_submission = pd.read_csv(os.path.join(DEFAULT_METADATA_BASE_PATH, 'sample_submission.csv'))


# In[6]:


df_sample_submission.head()


# <strong>Combining competition metadata</strong>

# In[7]:


# train.csv, train_controls.csv, test.csv, test_controls.csv

md = rio.combine_metadata(base_path=DEFAULT_METADATA_BASE_PATH)


# In[8]:


md.head(n=6)


# <br/>
# <br/>
# <br/>
# <em>Summary of sample_submission.csv and combing metadata:</em>
# <ul>
#     <li>id_code: experiment_plate_well</li>
#     <li>Every well has 2 sites, every site has 6 channels. The 12 images be considered as a whole</li>
# </ul>
# <br/>
# <br/>
# <br/>

# <strong>Split original train to new train and new test (md_new.csv)</strong>

# In[9]:


md_train = md['train' == md['dataset']]

md_train.head()


# In[10]:


# just keep the 1st site

md_train_reduced = md_train[1 == md_train['site']].drop(columns='site')

md_train_reduced


# In[11]:


md_new = md_train_reduced.copy()

def train_test(df):
    if df['experiment'] in TRAIN:
        return 'train'
    else:
        return 'test'

md_new['dataset'] = md_new.apply(lambda x: train_test(x), axis=1)


# In[12]:


md_new


# In[13]:


md_new['dataset'].value_counts()


# In[14]:


md_new.to_csv(os.path.join('./', 'md_new.csv'), index=False, header=True)


md_new_train = md_new['train' == md_new['dataset']]
md_new_test = md_new['test' == md_new['dataset']]
md_new_train.to_csv(os.path.join('./', 'md_new_train.csv'), index=False, header=True)
md_new_test.to_csv(os.path.join('./', 'md_new_test.csv'), index=False, header=True)
