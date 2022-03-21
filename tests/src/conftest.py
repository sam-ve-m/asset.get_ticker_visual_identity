from pytest import fixture


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


class StubRequestsObj:
    def __init__(self) -> None:
        self.url = None
        self.status_code = None

    def url(self):
        return self.url

    def set_url(self, url):
        self.url = url
        return self

    def status_code(self):
        return self.status_code

    def set_status_code(self, status_code):
        self.status_code = status_code
        return self


@fixture(scope='function')
def url_valid():
    return 'https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png'


@fixture(scope='function')
def url_invalid():
    return 'https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/123123PETR.png'