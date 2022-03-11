from flask import request, Response
from json import dumps
from etria_logger import Gladsheim

from src import service


def get_ticker_visual_identity():
    try:
        params = request.json
        url_path = service.create_ticker_url_path(params)
        requests_obj = service.get_requests_object_from_url_path(url_path)
        response = service.get_response_from_url_path(requests_obj)
        return Response(dumps(response), mimetype="application/json", status=200)
    except Exception as error:
        message = { "message": "Fission: get_ticker_visual_identity"}
        Gladsheim.error(error, message)
        return Response(dumps(message), mimetype="application/json", status=403)
