import cv2
from skimage.util import invert


def bordering_image(img):
    bordersize = 2
    mean = 255
    data = cv2.copyMakeBorder(
        img,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[mean, mean, mean]
    )
    data = invert(data)
    # ret, data = cv2.threshold(data, 0, 255, cv2.THRESH_BINARY)
    # data = thin(data)
    # data = cv2.Canny(data, 100, 200)
    # return data
    return invert(data)
