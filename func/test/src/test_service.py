from func.src.service import create_url_path, check_if_url_is_valid, validate_url_params
import pytest
from pydantic import ValidationError

br_params_valid = {
    "symbol": "PETRasd",
    "region": "br"
}
us_params_valid = {
    "symbol": "AAPL",
    "region": "us"
}
params_invalid = {
    "symbol": "asdPETR",
    "region": "br"
}
params_not_str = {
    "symbol": 123,
    "region": 1
}
params_region_not_str = {
    "symbol": "PETR",
    "region": 1
}
params_symbol_is_not_str = {
    "symbol": 123,
    "region": 'par'
}
params_region_not_us_or_br = {
    "symbol": "PETR",
    "region": 'par'
}




def test_when_region_br_and_symbol_valid_then_create_url():
    url_path = create_url_path(br_params_valid)
    assert url_path == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png"


def test_when_region_br_and_symbol_is_invalid_str_then_create_invalid_url():
    url_path = create_url_path(params_invalid)
    assert url_path == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/asdP.png"


def test_when_region_and_symbol_not_str_then_return_exception():
    with pytest.raises(ValidationError):
        create_url_path(params_not_str)


def test_when_region_not_str_then_return_exception():
    with pytest.raises(ValidationError):
        create_url_path(params_region_not_str)


def test_when_region_not_enum_choices_then_return_exception():
    with pytest.raises(ValidationError):
        create_url_path(params_region_not_us_or_br)


def test_when_symbol_not_str_then_return_exception():
    with pytest.raises(ValidationError):
        create_url_path(params_symbol_is_not_str)


def test_when_region_us_and_symbol_valid_then_create_url():
    url_path = create_url_path(us_params_valid)
    assert url_path == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/us/AAPL.png"


def test_when_region_us_and_symbol_is_invalid_str_then_create_invalid_url():
    url_path = create_url_path(params_invalid)
    assert url_path == "https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/asdP.png"


def test_when_url_valid_then_return_true():
    url_path = 'https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png'
    response = check_if_url_is_valid(url_path)
    assert response['status'] is True


def test_when_invalid_url_then_return_false():
    url_path = 'https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/aaPETR.png'
    response = check_if_url_is_valid(url_path)
    assert response['status'] is False


def test_validate_url_params_():
    ...







