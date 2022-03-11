from func.src.service import (
    create_ticker_url_path,
    get_requests_object_from_url_path,
    get_response_from_url_path,
)
from pydantic import ValidationError
from unittest.mock import patch
import pytest


class TickerDataBuilder:
    def __init__(self):
        self.symbol = None
        self.region = None

    def set_symbol(self, symbol: str):
        self.symbol = symbol
        return self

    def set_region(self, region: str):
        self.region = region
        return self

    def create_dict_params(self):
        dict_params = {"symbol": self.symbol, "region": self.region}
        return dict_params


def test_when_region_br_and_symbol_valid_then_create_url():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol("PETRasd").set_region("br").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
        url_path
        == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png"
    )


def test_when_region_br_and_symbol_is_invalid_str_then_create_invalid_url():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol("asdPETR").set_region("br").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
        url_path
        == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/asdP.png"
    )


def test_when_region_and_symbol_not_str_then_return_exception():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol(123).set_region(1).create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_not_str_then_return_exception():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol("PETR").set_region(1).create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_not_enum_choices_then_return_exception():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol("PETR").set_region("par").create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_symbol_not_str_then_return_exception():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol(123).set_region("br").create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_us_and_symbol_valid_then_create_url():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol("AAPL").set_region("us").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
        url_path
        == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/us/AAPL.png"
    )


def test_when_region_us_and_symbol_is_invalid_str_then_create_invalid_url():
    ticker = TickerDataBuilder()
    params = ticker.set_symbol("AAPL123").set_region("us").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
        url_path
        == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/us/AAPL123.png"
    )


class RequestsObj:
    def __init__(self) -> None:
        self.url = None
        self.status_code = None

    def url(self):
        return self.url

    def set_url(self, url):
        self.url = url
        return self

    def status_code(self):
        return self.status_code

    def set_status_code(self, status_code):
        self.status_code = status_code
        return self


@patch('func.src.service.requests.get')
def test_when_requests_valid_url_then_return_requests_object(mock_get_requests_object):
    url = "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png"
    mock_get_requests_object.return_value = RequestsObj().set_url(url).set_status_code(200)
    requests_response = get_requests_object_from_url_path(url)
    assert requests_response.status_code == 200
    assert requests_response.url == url


@patch('func.src.service.requests.get')
def test_when_requests_invalid_url_then_return_requests_object(mock_get_requests_object):
    url = "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/123123PETR.png"
    mock_get_requests_object.return_value = RequestsObj().set_url(url).set_status_code(403)
    requests_response = get_requests_object_from_url_path(url)
    assert requests_response.status_code == 403
    assert requests_response.url == url


def test_when_200_status_code_then_response_true():
    url = "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png"
    params = RequestsObj().set_status_code(200).set_url(url)
    response = get_response_from_url_path(params)
    assert response['status'] is True
    assert response['logo_uri'] == url


def test_when_403_status_code_then_response_true():
    url = "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/123123PETR.png"
    params = RequestsObj().set_status_code(403).set_url(url)
    response = get_response_from_url_path(params)
    assert response['status'] is False
    assert response['logo_uri'] == ''


def test_when_not_expected_status_code_then_response_raises():
    url = "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/123123PETR.png"
    params = RequestsObj().set_status_code(500).set_url(url)
    with pytest.raises(Exception, match='Internal server error'):
        get_response_from_url_path(params)
