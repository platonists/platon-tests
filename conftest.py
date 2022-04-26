
# todo: 增加清理缓存的参数，等待platon_env优化缓存污染问题
# todo: 增加强制部署的选项 （处理端口占用等问题）
def pytest_addoption(parser):
    parser.addoption("--chainFile", action="store", help="chainFile: chain data file")
