from flask import request, Response
from json import dumps
from logging import getLogger

from src import service

log = getLogger()


def get_ticker_visual_identity():
    try:
        params = request.json
        url_path = service.create_url_path(params)
        response = service.check_if_url_is_valid(url_path)
        return Response(
            dumps(response),
            mimetype="application/json",
            status=200
            )
    except Exception as error:
        log.error(str(error), exc_info=error)
        response = {
            'message': str(error),
            }
        return Response(
            dumps(response),
            mimetype="application/json",
            status=400
            )
