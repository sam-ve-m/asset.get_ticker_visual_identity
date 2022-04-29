# Jormungandr
from .domain.enum import RegionEnum
from .domain.exception import TickerNotFound
from .repository import S3Repository


# Third party
from etria_logger import Gladsheim
from decouple import config


class TickerVisualIdentityService:
    def __init__(self, params):
        self.params = params

    def get_url_ticker(self) -> dict:
        self._treatment_ticker_symbol()
        ticker_path = self._ticker_path_by_type()
        ticker_exist = S3Repository.get_ticker(ticker_path=ticker_path)
        if ticker_exist:
            ticker_url_access = S3Repository.generate_ticker_url(ticker_path=ticker_path)
            ticker_type = self.params["type"]
            result = {f"{ticker_type}_url": ticker_url_access}
            return result
        Gladsheim.error(message=f"No images found for this ticker path::{ticker_path}")
        raise TickerNotFound

    def _ticker_path_by_type(self):
        region = self.params["region"]
        ticker_type = self.params["type"]
        symbol = self.params["symbol"]
        url_per_type = {
            "logo": f'{region}/{symbol}/{ticker_type}.{config("LOGO_EXTENSION")}',
            "banner": f'{region}/{symbol}/{ticker_type}.{config("BANNER_EXTENSION")}',
            "thumbnail": f'{region}/{symbol}/{ticker_type}.{config("THUMBNAIL_EXTENSION")}',
        }
        url_path = url_per_type.get(ticker_type, None)
        return url_path

    def _treatment_ticker_symbol(self):
        if self.params["region"] == RegionEnum.br.value:
            ticker = self.params["symbol"]
            ticker_slice_index = int(config("TICKER_SLICE_INDEX"))
            ticker_without_suffix_number = ticker[:ticker_slice_index]
            self.params.update(symbol=ticker_without_suffix_number)
