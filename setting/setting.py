import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCHEME = 'ws'
NETWORK = 'private'

# 部署链的配置文件
CHAIN_FILE = os.path.join(BASE_DIR, 'env-files/chain_file.yml')
GENESIS_FILE = os.path.join(BASE_DIR, 'env-files/genesis.json')

# 当前测试版本
PLATON = os.path.join(BASE_DIR, 'env-files/bin/alaya')
VERSION = '0.16.2'

# 历史版本，通常使用线上版本，用于验证从该历史版本升级到测试版本的过程
HISTORY_PLATON = os.path.join(BASE_DIR, 'env-files/bin/history/platon')
HISTORY_VERSION = '1.1.0'

# 治理测试版本
PIP_PKGS_DIR = os.path.join(BASE_DIR, 'env-files/pip-pkgs')

# 内置钱包地址
Master_account = 'atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0'
Master_prikey = 'f51ca759562e1daf9e5302d121f933a8152915d34fcbc27e542baf256b5e4b74'
Incentive_pool = 'atp1zqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqr5jy24r'
cdfAccount = 'atp1ur2hg0u9wt5qenmkcxlp7ysvaw6yupt4vll2fq'
cdfAccount_prikey = '64bc85af4fa0e165a1753b762b1f45017dd66955e2f8eea00333db352198b77e'
platonFundAccount = 'atp1s0vntlngyuxtc04sj0tsp785svknk2qdlazpyt'
platonFundAccount_prikey = '5c76634db529cb19871f56f12564d52cfe66529cd2ca658ab61b30010d5415d3'





