# Jormungandr
from src.domain.exception import TickerNotFound
from func.src.services.ticker import TickerVisualIdentityService
from src.domain.enums import InternalCode
from src.domain.validator import TickerModel
from src.domain.response.model import ResponseModel

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response


def get_ticker_visual_identity() -> Response:

    try:
        json_params = request.get_json()
        validated_params = TickerModel(**json_params)
        ticker_visual_identity_service = TickerVisualIdentityService(params=validated_params)
        result = ticker_visual_identity_service.get_ticker_url()
        response = ResponseModel(
            result=result,
            success=True,
            code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except TickerNotFound as ex:
        result = {
            "url": None,
            "type": None
        }
        response = ResponseModel(
            result=result,
            success=True,
            message=ex.msg,
            code=InternalCode.DATA_NOT_FOUND
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError as ex:
        Gladsheim.error(ex=ex, message=f'Jormungandr::validator::There are invalid format'
                                       'or extra/missing parameters')
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="There are invalid format or extra/missing parameters",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=f"Jormungandr::get_ticker_visual_identity::{str(ex)}")
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
