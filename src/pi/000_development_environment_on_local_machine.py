"""
CSCI991 Project Spring 2019, UOW
Team B
pt882@uowmail.edu.au
"""

import os
import platform
import pprint
import subprocess
import sys
import warnings


# ... this TensorFlow binary was not compiled to use: AVX2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# FutureWarning ... in a future version of numpy ...
warnings.filterwarnings('ignore', category=FutureWarning)


import tensorflow as tf
from tensorflow import keras
from tensorflow.python.client import device_lib


print(sys.version)
print(platform.system(), platform.release(), platform.architecture()[0], platform.version())
print(platform.platform())

if platform.system() == 'Windows':
    print(platform.processor())
    print(subprocess.check_output(["wmic", "cpu", "get", "name"]).decode().strip().split('\n')[1])

if platform.system() == 'Windows':
    process = os.popen('wmic memorychip get capacity')
    result = process.read()
    process.close()
    memory = 0
    for m in result.split("  \n\n")[1:-1]:
        memory += int(m)
    print(memory / (1024 ** 3), 'GB')

print(tf.__version__)
print(keras.__version__)
pprint.pprint(device_lib.list_local_devices())
