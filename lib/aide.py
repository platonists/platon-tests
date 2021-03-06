from typing import TYPE_CHECKING

from platon_aide import Aide

from setting.setting import SCHEME

if TYPE_CHECKING:
    from platon_env.base.host import Host
    from platon_env.node import Node


class Aide(Aide):
    node: 'Node'
    host: 'Host'

    def __init__(self, node: 'Node'):
        self.node = node
        self.host = node.host
        super().__init__(node.rpc(SCHEME), node.gql())
