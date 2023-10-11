import cv2
import os
import numpy as np
from random import shuffle
from tqdm import tqdm


array_grande =[[ 95, 104, 123, ..., 131, 137, 106],
       [ 96, 105, 130, ..., 132, 122, 104],
       [ 96, 102, 110, ..., 130, 119, 104],
       [ 60,  72,  80, ..., 104, 113, 122],
       [ 47,  59,  82, ...,  63,  85,  95],
       [ 43,  47,  58, ..., 117,  38,  55]]

array_pequeno = [1, 0]

array_final = []

array_transicao = np.concatenate((array_grande,array_pequeno))

array_final.append(array_transicao)

np.save('train_data.npy', array_final)
