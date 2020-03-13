#!/usr/bin/env python
# coding: utf-8

# University of Wollong (UOW)  
# CSCI991 Project Spring 2019  
# Team B  
# 
# <em>Peng TIAN, pt882@uowmail.edu.au</em>

# # Visualize images in RxRx1
# 
# 
# <em>This code is based on visualization.ipynb<sup>[1]</sup>. Visualization.ipynb uses <strong>TPU</strong> via <strong>google colab</strong> whereas this code uses local <strong>GPU</strong>.  
# 
# The aim of this code is to ensure that <a href='https://github.com/recursionpharma/rxrx1-utils'>rxrx1-utils</a> can perform in <a href='000_development_environment_on_local_machine.ipynb'>local development environment</a>.
# </em>
#   
# 
# <strong>Reference:</strong>
# <ol>
#     <li><a hrefd='https://colab.research.google.com/github/recursionpharma/rxrx1-utils/blob/master/notebooks/visualization.ipynb'>https://colab.research.google.com/github/recursionpharma/rxrx1-utils/blob/master/notebooks/visualization.ipynb</a>
# </ol>
# 

# In[1]:


import sys
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


# train set, experiment RPE-05, plate 3, well D19, site 2

t = rio.load_site('train', 'RPE-05', 3, 'D19', 2, base_path=LOCAL_IMAGES_BASE_PATH)

t.shape


# In[5]:


fig, axes = plt.subplots(2, 3, figsize=(24, 16))

for i, ax in enumerate(axes.flatten()):
    ax.axis('off')
    ax.set_title('channel {}'.format(i + 1))
    _ = ax.imshow(t[:, :, i], cmap='gray')


# In[6]:


x = rio.convert_tensor_to_rgb(t)

x.shape


# In[7]:


plt.figure(figsize=(8, 8))
plt.axis('off')

_ = plt.imshow(x)


# In[8]:


y = rio.load_site_as_rgb('train', 'HUVEC-08', 4, 'K09', 1, base_path=LOCAL_IMAGES_BASE_PATH)

plt.figure(figsize=(8, 8))
plt.axis('off')

_ = plt.imshow(y)


# In[9]:


# train.csv, train_controls.csv, test.csv, test_controls.csv

md = rio.combine_metadata(base_path=DEFAULT_METADATA_BASE_PATH)

md.head()


# In[ ]:




