import cv2
from service.Preprocessing import preprocessing_image
from service.AdjustBrightness import adjust_brightness
from service.Features import get_features
from service.Clasification import do_classification
import base64

# image = cv2.imread('sample_ktp/0b9fb6cl.bmp')
# resize = cv2.resize(image, (800, 400), interpolation=cv2.INTER_AREA)

# print(do_classification(resize))

image, features = preprocessing_image('sample_ktp/wcrtrchs.bmp')
print(features)
cv2.imshow('image', image)
cv2.waitKey()

# TODO HIT GOOGLE VISION API

# example = 'NIK\nNama\nTempat/Tgl Lahir\nJenis Kelamin\nAlamat\nRT/RW\nKel/Desa\nKecamatan\nPROVINSI DKI ' \
#           'JAKARTA\nJAKARTA SELATAN\n3174096112900001\n: DEBBY ANGGRAINI\n: JAKARTA, 21-12-1990\n: PEREMPUAN\n: JL ' \
#           'KECAPI V\n: 006 / 005\n: JAGAKARSA\n: JAGAKARSA\n: ISLAM\nAgama\nStatus Perkawinan: BELUM ' \
#           'KAWIN\nPekerjaan\nKewarganegaraan:\nBerlaku Hingga\nGol. Darah :\n: KARYAWAN SWASTA\nWNI\n: 21-12-2016 '

# print(read_google_vision_result(example))

# file_data = cv2.imencode('.jpg', used_photo)
# f = open("base64.txt", "a")
# data = base64.b64encode(file_data[1]).decode('utf-8')
#
# f.write(data)
# f.close()
