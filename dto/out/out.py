from datetime import datetime
from Main import i18n
import string
import json

UNAUTHORIZED = "E-1-NIR-AUT-001"
EMPTY_ID_CARD_FILE = "E-4-NIR-DTO-001"
EMPTY_SELFIE_FILE = "E-4-NIR-DTO-002"
NOT_ORIGINAL_PHOTO = "E-4-NIR-SRV-001"
UNKNOWN_ERROR = "E-5-NIR-SRV-001"


class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ErrorMessage) or isinstance(obj, SuccessMessage) or isinstance(obj, Header) or isinstance(obj, ErrorPayload):
            return obj.__dict__
        return super().default(obj)


class SuccessMessage:
    def __init__(self, request_id, version, payload):
        self.success = True
        self.header = Header(request_id, version)
        self.payload = payload

    def JSON(self):
        return json.dumps(self, cls=MessageEncoder, indent=2)


class ErrorMessage:
    def __init__(self, request_id, language, version, status: int, error_code: string):
        self.success = False
        self.header = Header(request_id, version)
        self.payload = ErrorPayload(language, status, error_code)

    def JSON(self):
        return json.dumps(self, cls=MessageEncoder, indent=2)


class Header:
    def __init__(self, request_id, version):
        self.request_id = request_id
        self.version = version
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def JSON(self):
        return json.dumps(self, cls=MessageEncoder, indent=2)


class ErrorPayload:
    def __init__(self, language, status, error_code: string):
        self.status = status
        self.code = error_code
        self.message = i18n.read_message(language, error_code)

    def JSON(self):
        return json.dumps(self, cls=MessageEncoder, indent=2)
