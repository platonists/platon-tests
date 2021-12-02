import pytest
from platon_env.chain import Chain

from lib.aide import Aide
from setting import setting


def pytest_addoption(parser):
    parser.addoption("--chainFile", action="store", help="chainFile: chain data file")


@pytest.fixture(scope="session")
def chain(request):
    """ 返回链对象，不恢复环境，请谨慎使用
    """
    chain_file = request.config.getoption("--chainFile")
    chain = Chain.from_file(chain_file)
    chain.install(setting.PLATON,
                  setting.NETWORK,
                  setting.GENESIS_FILE,
                  )

    yield chain
    chain.uninstall()


@pytest.fixture()
def recover_chain(chain: Chain):
    """ 返回chain对象，并且在用例运行完成后恢复环境
    """
    yield chain
    chain.install(setting.PLATON,
                  setting.NETWORK,
                  setting.GENESIS_FILE,
                  )


def Aides(chain: Chain):
    """ 获取与节点对应的aide对象列表
    """
    aides = []
    for node in chain.nodes:
        aides.append(Aide(node))

    return aides
