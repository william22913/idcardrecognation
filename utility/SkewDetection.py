import numpy as np
from scipy.ndimage import interpolation as inter


def fix_skew(bin_img):
    delta = 0.5
    limit = 0.8
    angles = np.arange(-limit, limit + delta, delta)
    scores = []
    for angle in angles:
        hist, score = find_score(bin_img, angle)
        scores.append(score)

    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]

    # correcting skewness
    return inter.rotate(bin_img, best_angle, reshape=True, order=0)


def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score
