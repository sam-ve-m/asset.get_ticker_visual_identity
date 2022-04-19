# Standards
from enum import Enum, IntEnum


class RegionEnum(str, Enum):
    br = "br"
    us = "us"


class CodeResponse(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    INVALID_ZENDESK_API_URL = 20
    ERROR_TO_REQUEST_ZENDESK_API = 21
    INTERNAL_SERVER_ERROR = 100

import requests

print(type(requests.get('https://google.com.br')))