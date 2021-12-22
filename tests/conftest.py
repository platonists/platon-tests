import os.path
from random import choice

import pytest
from platon_env.chain import Chain

from setting import setting
from lib.funcs import assert_chain, get_aides


@pytest.fixture(scope='session')
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


@pytest.fixture
def condition_chain(chain, request):
    """
    支持在使用该fixture时，传入一个参数，返回一个符合条件的chain对象。
    当前链无法满足条件时，会进行重新部署。
    注意：
    1、通过lib.funcs.CONDITIONS，获取当前支持的判断条件
    2、多个条件，请使用多个fixture来完成
    """
    condition = request.param
    result = assert_chain(chain, condition)
    if not result:
        chain.install()
    return chain


@pytest.fixture()
def defer_reset_chain(chain: Chain):
    """ 返回chain对象，并且在用例运行完成后恢复环境
    """
    yield chain
    chain.install(setting.PLATON,
                  setting.NETWORK,
                  setting.GENESIS_FILE,
                  )


@pytest.fixture(scope='session')
def aides(chain: Chain):
    """ 返回链上所有节点的aide对象列表
    """
    return get_aides(chain, 'all')


@pytest.fixture
def random_aide(aides):
    """ 返回一个随机节点的aide对象
    """
    return choice(aides)


@pytest.fixture(scope='session')
def init_aides(chain: Chain):
    """ 返回链上创世节点的aide对象列表
    """
    return get_aides(chain, 'init')


@pytest.fixture
def init_aide(init_aides):
    """ 返回一个创世节点的aide对象
    """
    return choice(init_aides)


@pytest.fixture(scope='session')
def normal_aides(chain: Chain):
    """ 返回链上普通节点的aide对象列表
    """
    return get_aides(chain, 'normal')


@pytest.fixture
def normal_aide(normal_aides):
    """ 返回一个普通节点的aide对象
    """
    return choice(normal_aides)


@pytest.fixture
def validator_aides():
    ...


@pytest.fixture
def validator_aide(validator_aides):
    ...


@pytest.fixture
def verifier_aides():
    ...


@pytest.fixture
def verifier_aide(validator_aides):
    ...


@pytest.fixture()
def solidity(node, request):
    """ 根据传入的合约参数，返回一个solidity合约对象
    注意：
    1、
    """
    name = request.param
    file = ''
    assert os.path.isfile(file), ''
    return node.web3.platon.contract()


@pytest.fixture()
def wasm(node, request):
    """ 根据传入的合约参数，返回一个solidity合约对象
    """
    name = request.param
    file = ''
    assert os.path.isfile(file), ''
    return node.web3.platon.contract(vm_type='wasm')
