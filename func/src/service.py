import requests
from src.validator import ValidateJson


def validate_url_params(params: dict):
    ValidateJson.pydantic_validate(params)
    if params['region'] == 'br':
        symbol_slice = params['symbol']
        params.update(symbol=symbol_slice[:4])
        return params
    return params


def create_url_path(params: dict):
    params_dict = validate_url_params(params)
    url_path = f"https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/{params_dict['region']}/{params_dict['symbol']}.png"
    return url_path


def _raise(exception: Exception):
    raise exception


def check_if_url_is_valid(url_path: str):
    response_status_code = requests.get(url_path).status_code
    on_error = lambda: _raise(Exception('Something wrong'))
    dic_response = {
        200: lambda: True,
        400: lambda: _raise(Exception('Bad Request', 400)),
        403: lambda: _raise(Exception('Acess Denied', 403)),
    }
    response = dic_response.get(response_status_code, on_error)
    response()
