# Standards
from enum import Enum, IntEnum
from strenum import StrEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    PARTNERS_INVALID_API_URL = 20
    PARTNERS_ERROR = 21
    JWT_INVALID = 30
    DATA_ALREADY_EXISTS = 98
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100

    def __repr__(self):
        return self.value


class ImageType(StrEnum):
    banner = "banner"
    logo = "logo"
    thumbnail = "thumbnail"

    def __repr__(self):
        return self.value


class RegionEnum(StrEnum):
    BR = "BR"
    US = "US"

    def __repr__(self):
        return self.value
