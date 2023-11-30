import cv2
import uuid
import tempfile
import os
from Main import appConfig
from utility.Preprocessing import preprocessing_image
from utility.GoogleVisionAPI import hit_api_google_vision
from utility.Clasification import do_classification
from dto.out.out import *
from utility.FaceComparison import face_comparison
from flask import request, Response


NEXSOFT_API_KEY_FIELD = 'X-Nexsoft-Api-Key'
API_LANGUAGE = 'Accept-Language'
NEXSOFT_API_DEFAULT_LANGUAGE = 'en-US'


def check_nexsoft_api_key(headers):
    if headers.get(NEXSOFT_API_KEY_FIELD) is None:
        return False
    elif headers.get(NEXSOFT_API_KEY_FIELD) == appConfig.server_api_key:
        return True
    else:
        return False


def check_language(headers):
    if request.headers.get(API_LANGUAGE) is None:
        return NEXSOFT_API_DEFAULT_LANGUAGE
    elif headers.get(API_LANGUAGE) == 'en-US' or headers.get(API_LANGUAGE) == 'id-ID':
        return headers.get(API_LANGUAGE)
    else:
        return NEXSOFT_API_DEFAULT_LANGUAGE


def handle_request_without_selfie():
    key = uuid.uuid4()
    key = str(key).replace('-', '')

    request_id = request.headers.get("X-Request-Id")
    language = check_language(request.headers)

    if request_id is None:
        request_id = key

    if not check_nexsoft_api_key(request.headers):
        return Response(ErrorMessage(request_id, language, appConfig.server_version, 401, UNAUTHORIZED).JSON(),
                        content_type='application/json', status=401)

    if 'id-card' not in request.files or request.files['id-card'].filename == '':
        return Response(ErrorMessage(request_id, language, appConfig.server_version, 400, EMPTY_ID_CARD_FILE).JSON(),
                        content_type='application/json', status=400)

    id_card = request.files['id-card']
    temp_id_file, temp_id_card = tempfile.mkstemp(prefix='id_card_', dir='C:/Users/nexsoft/Desktop/temp', suffix=key)
    os.close(temp_id_file)
    id_card.save(temp_id_card)

    try:
        image = cv2.imread(temp_id_card)
        resize = cv2.resize(image, (800, 400), interpolation=cv2.INTER_AREA)

        if do_classification(resize) != 'original':
            return Response(ErrorMessage(request_id, language, appConfig.server_version, 400, NOT_ORIGINAL_PHOTO).JSON(),
                            content_type='application/json', status=400)

        image, people, _ = preprocessing_image(temp_id_card)
        valid, result = do_hit_api_google_vision(image)

        if not valid:
            return Response(ErrorMessage(request_id, language, appConfig.server_version, 400, UNKNOWN_ERROR).JSON(),
                            content_type='application/json', status=400)
    finally:
        os.remove(temp_id_card)

    return Response(
        SuccessMessage(
            request_id, appConfig.server_version,
            {
                "is_original_id": True,
                "id_card_value": result,
            }).JSON(), content_type='application/json', status=400)


def handle_request_with_selfie():
    key = uuid.uuid4()
    key = str(key).replace('-', '')

    request_id = request.headers.get("X-Request-Id")
    language = check_language(request.headers)

    if request_id is None:
        request_id = key

    if not check_nexsoft_api_key(request.headers):
        return Response(ErrorMessage(request_id, language, appConfig.server_version, 401, UNAUTHORIZED).JSON(),
                        content_type='application/json', status=401)

    if 'id-card' not in request.files or request.files['id-card'].filename == '':
        return Response(ErrorMessage(request_id, language, appConfig.server_version, 400, EMPTY_ID_CARD_FILE).JSON(),
                        content_type='application/json', status=400)

    if 'selfie' not in request.files or request.files['selfie'].filename == '':
        return Response(ErrorMessage(request_id, language, appConfig.server_version, 400, EMPTY_SELFIE_FILE).JSON(),
                        content_type='application/json', status=400)

    id_card = request.files['id-card']
    selfie = request.files['selfie']

    temp_id_file, temp_id_card = tempfile.mkstemp(prefix='selfie_', dir='C:/Users/nexsoft/Desktop/temp', suffix=key)
    os.close(temp_id_file)

    temp_selfie_file, temp_selfie = tempfile.mkstemp(prefix='selfie_', dir='C:/Users/nexsoft/Desktop/temp', suffix=key)
    os.close(temp_selfie_file)

    temp_people_file, temp_people = tempfile.mkstemp(prefix='people_', dir='C:/Users/nexsoft/Desktop/temp', suffix=key + ".jpg")
    os.close(temp_people_file)

    try:
        id_card.save(temp_id_card)
        selfie.save(temp_selfie)

        image = cv2.imread(temp_id_card)
        resize = cv2.resize(image, (800, 400), interpolation=cv2.INTER_AREA)

        if do_classification(resize) != 'original':
            return Response(ErrorMessage(request_id, language, appConfig.server_version, 400, NOT_ORIGINAL_PHOTO).JSON(),
                            content_type='application/json', status=400)

        image, people, _ = preprocessing_image(temp_id_card)
        cv2.imwrite(temp_people, people)
        valid, result = do_hit_api_google_vision(image)

        if not valid:
            return Response(ErrorMessage(request_id, language, appConfig.server_version, 400, UNKNOWN_ERROR).JSON(),
                            content_type='application/json', status=400)
        similarity = do_face_comparison(temp_people, selfie)

    finally:
        os.remove(temp_id_card)
        os.remove(temp_selfie)
        os.remove(temp_people)

    return Response(
        SuccessMessage(
            request_id, appConfig.server_version,
            {
                "is_original_id": True,
                "id_card_value": result,
                "similarity": similarity,
            }).JSON(), content_type='application/json', status=200)


def do_hit_api_google_vision(image):
    return hit_api_google_vision(image)


def do_face_comparison(temp_people, selfie):
    return face_comparison(temp_people, selfie)
