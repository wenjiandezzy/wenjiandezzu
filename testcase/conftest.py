import pytest


@pytest.fixture(scope='session', autouse=True)
def print_info():
    print('-'*10, '接口开始测试', '-'*10)
    yield
    print('-'*10, '接口测试结束', '-'*10)