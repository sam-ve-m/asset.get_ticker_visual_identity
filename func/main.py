# Jormungandr
from src import service
from src.enum import CodeResponse

# Standards
from http import HTTPStatus
from json import dumps

# Third party
from etria_logger import Gladsheim
from flask import request, Response


def get_ticker_visual_identity() -> dict:
    message = "Jormungandr::get_ticker_visual_identity"
    try:
        params = request.json
        url_path = service.create_ticker_url_path(params)
        requests_obj = service.get_requests_object_from_url_path(url_path)
        service_response = service.get_response_from_url_path(requests_obj)
        response = Response(
            dumps(service_response),
            mimetype="application/json",
            status=HTTPStatus.OK.value,
        )
        return response

    except ValueError as ex:
        Gladsheim.error(ex=ex, message=f'{message}::There are invalid format or extra parameters')
        response = Response(
            dumps(
                {
                    "result": None,
                    "message": "There are invalid format or extra parameters",
                    "success": False,
                    "code": CodeResponse.INVALID_PARAMS.value,
                }
            ),
            mimetype="application/json",
            status=HTTPStatus.BAD_REQUEST.value,
        )
        return response

    except Exception as ex:
        Gladsheim.error(ex=ex, message=f'{message}::{str(ex)}')
        response = Response(
            dumps(
                {
                    "result": None,
                    "message": "Unexpected error occurred",
                    "success": False,
                    "code": CodeResponse.INTERNAL_SERVER_ERROR.value,
                }
            ),
            mimetype="application/json",
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
        return response
