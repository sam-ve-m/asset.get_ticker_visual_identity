from flask import request, Response
from json import dumps
from etria_logger import Gladsheim

from src import service


def get_ticker_visual_identity():
    try:
        params = request.json
        url_path = service.create_ticker_url_path(params)
        requests_obj = service.get_requests_object_from_url_path(url_path)
        service_response = service.get_response_from_url_path(requests_obj)
        response = Response(
            dumps(service_response), mimetype='application/json', status=200
        )
        return response
    except Exception as error:
        message = 'Fission: get_ticker_visual_identity'
        Gladsheim.error(error, message)
        response = Response(
            dumps(str(error)), mimetype='application/json', status=403
        )
        return response
