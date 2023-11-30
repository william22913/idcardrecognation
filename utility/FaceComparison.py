import string
import face_recognition
import cv2


def face_comparison(first_photo: string, second_photo: string, with_vision=False):
    first_image = face_recognition.load_image_file(first_photo)
    second_image = face_recognition.load_image_file(second_photo)

    if with_vision:
        cv2.imshow('first_image', first_image)
        cv2.imshow('second_image', second_image)
        cv2.waitKey()

    first_image_encoding = face_recognition.face_encodings(first_image)[0]
    second_image_encoding = face_recognition.face_encodings(second_image)[0]

    results = face_recognition.face_distance([first_image_encoding], second_image_encoding)
    return 100.0 - results[0] * 100.0


