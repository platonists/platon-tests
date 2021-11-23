import os.path
from functools import singledispatch
from random import choice

import pytest

NO_PROPOSAL = 'no proposal'
CONDITIONS = set(NO_PROPOSAL)


def assert_chain(chain, condition):
    """ 判断chain是否符合条件
    """
    if not condition:
        return True

    if condition == NO_PROPOSAL:
        # 是否存在提案
        pass

    return False


@pytest.fixture
def chain(chain_obj, request):
    """ 返回一个符合条件的chain对象
    """
    condition = request.param
    result = assert_chain(chain_obj, condition)
    if not result:
        chain.install()
    return chain_obj


@pytest.fixture
def node(chain):
    """ 返回一各随机节点
    """
    return choice(chain.nodes)


def verifier_node():
    """ 返回一个随机验证节点
    """
    ...


def normal_node():
    """ 返回一个随机普通节点
    """
    ...


@pytest.fixture()
def solidity(node, request):
    """ 根据合约名，返回一个合约对象
    """
    name = request.param
    file = ''
    assert os.path.isfile(file), ''
    return node.web3.platon.contract()


@pytest.fixture()
def wasm(node, request):
    """ 根据合约名，返回一个合约对象
    """
    name = request.param
    file = ''
    assert os.path.isfile(file), ''
    return node.web3.platon.contract(vm_type='wasm')



