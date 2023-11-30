import numpy
import cv2
from utility.AdjustBrightness import adjust_brightness
from skimage.feature import local_binary_pattern
from skimage.feature import graycomatrix
from skimage.feature import graycoprops


class Features:
    def __init__(self, entropy, lbp, intensity, saturation, contrast, correlation, energy, homogeneity):
        self.entropy = entropy
        self.lbp = lbp
        self.intensity = intensity
        self.saturation = saturation
        self.contrast = contrast
        self.correlation = correlation
        self.energy = energy
        self.homogeneity = homogeneity


def get_features(resize, show_image=False):
    clip = cv2.cvtColor(adjust_brightness(resize, 150, 250), cv2.COLOR_RGB2GRAY)
    if show_image:
        cv2.imshow('clip', clip)

    red = resize[:, :, 0]
    green = resize[:, :, 1]
    blue = resize[:, :, 2]

    avg_red = sum(red.flatten())/(800.0 * 400.0)
    avg_green = sum(green.flatten())/(800.0 * 400.0)
    avg_blue = sum(blue.flatten())/(800.0 * 400.0)

    max_colour = max([avg_red, avg_green, avg_blue])
    min_colour = min([avg_red, avg_green, avg_blue])

    intensity = 1.0/3.0 * (avg_red + avg_green + avg_blue)
    saturation = 0

    if max_colour != min_colour:
        saturation = 1 - (min_colour / intensity)

    img_bw = (clip > 0.2)
    img_bw = img_bw.flatten()
    prob_w = img_bw.sum() / len(img_bw)
    prob_b = 1 - prob_w

    # Calculate Entropy
    if prob_w == 0 or prob_w == 1:
        entropy = 0
    else:
        entropy = (-((prob_b * numpy.log(prob_b)) +
                     (prob_w * numpy.log(prob_w))))

    # Compute LBP image
    radius = 3
    n_points = 24
    lbp_image = local_binary_pattern(clip, n_points, radius, method="uniform")

    lbp_hist, _ = numpy.histogram(lbp_image, bins=numpy.arange(0, n_points + 3), range=(0, n_points + 2))
    lbp_hist = lbp_hist / (lbp_hist.sum() + 1e-6)  # Normalize the histogram
    lbp_hist = lbp_hist.flatten()

    lbp = min(lbp_hist)

    co_matrix = graycomatrix(clip, [5], [0], levels=256, symmetric=True, normed=True)

    contrast = graycoprops(co_matrix, 'contrast')
    correlation = graycoprops(co_matrix, 'correlation')
    energy = graycoprops(co_matrix, 'energy')
    homogeneity = graycoprops(co_matrix, 'homogeneity')
    cv2.waitKey()

    # return [
    #     numpy.float32(entropy),
    #     numpy.float32(lbp),
    #     numpy.float32(intensity),
    #     numpy.float32(saturation),
    #     numpy.float32(contrast[0][0]),
    #     numpy.float32(correlation[0][0]),
    #     numpy.float32(energy[0][0]),
    #     numpy.float32(homogeneity[0][0])]

    return [
        numpy.float32(contrast[0][0]),
        numpy.float32(entropy),
        numpy.float32(intensity)]
