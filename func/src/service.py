from decouple import config
import requests

from .enum import RegionEnum, StatusCodeEnum
from .validator import MandatoryParameters


def create_ticker_url_path(params: dict) -> str:
    params_dict = _validate_url_params(params)
    url_path = f"https://{config('BASE_PATH_TICKER_VISUAL_IDENTITY')}/{params_dict['region']}/{params_dict['symbol']}.{config('VISUAL_IDENTITY_EXTENSION')}"
    return url_path


def _validate_url_params(params: dict) -> dict:
    MandatoryParameters.validate_unpacking(params)
    if params["region"] == RegionEnum.br.value:
        ticker = params["symbol"]
        ticker_slice_index = int(config("TICKER_SLICE_INDEX"))
        ticker_without_suffix_number = ticker[:ticker_slice_index]
        params.update(symbol=ticker_without_suffix_number)
        return params
    return params


def get_requests_object_from_url_path(url_path: str) -> object:
    requests_response = requests.get(url_path)
    return requests_response


def get_response_from_url_path(requests_response: object) -> dict:
    dic_response = {
        StatusCodeEnum.success.value: lambda: _response(True, requests_response.url),
        StatusCodeEnum.bad_request.value: lambda: _response(False, ""),
        StatusCodeEnum.internal_server_error.value: lambda: _raise(Exception("Internal server error"))
    }
    lambda_response = dic_response.get(
        requests_response.status_code, StatusCodeEnum.internal_server_error.value
    )
    response = lambda_response()
    return response


def _response(status: bool, url_path: str) -> dict:
    response = {
        "status": status,
        "logo_uri": url_path,
    }
    return response


def _raise(exception: Exception):
    raise exception
