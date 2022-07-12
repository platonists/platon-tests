import time
from typing import List, Set

from platon_env.genesis import Genesis
from platon_env.node import Node
from platon_env.chain import Chain
from platon_env.utils.executor import concurrent_executor

from lib.aide import Aide
from setting import setting


class ChainPluginMixin(object):

    def __init__(self, chain: Chain):
        self.chain = chain
        # TODO 这个属性可能产生bug 并未当前读取的最新文件,而是系统配置原始文件,这里可以选择传参进来,但是解决方案不优雅
        self.genesis_config = Genesis(setting.GENESIS_FILE)
        self.init_aides = self.init_aides()
        # self.normal_aides = self.normal_aides()
        pass

    def normal_aides(self):
        aide_list = [Aide(node) for node in self.chain.normal_nodes]
        return aide_list

    def init_aides(self):
        aide_list = [Aide(node) for node in self.chain.init_nodes]
        return aide_list

    @classmethod
    def get_block_number(cls, aides: List):
        """
        获取节点对象中区块高度
        @param aides: List[aide_obj]
        @return: 传入节点中 所有区块高度
        """
        return concurrent_executor(aides, 'get_block_number', )

    @classmethod
    def get_max_cheat_node(cls, init_nodes: Set[Node]) -> int:
        """
        获取作弊节点的最大数量
        @param init_nodes: 共识节点列表
        @return: 最大作弊节点值 int
        """
        num = len(init_nodes)
        if num < 3:
            raise Exception("the number of consensus nodes is less than 3")
        if num == 3:
            return 0
        f = (num - 1) / 3
        return int(f)

    @property
    def max_byzantine_node(self) -> int:
        """最大拜占庭节点数"""
        return self.get_max_cheat_node(self.chain.init_nodes)

    def check_block(self, aide_list: List[Aide] = None, need_number=10, multiple=3):
        """
        验证链上节点出块
        @param need_number: 出块总数量
        @param multiple: 倍数
        @param aide_list: 节点列表
        @return:
        """
        if aide_list is None:
            # TODO 为什么self.chain.nodes 就无法成功
            aide_list = self.init_aides
        use_time = int(need_number * self.block_interval * multiple)
        while use_time:
            if max(self.get_block_number(aide_list)) < need_number:
                time.sleep(1)
                use_time -= 1
                continue
            return
        raise Exception("The environment is not working properly")

    @property
    def block_interval(self) -> int:
        """
        Block interval
        """
        period = self.genesis_config.data["config"]["cbft"].get("period")
        amount = self.genesis_config.data["config"]["cbft"].get("amount")
        return int(period / 1000 / amount)

    def redeploy_node(self, nodes: list):
        self.chain.uninstall()
        _ = [self.chain.remove_process(item) for item in list(self.chain.processes.keys())]

        # new object  (重置类属性) hosts: init_nodes: normal_nodes: Set
        new_chain = Chain(nodes)
        new_chain.install(setting.PLATON, setting.NETWORK,
                          genesis_file=setting.GENESIS_FILE,
                          nodes=nodes)

        aides = [Aide(node) for node in nodes]

        return new_chain, aides



