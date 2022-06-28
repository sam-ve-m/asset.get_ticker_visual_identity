# Jormungandr
from func.src.service import TickerVisualIdentityService
from tests.src.stubs import StubTicker

# Third party
from pytest import fixture


@fixture(scope="function")
def instance_ticker_visual_identity():
    params = StubTicker(region='br', symbol='AAPLAA12@', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_us_ticker_visual_identity():
    params = StubTicker(region='us', symbol='AAPLAA12@', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_banner():
    params = StubTicker(region='br', symbol='AAPL', type='banner').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_banner():
    params = StubTicker(region='br', symbol='AAPL', type='thumbnail').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_type_abcd():
    params = StubTicker(region='br', symbol='AAPL', type='abcd').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_region_invalid():
    params = StubTicker(region='pr', symbol='AAPL', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_symbol_invalid():
    params = StubTicker(region='br', symbol='APPL', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance
