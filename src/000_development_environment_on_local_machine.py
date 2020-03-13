#!/usr/bin/env python
# coding: utf-8

# University of Wollong (UOW)  
# CSCI991 Project Spring 2019  
# Team B  
# 
# <em>Peng TIAN, pt882@uowmail.edu.au</em>

# # Development Environment on Loacl Machine

# ## Software

# <strong>Python</strong>

# In[1]:


import sys

sys.version


# <strong>Operating System</strong>

# In[2]:


import platform


# In[3]:


print(platform.system(), platform.release(), platform.architecture()[0], platform.version())
print(platform.platform())


# ## Hardware

# In[4]:


import os, subprocess


# <strong>CPU</strong>

# In[5]:


if platform.system() == 'Windows':
    print(platform.processor())
    print(subprocess.check_output(["wmic","cpu","get", "name"]).decode().strip().split('\n')[1])


# <strong>Memory</strong>

# In[6]:


if platform.system() == 'Windows':
    process = os.popen('wmic memorychip get capacity')
    result = process.read()
    process.close()
    memory = 0
    for m in result.split("  \n\n")[1:-1]:
         memory += int(m)
    print( memory / (1024**3), 'GB')


# ## Tensorflow

# In[7]:


import tensorflow as tf
from tensorflow import keras


# <strong>tensorfolow version</strong>

# In[8]:


tf.__version__


# <strong>keras version</strong>

# In[9]:


keras.__version__


# <strong>devices</strong>

# In[10]:


from tensorflow.python.client import device_lib


# In[11]:


device_lib.list_local_devices()


# In[ ]:




