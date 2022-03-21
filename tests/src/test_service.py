from .conftest import TickerDataBuilder, StubRequestsObj
from func.src.service import (
    create_ticker_url_path,
    get_requests_object_from_url_path,
    get_response_from_url_path,
)

from pydantic import ValidationError
from unittest.mock import patch
import pytest


def test_when_region_br_and_symbol_valid_then_create_url():
    params = TickerDataBuilder().set_symbol("PETRasd").set_region("br").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
            url_path
            == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png"
    )


def test_when_region_br_and_symbol_is_invalid_str_then_create_invalid_url():
    params = TickerDataBuilder().set_symbol("asdPETR").set_region("br").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
            url_path
            == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/asdP.png"
    )


def test_when_region_and_symbol_not_str_then_return_exception():
    params = TickerDataBuilder().set_symbol(123).set_region(1).create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_not_str_then_return_exception():
    params = TickerDataBuilder().set_symbol("PETR").set_region(1).create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_not_enum_choices_then_return_exception():
    params = TickerDataBuilder().set_symbol("PETR").set_region("par").create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_symbol_not_str_then_return_exception():
    params = TickerDataBuilder().set_symbol(123).set_region("br").create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_us_and_symbol_valid_then_create_url():
    params = TickerDataBuilder().set_symbol("AAPL").set_region("us").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
            url_path
            == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/us/AAPL.png"
    )


def test_when_region_us_and_symbol_is_invalid_str_then_create_invalid_url():
    params = TickerDataBuilder().set_symbol("AAPL123").set_region("us").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
            url_path
            == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/us/AAPL123.png"
    )


@patch("func.src.service.requests.get")
def test_when_requests_valid_url_then_return_requests_object(mock_requests_get, url_valid):
    mock_requests_get.return_value = (StubRequestsObj().set_url(url_valid).set_status_code(200))
    requests_response = get_requests_object_from_url_path(url_valid)

    assert requests_response.status_code == 200
    assert requests_response.url == url_valid


@patch("func.src.service.requests.get")
def test_get_requests_object_is_called(mock_requests_get, url_valid):
    get_requests_object_from_url_path(url_valid)

    mock_requests_get.assert_called_once_with(url_valid)


@patch("func.src.service.requests.get")
def test_when_requests_invalid_url_then_return_requests_object(mock_get_requests_object, url_invalid):
    mock_get_requests_object.return_value = StubRequestsObj().set_url(url_invalid).set_status_code(403)
    requests_response = get_requests_object_from_url_path(url_invalid)

    assert requests_response.status_code == 403
    assert requests_response.url == url_invalid


def test_when_200_status_code_then_response_true(url_valid):
    params = StubRequestsObj().set_status_code(200).set_url(url_valid)
    response = get_response_from_url_path(params)

    assert response["status"] is True
    assert response["logo_uri"] == url_valid


def test_when_403_status_code_then_response_true(url_invalid):
    params = StubRequestsObj().set_status_code(403).set_url(url_invalid)
    response = get_response_from_url_path(params)

    assert response["status"] is False
    assert response["logo_uri"] == ""


def test_when_not_expected_status_code_then_response_raises(url_invalid):
    params = StubRequestsObj().set_status_code(500).set_url(url_invalid)
    with pytest.raises(Exception, match="Internal server error"):
        get_response_from_url_path(params)
