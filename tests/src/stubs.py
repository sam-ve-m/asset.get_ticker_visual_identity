class StubTicker:
    def __init__(self, symbol=None, region=None, type=None):
        self.symbol = symbol
        self.region = region
        self.type = type

    def create_dict_params(self):
        dict_params = {
            "symbol": self.symbol,
            "region": self.region,
            "type": self.type,
            }
        return dict_params


stub_path = 'url.inteira.com.br'
stub_path_encoded = stub_path.encode()
stub_params_type_invalid = StubTicker(region='br', symbol='AAPL', type='abcd').create_dict_params()
stub_params_region_invalid = StubTicker(region='pr', symbol='AAPL', type='logo').create_dict_params()
