from enum import Enum
from pydantic import BaseModel, Extra, validator


class RegionEnum(str, Enum):
    br = 'br'
    us = 'us'


class ValidateJson(BaseModel, extra=Extra.forbid):
    symbol: str
    region: RegionEnum

    @validator('symbol')
    def is_empty(symbol):
        if not symbol:
            raise ValueError("Symbol is empty.")
        return symbol

    @staticmethod
    def pydantic_validate(json: dict):
        return ValidateJson(**json)
