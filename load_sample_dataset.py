"""
 Functions to load images and their labels,
 feature vectors from the sample folder

 Date: 18th February, 18
"""

import numpy as np
import pandas as pd
from skimage.feature import hog
from skimage import io
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import os
import warnings
warnings.filterwarnings('ignore')


def read_images_from_dir(directory='./sample/processed'):
    """
    Read .jpeg images from a given directory path along with associated labels
    :param directory: The directory with the images to be loaded
    :return: List of numpy.ndarray images
    """
    images = []

    data = pd.read_csv('./trainLabels.csv')

    for file in os.listdir(directory):
        if file.endswith('.jpeg'):
            img = io.imread('{}/{}'.format(directory, file))

            name, ext = file.split('.')
            label = data[data.image == name].values[0][
                1]  # FIXME Better way to do this?

            images.append((img, label))

    return images


def calculate_features(images):
    """
    Calculate HOG features of a list of images generated by
    'read_images_from_dir()'
    :param images: list of images
    :return: numpy array of the feature vectors
    """

    features_list = []
    labels_list = []

    for img, label in images:
        features = hog(
            img,
            orientations=8,
            pixels_per_cell=(16, 16),
            cells_per_block=(1, 1))
        features_list.append(features.T)
        labels_list.append(label)

    return np.array(features_list), np.array(labels_list)


def load_sample_dataset(test_split=20):
    """
    Load sample dataset
    :param test_split: Percentage of total data to be used as test.
    Rest is train
    :return: train_x, test_x, train_y, test_y
    """
    images = read_images_from_dir()
    features, labels = calculate_features(images)

    # Shuffle the features and labels in such a way that the relative
    # ordering is preserved
    features, labels = shuffle(features, labels)

    return train_test_split(features, labels, test_size=1 - test_split / 100)


if __name__ == '__main__':
    load_sample_dataset()
