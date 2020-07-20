import numpy as np
import cv2


def vertical_projection(picture, threshold):
    height, width = picture.shape
    histogram_y = []
    for x in range(0, width):
        counter = 0
        for y in range(0, height):
            if picture[y][x] == 0:
                counter = counter + 1
        histogram_y.append(counter)
    range_y = []
    start_point = 0
    end_point = 0

    for x in range(0, len(histogram_y) - 1):
        if histogram_y[x] >= threshold:
            if start_point == 0:
                start_point = x

        if histogram_y[x + 1] > threshold:
            if start_point != 0:
                end_point = x + 1
        else:
            if start_point != 0:
                end_point = x
                if start_point != end_point:
                    range_y.append((start_point, end_point))
                start_point = 0
                end_point = 0
    return range_y


def horizontal_projection(picture, threshold):
    height, width = picture.shape
    histogram_y = []
    for x in range(0, height):
        counter = 0
        for y in range(0, width):
            if picture[x][y] == 0:
                counter = counter + 1
        histogram_y.append(counter)

    range_x = []
    start_point = 0
    end_point = 0
    for x in range(0, len(histogram_y) - 1):
        if histogram_y[x] >= threshold:
            if start_point == 0:
                start_point = x

        if histogram_y[x + 1] > threshold:
            if start_point != 0:
                end_point = x + 1
        else:
            if start_point != 0:
                range_x.append((start_point, end_point))
                start_point = 0
                end_point = 0
    return range_x


def crop(image, threshold):
    bordersize = 3
    copiedImage = cv2.copyMakeBorder(
        image,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )
    rangeX = vertical_projection(copiedImage, threshold)
    segmentedVert = copiedImage[:, rangeX[0][0]:rangeX[0][1]]
    rangeY = horizontal_projection(segmentedVert, threshold)
    result = np.asarray(segmentedVert[rangeY[0][0]:get_last_range(rangeY), :])
    return result


def vertical_projection_remove_picture(picture):
    height, width = picture.shape
    histogram_y = []
    for x in range(0, width):
        counter = 0
        for y in range(0, height):
            if picture[y][x] == 0:
                counter = counter + 1
        histogram_y.append(counter)
    start_point = 0

    for x in range(0, len(histogram_y) - 1):
        if x > width / 2:
            if histogram_y[x] >= 100:
                if start_point == 0:
                    start_point = x
                    break
    return start_point


def get_last_range(rangeY):
    if rangeY[len(rangeY) - 1][1] == 0:
        return rangeY[len(rangeY) - 1][0]
    else:
        return rangeY[len(rangeY) - 1][1]
