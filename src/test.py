import os
import pandas as pd


metadata_path = '../small_recursion-cellular-image-classification/metadata'

train = pd.read_csv(os.path.join(metadata_path, 'train.csv'))
for r in range(0, train.shape[0]):
    print(train.loc[r]['experiment'], train.loc[r]['well'])
