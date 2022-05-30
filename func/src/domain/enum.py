# Standards
from enum import Enum, IntEnum


class CodeResponse(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100


class ImageType(str, Enum):
    banner = "banner"
    logo = "logo"
    thumbnail = "thumbnail"


class RegionEnum(str, Enum):
    br = "br"
    us = "us"
