from pydantic import BaseModel, Extra, validator

from .enum import RegionEnum


class MandatoryParameters(BaseModel, extra=Extra.forbid):
    symbol: str
    region: RegionEnum

    @validator("symbol")
    def is_empty(symbol: str) -> str:
        if not symbol:
            raise ValueError("Symbol is empty.")
        return symbol

    @validator("symbol")
    def is_alpha(symbol: str) -> str:
        if symbol.isnumeric():
            raise ValueError("Wrong format type")
        return symbol

    @validator("region")
    def is_numeric(region: str) -> RegionEnum:
        if not region.isalpha():
            raise ValueError("Wrong format type")
        return region

    @staticmethod
    def validate_unpacking(json: dict) -> dict:
        params = MandatoryParameters(**json).dict()
        return params
