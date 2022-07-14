import copy
import time
import random

import allure
import pytest
from deepdiff import DeepDiff
from loguru import logger
from platon_env.chain import Chain
from platon_env.genesis import Genesis

from lib.aide import Aide
from setting import setting
from utils.chain_utils import max_byzantine_node, get_block_number, check_block
from utils.mixin import ChainPluginMixin


@allure.title("start all nodes normally")
@pytest.mark.P0
def test_all_node_normal(chain, aides):
    """
    @describe: 用于测试启动所有共识节点，查看块情况
    @step: 并发获取所有节点区块
    @expect:
        - 8个节点 出块高度差距 < 5
        - 3秒前区块高度 < 等待3s后节点中最高区块
    """
    chain_plugin_mixin = ChainPluginMixin(chain)
    pre_block_number = chain_plugin_mixin.get_block_number(aides)
    assert max(pre_block_number) - min(pre_block_number) < 5
    time.sleep(3)
    later_block_number = chain_plugin_mixin.get_block_number(aides)
    assert max(pre_block_number) < max(later_block_number)


@allure.title("Start consensus node 2f+1 starts to block")
@pytest.mark.P0
def test_SC_ST_002(chain):
    """
    @describe: 达到最小共识数即开始出块
    @step: 部署三个共识节点
    @expect:
        - 更改创世文件，并清理链
        - 部署3个共识节点正常出块
        - 停1个共识节点
    @expect: 三个共识节点停1个节点不在出块
    """
    chain_plugin_mixin = ChainPluginMixin(chain)
    deploy_nodes_number: int = (2 * chain_plugin_mixin.max_byzantine_node + 1)

    new_chain, aides = chain_plugin_mixin.redeploy_node(list(chain.init_nodes)[0:deploy_nodes_number])

    chain_plugin_mixin = ChainPluginMixin(new_chain)

    chain_plugin_mixin.check_block(aide_list=aides)

    # 暂停一个节点
    # TODO 1.aides还是三个,查询数据正常出块,  确实在服务器上已删除节点文件信息
    new_chain.uninstall(random.choices(list(new_chain.init_nodes)))
    chain_plugin_mixin.check_block(aide_list=aides)


@allure.title("Start all nodes normally, and gradually close f")
@pytest.mark.P0
def test_SC_CL_001(chain):
    """
    启动n个节点后，逐渐关闭f(指作弊节点)，则关闭节点的不出块
    原代码：关闭一个作弊节点后 验证其他节点正常出块, get_all_nodes 获取的是8个节点，随便关闭一个？还是要关闭共识节点
    """
    chain_plugin_mixin = ChainPluginMixin(chain)
    chain_plugin_mixin.check_block()
    # 关闭一个共识节点
    init_aides = chain_plugin_mixin.init_aides[0:chain_plugin_mixin.max_byzantine_node]
    init_nodes = [item.node for item in init_aides]
    chain_plugin_mixin.chain.stop(init_nodes)
    chain_plugin_mixin.check_block(chain_plugin_mixin.init_aides[chain_plugin_mixin.max_byzantine_node:])


@allure.title("Start 2f+1 nodes normally, start one after 30 seconds")
@pytest.mark.P2
def test_SC_IV_001(chain, init_aides):
    """
    @describe: 先启动2f+1, 30后再启动1个节点

    @step:
        - 清理链
        - 重新部署三个共识节点,会根据当前传入节点修改创世文件
        - 再部署一个节点,创世文件不改变 genesis_is_reset=False,指定连接节点 static_nodes=[i.enode for i in chain.init_nodes]

    @expect:
        - 部署三个节点 正常出块
        - 后部署一个节点 end_aides_block_number > start_aides_block_number

    @teardown: chain.uninstall() 清理链
    """
    start_aides_block_number: list = get_block_number(init_aides, detail=True)
    logger.info(f"初始节点块高：{start_aides_block_number}")

    _byzantine_node: int = (2 * max_byzantine_node(chain) + 1)

    chain.install(setting.PLATON, setting.NETWORK, genesis_file=setting.GENESIS_FILE,
                  nodes=list(chain.init_nodes)[:_byzantine_node])
    time.sleep(30)
    assert check_block(aides=init_aides[:_byzantine_node], need_number=10, multiple=3)
    start_aides_block_number: list = get_block_number(init_aides[:_byzantine_node], detail=True)
    logger.info(f"链上节点块高：{start_aides_block_number}")

    chain.install(setting.PLATON, setting.NETWORK, genesis_file=setting.GENESIS_FILE, genesis_is_reset=False,
                  static_nodes=[i.enode for i in chain.init_nodes],
                  nodes=list(chain.init_nodes)[_byzantine_node: _byzantine_node + 1])
    assert check_block(aides=init_aides[_byzantine_node:_byzantine_node + 1], need_number=10, multiple=3)

    end_aides_block_number: list = get_block_number(init_aides[:_byzantine_node + 1], detail=True)
    logger.info(f"链上节点块高：{end_aides_block_number}")



    pass


def test_node_block_numbers(chain, aides):
    result = get_block_number(aides)
    logger.info(f"{result}")
