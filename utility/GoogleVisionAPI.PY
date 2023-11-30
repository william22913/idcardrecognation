import logging
from Main import appConfig
from utility.TextReader import read_google_vision_result
import requests
import json
import cv2
import base64


google_key = 'x-goog-api-key'
message = '{"requests": [{"image": {"content": {}}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],' \
      '"imageContext": {"languageHints": ["id"]}}]}'


def hit_api_google_vision(image):
    file_data = cv2.imencode('.jpg', image)
    base64_image = base64.b64encode(file_data[1]).decode('utf-8')

    payload = json.loads(message)
    payload['requests'][0]['image']['content'] = base64_image
    header = {'Content-Type': 'application/json', google_key: appConfig.google_api_key}
    response = requests.post(appConfig.google_url, json=payload, headers=header)

    if response.status_code != 200:
        logging.log(0, 'ERROR FOUND WHEN HIT GOOGLE API', response.text)
        return False, {}

    response_payload = json.loads(response.text)
    text = response_payload['responses'][0]['textAnnotations'][0]['description']
    return True, read_google_vision_result(text)


