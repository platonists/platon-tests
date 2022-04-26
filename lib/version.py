import os
from typing import Tuple

from setting.setting import VERSION, PIP_BIN_DIR


def tuple_version(version: str):
    """ 将str版本转换为tuple形式
    """
    return tuple([int(v) for v in version.split('.')])


def int_version(version: Tuple[int, ...]):
    """ 将tuple版本转换为int形式
    """
    return int.from_bytes(bytes(version), byteorder='big')


class Version:
    major: int
    minor: int
    patch: int

    def __init__(self, name: str, version: str, path: str = None):
        self.name = name
        self.version = version
        self.path = path or os.path.join(PIP_BIN_DIR, f'{self.name}/platon')
        # 私有变量
        self.__tuple = tuple_version(self.version)
        self.__int = int_version(self.__tuple)
        self.major = self.__tuple[0]
        self.minor = self.__tuple[1]
        self.patch = self.__tuple[2]

    def __str__(self):
        return self.version

    def __int__(self):
        return self.__int

    def __iter__(self):
        return self.__tuple


class PipVersions:
    # 正常升级版本
    patch_upgrade_version: Version
    minor_upgrade_version: Version
    major_upgrade_version: Version
    # 跨版本升级版本
    major_upgrade_version: Version
    major_across_version: Version
    # 特殊版本
    min_version: Version
    max_version: Version

    def __init__(self):
        self._set_pip_versions()

    def _set_pip_versions(self, current_version: str = None):
        current_version = current_version or VERSION
        version = Version(current_version)
        # 正常升级版本
        self.patch_upgrade_version = Version(f'{version.major}.{version.minor}.{version.patch + 1}')
        self.minor_upgrade_version = Version(f'{version.major}.{version.minor + 1}.{version.patch + 1}')
        self.major_upgrade_version = Version(f'{version.major + 1}.{version.minor + 1}.{version.patch + 1}')
        # 跨版本升级版本
        self.minor_across_version = Version(f'{version.major}.{version.minor + 2}.{version.patch + 2}')
        self.major_across_version = Version(f'{version.major + 2}.{version.minor + 2}.{version.patch + 2}')
        # 特殊版本
        self.min_version = Version('255.255.255')
        self.max_version = Version('0.0.0')
