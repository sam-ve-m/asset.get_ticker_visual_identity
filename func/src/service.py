import requests
from func.src.validator import MandatoryParameters
from func.src.enum import RegionEnum, StatusCodeEnum
from decouple import config


def create_url_path(params: dict):
    params_dict = validate_url_params(params)
    url_path = f"https://{config('BASE_PATH_TICKER_VISUAL_IDENTITY')}/{params_dict['region']}/{params_dict['symbol']}.{config('VISUAL_IDENTITY_EXTENSION')}"
    return url_path


def validate_url_params(params: dict):
    MandatoryParameters.validate_unpacking(params)
    if params['region'] == RegionEnum.br.value:
        ticker = params['symbol']
        ticker_slice_index = int(config('TICKER_SLICE_INDEX'))
        ticker_without_suffix_number = ticker[:ticker_slice_index]
        params.update(symbol=ticker_without_suffix_number)
        return params
    return params


def check_if_url_is_valid(url_path: str):
    response_status_code = requests.get(url_path).status_code
    dic_response = {
        StatusCodeEnum.sucess.value: lambda: _response(True, url_path),
        StatusCodeEnum.bad_request.value: lambda: _response(False, ''),
        StatusCodeEnum.internal_server_error.value: lambda: _raise(Exception('Internal server error'))
    }
    lambda_response = dic_response.get(response_status_code, StatusCodeEnum.internal_server_error.value)
    response = lambda_response()
    return response


def _response(boll, url_path):
    response = {
        'status': boll,
        'logo_uri': url_path,
        }
    return response


def _raise(exception: Exception):
    raise exception
