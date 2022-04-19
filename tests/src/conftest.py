# Third party
from pytest import fixture


@fixture(scope='function')
def url_valid():
    return 'https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/PETR.png'


@fixture(scope='function')
def url_invalid():
    return 'https://sigame-companies-logo.s3.sa-east-1.amazonaws.com/br/123123PETR.png'