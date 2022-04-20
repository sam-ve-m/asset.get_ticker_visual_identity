# Jormungandr
from .enum import RegionEnum, CodeResponse
from .validator import MandatoryParameters

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from decouple import config
from requests.models import Response
import requests


def create_ticker_url_path(params: dict) -> str:
    params_dict = __validate_url_params(params)
    try:
        url_path = f"https://{config('BASE_PATH_TICKER_VISUAL_IDENTITY')}/{params_dict['region']}/{params_dict['symbol']}.{config('VISUAL_IDENTITY_EXTENSION')}"
        return url_path
    except Exception as ex:
        message = f'Jormungandr::get_ticker_visual_identity::create_ticker_url_path:: error to get .env params'
        Gladsheim.error(error=ex, message=message)
        raise ex


def __validate_url_params(params: dict) -> dict:
    MandatoryParameters.unpacking_to_dict(params)
    if params["region"] == RegionEnum.br.value:
        ticker = params["symbol"]
        ticker_slice_index = int(config("TICKER_SLICE_INDEX"))
        ticker_without_suffix_number = ticker[:ticker_slice_index]
        params.update(symbol=ticker_without_suffix_number)
        return params
    return params


def get_requests_object_from_url_path(url_path: str) -> Response:
    try:
        requests_obj = requests.get(url_path)
        return requests_obj
    except Exception as ex:
        message = f'Jormungandr::get_ticker_visual_identity::get_requests_object_from_url_path:: error requesting in {url_path}'
        Gladsheim.error(error=ex, message=message)
        raise ex


def get_response_from_url_path(requests_obj: Response) -> dict:
    message = 'There is no logo for the informed symbol and/or region'
    responses = {
        HTTPStatus.OK.value: lambda: __response(success=True, url_path=requests_obj.url, code=CodeResponse.SUCCESS.value),
        HTTPStatus.FORBIDDEN.value: lambda: __response(success=True, code=CodeResponse.DATA_NOT_FOUND.value, message=message),
        HTTPStatus.INTERNAL_SERVER_ERROR.value: lambda: __raise(Exception("unexpected error occurred"))
    }
    
    lambda_response = responses.get(
        requests_obj.status_code, responses.get(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    )
    response = lambda_response()
    return response


def __response(success: bool, code: int, url_path: str = None, message: str = None) -> dict:
    response = {
            "result": {"logo_uri": url_path},
            "message": message,
            "success": success,
            "code": code
        }
    return response


def __raise(exception: Exception):
    raise exception
