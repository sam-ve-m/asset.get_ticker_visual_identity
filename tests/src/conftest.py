# Jormungandr
from func.src.service import TickerVisualIdentityService
from tests.src.stubs import StubTicker

# Third party
from pytest import fixture


@fixture(scope="function")
def instance_ticker_visual_identity():
    params = StubTicker(region='br', symbol='AAPL', type='logo').create_dict_params()
    service_instance = TickerVisualIdentityService(params=params)
    return service_instance
