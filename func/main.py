from flask import request, Response
from logging import getLogger
from json import dumps
from src import service

log = getLogger()


def get_ticker_visual_identity():
    try:
        json_params = request.json
        url_path = service.create_url_path(json_params)
        service.check_if_url_is_valid(url_path)
        response = {
            'status': True,
            'logo_uri': url_path
            }
    except Exception as error:
        log.error(str(error), exc_info=error)
        response = {
            'status': False,
            'message': str(error)
            }
    finally:
        return Response(
            dumps(response),
            mimetype="application/json"
        )
