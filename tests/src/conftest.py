# Jormungandr
from func.src.service import TickerVisualIdentityService
from tests.src.stubs import StubTicker

# Third party
from pytest import fixture


@fixture(scope="function")
def instance_ticker_visual_identity():
    params = StubTicker(region='BR', symbol='AAPLAA12@', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_us_ticker_visual_identity():
    params = StubTicker(region='US', symbol='AAPLAA12@', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_us_logo():
    params = StubTicker(region='US', symbol='AAPLAA12@', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_us_banner():
    params = StubTicker(region='US', symbol='AAPL', type='banner').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_banner():
    params = StubTicker(region='BR', symbol='AAPL', type='banner').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_thumbnail():
    params = StubTicker(region='BR', symbol='AAPL', type='thumbnail').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_us_thumbnail():
    params = StubTicker(region='US', symbol='AAPL4', type='thumbnail').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_service_with_type_abcd():
    params = StubTicker(region='BR', symbol='AAPL', type='abcd').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_region_invalid():
    params = StubTicker(region='PR', symbol='AAPL', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance


@fixture(scope="function")
def instance_symbol_invalid():
    params = StubTicker(region='BR', symbol='APPL', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance
