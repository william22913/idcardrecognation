import cv2
import numpy
from service.ProfileProjection import vertical_projection_remove_picture, horizontal_projection_header
from service.AdjustBrightness import adjust_brightness
from service.Features import get_features
import string


def preprocessing_image(path: string, with_vision=False):
    image = cv2.imread(path)
    resize = cv2.resize(image, (800, 400), interpolation=cv2.INTER_AREA)
    resize = adjust_brightness(resize, 340, 180)

    if with_vision:
        cv2.imshow('original', resize)
        cv2.waitKey()

    grey = cv2.cvtColor(resize, cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_OTSU)

    # Removing KTP Picture
    range_y = vertical_projection_remove_picture(binary)
    without_picture = binary[:, 0:range_y+10]

    if with_vision:
        cv2.imshow('remove photo', without_picture)
        cv2.waitKey()

    node_x = horizontal_projection_header(binary, 5)
    used_photo = numpy.full((400, 800, 3), dtype=numpy.uint8, fill_value=255)

    header = resize[0:node_x+2, :, :]
    body = resize[node_x:, 0:range_y-3, :]
    header_height, header_width, _ = header.shape
    body_height, body_width, _ = body.shape

    # used_photo = body
    used_photo[0:header_height, 0:header_width, :] = header
    used_photo[header_height-2:body_height+header_height, 0:body_width, :] = body

    features = get_features(resize)

    if with_vision:
        cv2.imshow('used', used_photo)
        # cv2.imshow('header', header)
        # cv2.imshow('body', body)
        cv2.waitKey()

    return used_photo, features
