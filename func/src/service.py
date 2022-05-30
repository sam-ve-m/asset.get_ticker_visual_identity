# Jormungandr
from .domain.enum import RegionEnum
from .domain.exception import TickerNotFound
from .repositories.s3 import S3Repository
from .repositories.redis import RedisRepository

# Third party
from etria_logger import Gladsheim
from decouple import config


class TickerVisualIdentityService:
    def __init__(self, params):
        self.params = params

    def get_ticker_url(self) -> dict:
        self._treatment_ticker_symbol()
        ticker_path = self._ticker_path_by_type()
        ticker_url_access = TickerVisualIdentityService._get_or_set_ticker_url_access(ticker_path=ticker_path)
        ticker_type = self.params["type"]
        result = {"url": ticker_url_access, "type": ticker_type}
        return result

    def _ticker_path_by_type(self) -> str:
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
        region = self.params["region"]
        if region == RegionEnum.br.value:
            ticker = self.params["symbol"]
            ticker_slice_index = int(config("TICKER_SLICE_INDEX"))
            ticker_without_suffix_number = ticker[:ticker_slice_index]
            self.params.update(symbol=ticker_without_suffix_number)

    @staticmethod
    def _get_or_set_ticker_url_access(ticker_path) -> str:
        result = RedisRepository.get(ticker_path)
        if result:
            ticker_url_access = result.decode()
            return ticker_url_access
        ticker_exist = S3Repository.get_ticker(ticker_path=ticker_path)
        if ticker_exist:
            ticker_url_access = S3Repository.generate_ticker_url(ticker_path=ticker_path)
            RedisRepository.set(key=ticker_path, value=ticker_url_access)
            return ticker_url_access
        Gladsheim.error(message=f"No images found for this ticker path::{ticker_path}")
        raise TickerNotFound
