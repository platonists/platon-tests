
import maintain
from deepdiff import DeepDiff


def _001():
    a = [{'192.168.10.221:6789': 57}, {'192.168.10.224:6789': 57}, {'192.168.10.223:6789': 57}]
    b = [{'192.168.10.221:6789': 108}, {'192.168.10.224:6789': 108}, {'192.168.10.223:6789': 108},
         {'192.168.10.222:6789': 106}]

    res = DeepDiff(a, b)
    print(res)
    for k, v in res.get("values_changed").items():
        assert v.get("old_value") > v.get("new_value")
    pass


# class Assertion:
#     """提供断言方法"""
#
#     @classmethod
#     def _lt(cls, old, new):
#         """
#         新旧可迭代对象数据对比
#         @param old:
#         @param new:
#         @return:
#         """
#         result = DeepDiff(old, new)
#         for k, v in result.get("values_changed").items():
#             assert v.get("old_value") > v.get("new_value")
#         pass


if __name__ == '__main__':
    pass
