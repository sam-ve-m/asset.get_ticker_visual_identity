from src.service import create_ticker_url_path, check_if_url_is_valid
from pydantic import ValidationError
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


def test_when_url_valid_then_return_true():
    url_path = "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png"
    response = check_if_url_is_valid(url_path)
    assert response["status"] is True


def test_when_invalid_url_then_return_false():
    url_path = "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/aaPETR.png"
    response = check_if_url_is_valid(url_path)
    assert response["status"] is False
