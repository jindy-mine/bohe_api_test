import re
from common.handle_config import conf


class EnvData:
    aaa='1www'
    pass


def replace_data(data):
    """替换数据"""

    while re.search("#(.*?)#", data):
        res = re.search("#(.*?)#", data)
        # 返回的是一个匹配对象
        # 获取匹配到的数据
        key = res.group()
        # 获取匹配规则中括号里面的内容
        item = res.group(1)
        try:
            # 获取配置文件中对应的值
            value = conf.get("bohe", item)
        except:
            value = getattr(EnvData, item)

        data = data.replace(key, value)
    return data


data = '{"user":#user#,"pwd":#pwd#,"name":"#name#","age":"#age#","aaa":"#aaa#"}'
res = replace_data(data)
print(res)
