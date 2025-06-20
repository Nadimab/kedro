"""
This is a boilerplate pipeline 'siamese'
generated using Kedro 0.18.1
"""
from typing import Callable, Dict
import sys
import numpy as np
import pandas as pd
#from scipy.misc import imread
import pickle
import os
import matplotlib.pyplot as plt

import cv2
import time

import tensorflow as tf
from keras.models import Sequential
#from keras.optimizers import Adam
from tensorflow.keras.optimizers import Adam
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model

#from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform

#from keras.engine.topology import Layer
from keras.regularizers import l2
from keras import backend as K

from sklearn.utils import shuffle

import numpy.random as rng

def data_preparation(validated_json_dataset):
    return validated_json_dataset


def siamese_network_fun(trajectory_dataset: Dict[str, Callable]) -> Dict[str,Callable]:   
    return trajectory_dataset

def clustering_siamese(siamese_matrix):
    return siamese_matrix