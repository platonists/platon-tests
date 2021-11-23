import pytest
from platon_env.chain import Chain
from setting import setting


def pytest_addoption(parser):
    parser.addoption("--chainFile", action="store", help="chainFile: chain data file")


@pytest.fixture(scope="session")
def env(request):
    """ 返回链对象，请勿直接使用
    """
    chain_file = request.config.getoption("--chainFile")
    chain = Chain.from_file(chain_file)
    chain.install(setting.PLATON,
                  setting.NETWORK,
                  setting.GENESIS_FILE,
                  )

    yield chain
    chain.uninstall()


def chain(env):
    """ 获取符合条件的chain对象
    """
    pass


