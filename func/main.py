# Jormungandr
from src import service
from src.enum import CodeResponse

# Standards
from http import HTTPStatus
from json import dumps

# Third party
from etria_logger import Gladsheim
from flask import request, Response
from pydantic.error_wrappers import ValidationError


def get_ticker_visual_identity():
    try:
        message = 'Jormungandr::get_ticker_visual_identity'
        params = request.json
        url_path = service.create_ticker_url_path(params)
        requests_obj = service.get_requests_object_from_url_path(url_path)
        service_response = service.get_response_from_url_path(requests_obj)
        response = Response(
            dumps({'result': service_response, 'success': True, 'code': CodeResponse.SUCCESS.value}),
            mimetype='application/json', status=HTTPStatus.OK.value)
        return response
    except ValidationError as ex:
        Gladsheim.error(ex=ex, message=message)
        response = Response(
            dumps({'message': f'{message}::There are invalid parameters', 'success': False,
                   'code': CodeResponse.INVALID_PARAMS.value}), mimetype='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value)
        return response
    except Exception as ex:
        Gladsheim.error(ex=ex, message=message)
        response = Response(
            dumps({'message': f'{message}::unexpected error occurred', 'success': False,
                   'code': CodeResponse.INTERNAL_SERVER_ERROR.value}), mimetype='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value)
        return response
