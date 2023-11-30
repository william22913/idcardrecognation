import cv2
import numpy
from os import walk
from utility.AdjustBrightness import adjust_brightness
from utility.Features import get_features

knn = cv2.ml.KNearest_create()
path_original = './original'
features_ori = []
labels_ori = []
features_scan = []
labels_scan = []

x = 0
for (dir_path, dir_names, filenames) in walk(path_original):
    features_ori = numpy.zeros((len(filenames), 3))
    for filename in filenames:
        image = cv2.imread(path_original + "/" + filename)
        resize = cv2.resize(image, (800, 400), interpolation=cv2.INTER_AREA)
        resize = adjust_brightness(resize, 340, 180)
        feature = get_features(resize)
        for idx, j in enumerate(feature):
            features_ori[x, idx] = j
        labels_ori.append(numpy.float32(0))
        x = x + 1

labels_ori = numpy.asarray(labels_ori)
path_original = './scanned'
x = 0
for (dir_path, dir_names, filenames) in walk(path_original):
    features_scan = numpy.zeros((len(filenames), 3))
    for filename in filenames:
        image = cv2.imread(path_original + "/" + filename)
        resize = cv2.resize(image, (800, 400), interpolation=cv2.INTER_AREA)
        resize = adjust_brightness(resize, 340, 180)
        feature = get_features(resize)
        for idx, j in enumerate(feature):
            features_scan[x, idx] = j
        labels_scan.append(numpy.float32(1))
        x = x + 1

labels_scan = numpy.asarray(labels_scan)
features = numpy.vstack((features_ori, features_scan))
labels = numpy.concatenate((labels_ori, labels_scan))
features = features.astype(numpy.float32)
labels = numpy.asarray(labels).astype(numpy.float32)

numpy.save('../data/features', features)
numpy.save('../data/labels', labels)
