from typing import Literal

from platon_env.chain import Chain

from lib.aide import Aide

NO_PROPOSAL = 'no proposal'
CONDITIONS = set(NO_PROPOSAL)       # 方便用例fixture使用


def assert_chain(chain, condition):
    """ 判断chain是否符合条件
    """
    if not condition:
        return True

    # 是否存在提案
    if condition == NO_PROPOSAL:
        pass

    return False


def get_aides(chain: Chain, _type: Literal['all', 'init', 'normal'] = 'all'):
    """ 根据不同的类型，获取
    todo: 待扩展 validator、verifier、staking 等实时方式
    """
    assert _type in ['all', 'init', 'normal']

    nodes = []
    if _type == 'all':
        nodes = chain.nodes
    elif _type == 'init':
        nodes = chain.init_nodes
    elif _type == 'normal':
        nodes = chain.normal_nodes

    aides = []
    for node in nodes:
        aides.append(Aide(node))

    return aides
