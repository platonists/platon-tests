"""
测试各个设置下的出块情况
"""
import time
from copy import copy

import allure
import pytest
from dacite import from_dict
from loguru import logger
from platon_env.genesis import Genesis

from setting import setting


def test_debug(aides):
    print(aides[0].platon.chain_id)


@allure.title("Test node interconnections between different init_node founding files")
@pytest.mark.P0
def test_CH_IN_009(init_aide, normal_aide):
    """
    @describe: 测试不同 init_node 创世文件之间的节点互连

    @setup: 获取共识节点 和 标准节点

    @step:
        - 1.部署测试环境(8个)节点
        - 2.获取标准节点 更改 创世文件，上传至服务器并重新部署
        - 3.部署节点连接共识节点
        - 4. net.peerCount 返回当前节点上已经连接的其他节点数量

    @expect:
        - 1.重新部署节点正常运行
        - 2.连接其他节点数量等于0

    @teardown: chain.uninstall() 清理链
    """
    test_node = normal_aide.node
    genesis = Genesis(setting.GENESIS_FILE)
    genesis.fill_init_nodes(nodes=[test_node])
    genesis_13_path = setting.GENESIS_FILE.replace("genesis", "genesis_0.13.0")
    genesis.save(genesis_13_path)
    # 将genesis_13_path 上传至服务并更名 genesis 可手动查看验证
    test_node.install(setting.PLATON, setting.NETWORK, genesis_file=genesis_13_path)
    assert test_node.status()
    normal_aide.admin.add_peer(init_aide.node.enode)
    time.sleep(5)
    assert normal_aide.web3.net.peer_count == 0


@allure.title("Test deployment of a single-node private chain, synchronization of single-node blocks")
@pytest.mark.P0
def test_CH_IN_005(global_test_env):
    test_node = copy(global_test_env.get_a_normal_node())
    logger.info("test node :{}".format(test_node.node_mark))
    genesis_data = global_test_env.genesis_config
    genesis = from_dict(data_class=Genesis, data=genesis_data)
    genesis.config.cbft.initialNodes = [{"node": test_node.enode, "blsPubKey": test_node.blspubkey}]
    file = test_node.local_node_tmp + "/genesis_0.13.0.json"
    genesis.to_file(file)
    test_node.deploy_me(file)
    time.sleep(5)
    assert test_node.block_number > 0, "block height has not increased"
    join_node = copy(global_test_env.get_rand_node())
    logger.info("join node:{}".format(join_node.node_mark))
    join_node.deploy_me(file)
    join_node.admin.addPeer(test_node.enode)
    time.sleep(5)
    assert join_node.block_number > 0, "block height has not increased"
