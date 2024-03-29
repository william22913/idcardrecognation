import numpy as np
import cv2
from utility.AdjustBrightness import adjust_brightness
from utility.Features import get_features

new_model = cv2.ml.KNearest_create()
is_initiate = 0


def value_of(label):
    if label == np.float32(0):
        return 'original'
    else:
        return 'scanned'


def initiate():
    features = np.load('./classification_model/data/features.npy')
    labels = np.load('./classification_model/data/labels.npy')
    new_model.train(features, 0, labels)


def do_classification(image):
    if is_initiate == 0:
        initiate()

    resize = adjust_brightness(image, 340, 180)
    feature = get_features(resize)
    temp = np.zeros((1, 3))
    for idx, j in enumerate(feature):
        temp[0, idx] = j

    temp = np.asarray(temp).astype(np.float32)

    _, res, neighbours, distance = new_model.findNearest(temp, 3)

    return value_of(res)
