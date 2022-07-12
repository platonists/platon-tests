import time
import random

import allure
import pytest
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


@allure.title("Start 2f+1 nodes normally, start one after 50 seconds")
@pytest.mark.P2
def test_SC_IV_001(chain, init_aides):
    """
    先启动2f+1, 50秒后启动1
    """
    _byzantine_node: int = (2 * max_byzantine_node(chain) + 1)
    chain.uninstall()  # 不能使用stop redeploy 进程会被占用

    new_chain = Chain(list(chain.init_nodes)[:_byzantine_node])
    new_chain.install(setting.PLATON, setting.NETWORK,
                      genesis_file=setting.GENESIS_FILE, )
    time.sleep(50)
    start_block_number = get_block_number([Aide(node) for node in new_chain.init_nodes])
    print(start_block_number)
    new_chain.install(setting.PLATON, setting.NETWORK,
                      genesis_file=setting.GENESIS_FILE,
                      nodes=list(chain.init_nodes)[_byzantine_node: _byzantine_node + 1])
    new_chain.init_aides = [Aide(node) for node in list(new_chain.init_nodes)[:_byzantine_node + 1]]
    check_block(aides=new_chain.init_aides, need_number=max(start_block_number) + 10, multiple=2)
    # num = int(2 * global_test_env.max_byzantium + 1)
    # log.info("Deploy {} nodes".format(num))
    # test_nodes = global_test_env.consensus_node_list[0:num]
    # global_test_env.deploy_nodes(node_list=test_nodes, genesis_file=global_test_env.cfg.genesis_tmp)
    # time.sleep(50)
    # start = max(global_test_env.block_numbers(node_list=test_nodes).values())
    # global_test_env.deploy_nodes(global_test_env.consensus_node_list[num:num + 1],
    #                              genesis_file=global_test_env.cfg.genesis_tmp)
    # global_test_env.check_block(need_number=start + 10, multiple=2,
    #                             node_list=global_test_env.consensus_node_list[0:num + 1])
