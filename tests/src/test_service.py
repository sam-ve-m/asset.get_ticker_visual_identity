# Jormungandr
from func.src.domain.exception import TickerNotFound
from func.src.domain.validator import TickerModel
from tests.src.stubs import StubTicker, stub_path, stub_path_encoded, stub_params_type_invalid, stub_params_region_invalid

# Standards
from unittest.mock import patch

# Third party
import pytest


@patch('func.src.service.RedisRepository.set')
@patch('func.src.service.S3Repository.generate_ticker_url', return_value=stub_path)
@patch('func.src.service.S3Repository.get_ticker', return_value=True)
@patch('func.src.service.RedisRepository.get', return_value=False)
def test_when_region_and_symbol_and_type_valid_then_create_url(mock_redis_get, mock_s3_get, mock_generate_ticket, mock_redis_set, instance_ticker_visual_identity):
    result = instance_ticker_visual_identity.get_ticker_url()
    assert isinstance(result, dict)
    assert "logo_url" in result
    assert result["logo_url"] == 'url.inteira.com.br'


@patch('func.src.service.RedisRepository.get', return_value=stub_path_encoded)
def test_when_url_key_already_exist_in_redis_then_get_url(mock_redis_get, instance_ticker_visual_identity):
    result = instance_ticker_visual_identity.get_ticker_url()
    assert isinstance(result, dict)
    assert "logo_url" in result
    assert result["logo_url"] == 'url.inteira.com.br'


@patch('func.src.service.S3Repository.get_ticker', return_value=False)
@patch('func.src.service.RedisRepository.get', return_value=False)
def test_when_symbol_is_invalid_then_raises(mock_redis_get, mock_s3_get, instance_symbol_invalid):
    with pytest.raises(TickerNotFound):
        instance_symbol_invalid.get_ticker_url()


def test_when_region_is_invalid_then_raises():
    with pytest.raises(ValueError):
        TickerModel(**stub_params_region_invalid)


def test_when_type_is_invalid_then_raises():
    with pytest.raises(ValueError):
        TickerModel(**stub_params_type_invalid)


def test_when_get_logo_then_return_url_path(instance_ticker_visual_identity):
    instance_ticker_visual_identity._treatment_ticker_symbol()
    url_path = instance_ticker_visual_identity._ticker_path_by_type()

    assert url_path == 'br/AAPL/logo.jpg'


def test_when_get_banner_then_return_url_path(instance_service_with_banner):
    url_path = instance_service_with_banner._ticker_path_by_type()
    assert url_path == 'br/AAPL/banner.jpeg'


def test_when_get_banner_then_return_url_path(instance_service_with_banner):
    url_path = instance_service_with_banner._ticker_path_by_type()
    assert url_path == 'br/AAPL/thumbnail.jpg'


def test_when_get_not_predicted_img_type_then_return_none(instance_service_with_type_abcd):
    url_path = instance_service_with_type_abcd._ticker_path_by_type()
    assert url_path is None


def test_when_region_br_then_slice_4_first_letters(instance_ticker_visual_identity):
    instance_ticker_visual_identity._treatment_ticker_symbol()
    symbol = instance_ticker_visual_identity.params['symbol']

    assert symbol == 'AAPL'


def test_when_region_us_then_symbol_not_change(instance_us_ticker_visual_identity):
    instance_us_ticker_visual_identity._treatment_ticker_symbol()
    symbol = instance_us_ticker_visual_identity.params['symbol']

    assert symbol == 'AAPLAA12@'
