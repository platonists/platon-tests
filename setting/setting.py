import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NETWORK = 'private'

# 部署链的配置文件
CHAIN_FILE = os.path.join(BASE_DIR, 'env-files/chain_file.yml')
GENESIS_FILE = os.path.join(BASE_DIR, 'env-files/genesis.yml')

# 当前测试版本
PLATON = os.path.join(BASE_DIR, 'env-files/bin/platon')
VERSION = '1.1.1'

# 历史版本，通常使用线上版本     //用于验证从该历史版本升级到测试版本的过程
HISTORY_PLATON = os.path.join(BASE_DIR, 'env-files/bin/history/platon')
HISTORY_VERSION = '1.1.0'

# 治理测试版本
PIP_PKGS_DIR = os.path.join(BASE_DIR, 'env-files/pip-pkgs')
