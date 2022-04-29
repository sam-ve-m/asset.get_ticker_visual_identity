# Jormungandr
from tests.src.stubs import StubTicker, stub_path

# Standards
from unittest.mock import patch

# Third party
from pydantic import ValidationError
import pytest


@patch('func.src.service.S3Repository.generate_ticker_url', return_value=stub_path)
@patch('func.src.service.S3Repository.get_ticker', return_value=True)
def test_when_region_br_symbol_and_type_valid_then_create_url(mock_s3_get_ticker, mock_generate_ticket, instance_ticker_visual_identity):
    result = instance_ticker_visual_identity.get_url_ticker()
    assert isinstance(result, dict)
    assert "logo_url" in result
    assert result["logo_url"] == 'url.inteira.com.br'



def test_when_region_br_and_symbol_is_invalid_str_then_create_invalid_url():
    params = StubTicker().set_symbol("asdPETR").set_region("br").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
            url_path
            == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/asdP.png"
    )


def test_when_region_and_symbol_not_str_then_return_exception():
    params = StubTicker().set_symbol(123).set_region(1).create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_not_str_then_return_exception():
    params = StubTicker().set_symbol("PETR").set_region(1).create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_not_enum_choices_then_return_exception():
    params = StubTicker().set_symbol("PETR").set_region("par").create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_symbol_not_str_then_return_exception():
    params = StubTicker().set_symbol(123).set_region("br").create_dict_params()
    with pytest.raises(ValidationError):
        create_ticker_url_path(params)


def test_when_region_us_and_symbol_valid_then_create_url():
    params = StubTicker().set_symbol("AAPL").set_region("us").create_dict_params()
    url_path = create_ticker_url_path(params)
    assert (
            url_path
            == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/us/AAPL.png"
    )


def test_when_region_us_and_symbol_is_invalid_str_then_create_invalid_url():
    params = StubTicker().set_symbol("AAPL123").set_region("us").create_dict_params()
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
def test_when_function_is_called_then_requests_get_has_called(mock_requests_get, url_valid):
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

    assert response["success"] is True
    assert response['result']["logo_uri"] == url_valid


def test_when_403_status_code_then_response_true(url_invalid):
    params = StubRequestsObj().set_status_code(403).set_url(url_invalid)
    response = get_response_from_url_path(params)

    assert response["success"] is True
    assert response['result']["logo_uri"] is None


def test_when_500_status_code_then_response_raises(url_invalid):
    params = StubRequestsObj().set_status_code(500).set_url(url_invalid)
    with pytest.raises(Exception, match="unexpected error occurred"):
        get_response_from_url_path(params)


def test_when_not_expected_status_code_then_response_raises(url_invalid):
    params = StubRequestsObj().set_status_code(301).set_url(url_invalid)
    with pytest.raises(Exception, match="unexpected error occurred"):
        get_response_from_url_path(params)
