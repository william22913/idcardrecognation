import cv2
import numpy as np
from service.ProfileProjection import vertical_projection, horizontal_projection, vertical_projection_remove_picture
from service.AdjustBrightness import adjust_brightness
from service.SkewDetection import fix_skew
from service.Clasification import do_classification

image = cv2.imread('Sample KTP/85lya0a0.bmp')
resize = cv2.resize(image, (800, 400), interpolation=cv2.INTER_AREA)
resize = adjust_brightness(resize, 340, 180)
cv2.imshow('original', resize)
cv2.waitKey()

grey = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_OTSU)
skewFix = binary # fix_skew()

cv2.imshow('skewFix', skewFix)
cv2.waitKey()
height, width = skewFix.shape

# Removing KTP Picture
rangeY = vertical_projection_remove_picture(skewFix)
withoutPicture = skewFix[:, 0:rangeY]
cv2.imshow('remove photo', withoutPicture)
cv2.waitKey()

# Horizontal Projection
rangeX = horizontal_projection(withoutPicture, 5)

# Finding Start Point
start = 0
for i in range(0, len(rangeX)):
    temp = withoutPicture[rangeX[i][0]:rangeX[i][1], :]
    tempVertical = vertical_projection(temp, 0)
    if len(tempVertical) >= 5:
        if (tempVertical[0][1] - tempVertical[0][0]) < 20:
            start = i
            break

print("Start Point : ", start)
# Getting NIK
NIK = withoutPicture[rangeX[start + 2][0]:rangeX[start + 2][1], :]
cv2.imshow('NIK', NIK)

# Vertical Projection of NIK
rangeY_NIK = vertical_projection(NIK, 1)

# Slice NIK part and get all number of NIK
result = []
for i in range(len(rangeY_NIK) - 16, len(rangeY_NIK)):
    result.append(do_classification(NIK[:, rangeY_NIK[i][0]:rangeY_NIK[i][1]]))

result = np.array(result)
print("Nomor NIK : ", result.flatten())

cv2.waitKey()
cv2.destroyAllWindows()
