"""
=========================================
Author:薄咊
Time:2020/3/18  20:18
==========================================
"""
from configparser import ConfigParser
from common.handle_path import CONF_FILENAME


# 封装配置文件
class HandleConfig(ConfigParser):
    """配置文件解析器类的封装"""

    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding="utf8")


conf = HandleConfig(CONF_FILENAME)

# if __name__ == '__main__':
#     res = conf.get("mysql", "host")
#     print(res)
