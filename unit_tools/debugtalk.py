import random
import re
import time

from unit_tools.handle_data.yaml_handle import get_extract_yaml

class DebugTalk:

    def get_extract_data(self, node_name, out_format=None):
        """
        获取extract.yaml数据，首先判断out_format是否为数字类型，如果不是就获取下一个节点的value
        :param node_name:extract.yaml文件中的key
        :param out_format:str类型，0：随机去读取；-1：读取全部数据，返回字符串格式；-2：读取全部，返回列表格式；其他值就按顺序读取
        :return:
        """
        data = get_extract_yaml(node_name)

        # 1. 直接从 yaml 中获取数据
        if data is None:
            print(f"extract.yaml 中未找到 {node_name}")
            return None


        # 2. 如果数据是普通字符串或数字（比如 accessToken, user_id），直接返回，不需要处理 out_format
        if not isinstance(data, list):
            return data

        # 3. 如果数据是列表，且传入了 out_format 参数，则进行动态处理
        if out_format is not None and bool(re.compile(r'^[+-]?\d+$').match(str(out_format))):
            out_format = int(out_format)

            if out_format == 0:
                return random.choice(data)
            elif out_format == -1:
                return ','.join(map(str, data))
            elif out_format == -2:
                return [str(item) for item in data]
            else:
            # 按顺序读取 (索引从1开始)
                if 0 < out_format <= len(data):
                    return data[out_format - 1]
                else:
                    print(f"索引{out_format}越界，当前列表长度{len(data)}")
                    return None
        return data


    # @classmethod
    def get_now_time(self):
        return time.time()

    def get_header(self, params_type):
        """
        获取请求头
        :param params_type: 参数类型，如data或者json
        :return:
        """
        header_mapping = {
            'data':{'Content': 'application/x-www-form-urlencoded; charset=utf-8'},
            'json':{'Content-Type': 'application/json; charset=utf-8'},
        }
        header = header_mapping.get(params_type)
        if header is None:
            raise ValueError('不支持其他类型的请求头设置')
        return header


    def seq_read(self, data, randoms):
        """
        获取extract.yaml，第二个参数不为0，-1，-2的情况下
        :param data:
        :param randoms:
        :return:
        """
        if randoms not in [0, -1, -2]:
            return data[randoms-1]
        else:
            return None

if __name__ == '__main__':
    debug = DebugTalk()
    res = debug.get_extract_data('usernames', -2)
    print(res)