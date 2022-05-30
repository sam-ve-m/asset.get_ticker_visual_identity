# Jormungandr
from src.domain.exception import TickerNotFound
from src.service import TickerVisualIdentityService
from src.domain.enum import CodeResponse
from src.domain.validator import TickerModel
from src.domain.response.model import ResponseModel

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response


def get_ticker_visual_identity() -> Response:
    message = "Jormungandr::get_ticker_visual_identity"
    json_params = request.get_json()
    try:
        validated_params = TickerModel(**json_params).dict()
        ticker_visual_identity_service = TickerVisualIdentityService(params=validated_params)
        result = ticker_visual_identity_service.get_ticker_url()
        response_model = ResponseModel.build_response(
            result=result,
            success=True,
            code=CodeResponse.SUCCESS
            )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.OK)
        return response

    except TickerNotFound as ex:
        response_model = ResponseModel.build_response(
            success=True,
            message=ex.msg,
            code=CodeResponse.DATA_NOT_FOUND
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.NOT_FOUND
            )
        return response

    except ValueError as ex:
        Gladsheim.error(ex=ex, message=f'{message}::There are invalid format'
                                       'or extra/missing parameters')
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.INVALID_PARAMS,
            message="There are invalid format or extra/missing parameters",
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.BAD_REQUEST
        )
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=f"{message}::{str(ex)}")
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return response
