# Jormungandr
from func.src.domain.exception import TickerNotFound
from func.src.domain.validator import TickerModel
from tests.src.stubs import stub_path, stub_path_encoded, stub_params_type_invalid, stub_params_region_invalid

# Standards
from unittest.mock import patch

# Third party
import pytest


@patch('func.src.service.config', side_effect=[4, 'companies', 'png', 'companies', 'png', 'companies', 'png'])
@patch('func.src.service.RedisRepository.set')
@patch('func.src.service.S3Repository.generate_ticker_url', return_value=stub_path)
@patch('func.src.service.S3Repository.get_ticker', return_value=True)
@patch('func.src.service.RedisRepository.get', return_value=False)
def test_when_region_and_symbol_and_type_valid_then_create_url(mock_redis_get, mock_s3_get, mock_generate_ticket, mock_redis_set, mock_env, instance_ticker_visual_identity):
    result = instance_ticker_visual_identity.get_ticker_url()
    assert isinstance(result, dict)
    assert "url" in result
    assert "type" in result
    assert result["url"] == 'url.inteira.com.br'
    assert result['type'] == "logo"


@patch('func.src.service.config', side_effect=[4, 'companies', 'png', 'companies', 'png', 'companies', 'png'])
@patch('func.src.service.RedisRepository.get', return_value=stub_path_encoded)
def test_when_url_key_already_exist_in_redis_then_get_url(mock_redis_get, mock_env, instance_ticker_visual_identity):
    result = instance_ticker_visual_identity.get_ticker_url()
    assert isinstance(result, dict)
    assert "url" in result
    assert "type" in result
    assert result["url"] == 'url.inteira.com.br'
    assert result['type'] == "logo"


@patch('func.src.service.config', side_effect=[4, 'companies', 'png', 'companies', 'png', 'companies', 'png'])
@patch('func.src.service.S3Repository.get_ticker', return_value=False)
@patch('func.src.service.RedisRepository.get', return_value=False)
def test_when_symbol_is_invalid_then_raises(mock_redis_get, mock_s3_get, mock_env, instance_symbol_invalid):
    with pytest.raises(TickerNotFound):
        instance_symbol_invalid.get_ticker_url()


def test_when_region_is_invalid_then_raises():
    with pytest.raises(ValueError):
        TickerModel(**stub_params_region_invalid)


def test_when_type_is_invalid_then_raises():
    with pytest.raises(ValueError):
        TickerModel(**stub_params_type_invalid)


@patch('func.src.service.config', side_effect=[4, 'companies', 'png', 'companies', 'png', 'companies', 'png'])
def test_when_get_logo_then_return_url_path(mock_env, instance_ticker_visual_identity):
    instance_ticker_visual_identity._treatment_ticker_symbol()
    url_path = instance_ticker_visual_identity._ticker_path_by_type()

    assert url_path == 'companies/BR/AAPL/logo.png'


@patch('func.src.service.config', side_effect=['companies', 'png', 'companies', 'png', 'companies', 'png'])
def test_when_get_banner_then_return_url_path(mock_env, instance_service_with_banner):
    url_path = instance_service_with_banner._ticker_path_by_type()
    assert url_path == 'companies/BR/AAPL/banner.png'


@patch('func.src.service.config', side_effect=['companies', 'png', 'companies', 'png', 'companies', 'png'])
def test_when_get_thumbnail_then_return_url_path(mock_env, instance_service_with_thumbnail):
    url_path = instance_service_with_thumbnail._ticker_path_by_type()
    assert url_path == 'companies/BR/AAPL/thumbnail.png'


@patch('func.src.service.config', side_effect=['companies', 'png', 'companies', 'png', 'companies', 'png'])
def test_when_get_us_logo_then_return_url_path(mock_env, instance_service_with_us_logo):
    instance_service_with_us_logo._treatment_ticker_symbol()
    url_path = instance_service_with_us_logo._ticker_path_by_type()

    assert url_path == 'companies/US/AAPLAA12@/logo.png'


@patch('func.src.service.config', side_effect=['companies', 'png', 'companies', 'png', 'companies', 'png'])
def test_when_get_us_banner_then_return_url_path(mock_env, instance_service_with_us_banner):
    url_path = instance_service_with_us_banner._ticker_path_by_type()
    assert url_path == 'companies/US/AAPL/banner.png'


@patch('func.src.service.config', side_effect=['companies', 'png', 'companies', 'png', 'companies', 'png'])
def test_when_get_us_thumbnail_then_return_url_path(mock_env, instance_service_with_us_thumbnail):
    url_path = instance_service_with_us_thumbnail._ticker_path_by_type()
    assert url_path == 'companies/US/AAPL4/thumbnail.png'


@patch('func.src.service.config', side_effect=['companies', 'png', 'companies', 'png', 'companies', 'png'])
def test_when_get_not_predicted_img_type_then_return_none(mock_env, instance_service_with_type_abcd):
    url_path = instance_service_with_type_abcd._ticker_path_by_type()
    assert url_path is None


@patch('func.src.service.config', side_effect=[4])
def test_when_region_br_then_slice_4_first_letters(mock_env, instance_ticker_visual_identity):
    instance_ticker_visual_identity._treatment_ticker_symbol()
    symbol = instance_ticker_visual_identity.params['symbol']

    assert symbol == 'AAPL'


@patch('func.src.service.config', side_effect=[4])
def test_when_region_us_then_symbol_not_change(mock_env, instance_us_ticker_visual_identity):
    instance_us_ticker_visual_identity._treatment_ticker_symbol()
    symbol = instance_us_ticker_visual_identity.params['symbol']

    assert symbol == 'AAPLAA12@'
