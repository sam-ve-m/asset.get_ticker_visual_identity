# Jormungandr
from func.src.domain.enums.response import Region, ImageType

# Third party
from pydantic import BaseModel, Extra, validator


class Ticker(BaseModel, extra=Extra.forbid):
    symbol: str
    region: Region
    type: ImageType

    @validator("symbol")
    def is_empty(cls, symbol: str) -> str:
        if not symbol:
            raise ValueError("Symbol is empty.")
        return symbol

    @validator("symbol")
    def is_alpha(cls, symbol: str) -> str:
        if symbol.isnumeric():
            raise ValueError("Wrong format type")
        return symbol
