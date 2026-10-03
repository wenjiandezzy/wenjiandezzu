import yaml
from configs.setting import FILE_PATH


def read_yaml(yaml_path):
    """
    读取yaml文件数据
    :param yaml_path:文件路径
    :return:
    """
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data
    except UnicodeDecodeError:
        print(f'{yaml_path}文件编码格式错误，--尝试使用utf-8去解码YAML文件时发生错误，请确保yaml文件是utf-8格式')
    except Exception as e:
        print(f'读取{yaml_path}文件时出现异常，原因：{e}')

def write_yaml(value, mode = 'a'):
    """
    向extract.yaml写入数据
    :param value:(dict)写入的数据，必须为字典类型
    :param mode: 'a'追加，'w'覆盖(默认追加)
    :return:
    """
    if not isinstance(value, dict):
        print(f'写入的数据类型必须为字典')
        return
    file_path = FILE_PATH['extract']
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            yaml.dump(value, f, allow_unicode=True, sort_keys=False)
    except Exception as e:
        print(f'写入yaml文件出现异常，原因是{e}')

def clear_yaml():
    """
    清空yaml文件
    :return:
    """
    with open(FILE_PATH['extract'], 'w') as f:
        f.truncate()

def get_extract_yaml(node_name):
    """
    用于获取extract.yaml文件的数据
    :param node_name: extract.yaml中的key(如'accessToken', 'usernames')
    :return:
    """
    file_path = FILE_PATH['extract']
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            extract_data = yaml.safe_load(file)

            if extract_data is None or not isinstance(extract_data, dict):
                return None

            return extract_data.get(node_name)

    except Exception as e:
        print(f'Error:读取yaml文件失败 --{file_path}--{e}')
        return None



if __name__ == '__main__':
    # write_yaml({'name': 'zzy'})
    # res = read_yaml('../../extract.yaml')
    res = get_extract_yaml('accessToken')
    print(res)
    # clear_yaml()
    # print(res)
    # get_extract_yaml('zzy')

