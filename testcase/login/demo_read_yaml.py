from configs.setting import FILE_PATH
from unit_tools.handle_data.yaml_handle import read_yaml

yaml_path = FILE_PATH['login']
data_list = read_yaml(yaml_path)
api_info = data_list[0]
print('处理之前：', api_info)
req_param = api_info['testCase'][0]['data']
print('处理之后：',req_param)
