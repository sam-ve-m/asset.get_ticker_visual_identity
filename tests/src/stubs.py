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
