import json
import re

from unit_tools.debugtalk import DebugTalk
from unit_tools.handle_data.yaml_handle import read_yaml
from unit_tools.handle_data.configParser import Configparser
from unit_tools.sendrequests import SendRequest

class RequestsBase:

    def __init__(self):
        self.conf = Configparser()
        self.send_request = SendRequest()


    def parse_and_replace_variables(self, yml_data):
        """
        解析并替换yaml数据中的变量引用，如：${get_extract_data(usernames, 0)}
        :param yml_data:解析的yaml数据
        :return: 返回的是dict类型
        """
        yml_data_str = yml_data if isinstance(yml_data, str) else json.dumps(yml_data, ensure_ascii=False)
        print(f'解析前：{yml_data_str}')

        max_iterations = 20
        iteration = 0

        # for 循环面对嵌套 ${...} 时可能会失效，采用while循环配合最大迭代次数防止死循环
        while '${' in yml_data_str and '}' in yml_data_str and iteration < max_iterations:
            start_index = yml_data_str.index('$')
            end_index = yml_data_str.index('}', start_index)
            variable_data = yml_data_str[start_index:end_index + 1]

        # for _ in range(yml_data_str.count('${')):
        #     if '${' in yml_data_str and '}' in yml_data_str:
        #         start_index = yml_data_str.index('$')
        #         end_index = yml_data_str.index('}', start_index)
        #         variable_data = yml_data_str[start_index:end_index + 1]

            #使用正则表达式提取函数名和参数
            match = re.match(r'\$\{(\w+)\((.*?)\)\}', variable_data)
            if match:
                func_name, func_params = match.groups()
                func_params = func_params.split(',') if func_params else []
                # print(func_params)
                # print(func_name)

                #使用面向对象反射getattr调用函数
                extract_data = getattr(DebugTalk(), func_name)(*func_params)
                print(f'提取到的结果：{extract_data}')

                #使用正则表达式替换原始字符中的变量引用为调用后的结果
                yml_data_str = re.sub(re.escape(variable_data), str(extract_data), yml_data_str)


        #还原数据，将其转换为字典类型
        try:
            data = json.loads(yml_data_str)
        except json.JSONDecodeError:
            data = yml_data_str

        return data

    def execute_test_cases(self, api_info):
        """
        规范yaml接口信息，执行接口、提取结果以及断言操作
        :param api_info:yaml里面的接口信息
        :return:
        """
        # print(api_info)
        try:
            #处理baseInfo里面的数据
            # conf_host = self.conf.get_host('host')
            url = api_info['baseInfo']['url']
            api_name = api_info['baseInfo']['api_name']
            method = api_info['baseInfo']['method']

            header = api_info['baseInfo'].get('header', None)
            if header is not None:
                header = self.parse_and_replace_variables(header) if isinstance(header, str) else header

            cookies = api_info['baseInfo'].get('cookies', None)
            if cookies is not None:
                cookies = self.parse_and_replace_variables(cookies) if isinstance(cookies, str) else cookies

            #处理testCase下面的数据
            for testcase in api_info['testCase']:
                case_name = testcase.pop('case_name')
                print(f'用例名称{case_name}')
                #通过变量引用处理断言结果
                value_result = self.parse_and_replace_variables(testcase.get('validation'))
                testcase['validation'] = value_result
                validation = testcase.pop('validation')
                #处理接口返回值提取部分
                extract, extract_list = testcase.pop('extract', None), testcase.pop('extract_list', None)

                #处理参数类型和请求参数
                for param_type, param_value in testcase.items():
                    if param_type in ['params', 'data', 'json']:
                        request_params = self.parse_and_replace_variables(param_value)
                        testcase[param_type] = request_params


                print(testcase)
                file = None
                response = self.send_request.execute_api_request(api_name = api_name,
                                                                 url = url,
                                                                 method = method,
                                                                 header = header,
                                                                 case_name = case_name,
                                                                 cookie = cookies,
                                                                 file = None,
                                                                 **testcase)
                status_code = response.status_code
                


        except Exception as e:
            print(f'未知异常：{e}')



if __name__ == '__main__':
    api_info = read_yaml(r'../../test_project/data/login.yaml')[0]
    req = RequestsBase()
    # res = req.parse_and_replace_variables(api_info)
    # print(f'解析后：{res}')
    req.execute_test_cases(api_info)


"""
读取 YAML：拿到adduser.yaml中testCase 里的字典
转为字符串：变成 {"username": "${get_extract_data(username)}", "password": "emilyspass", ...}
正则匹配：找到 ${get_extract_data(username)}
解析与反射：提取出 func_name="get_extract_data"，参数为 ["username"]。通过 getattr 调用 DebugTalk 里的方法
读取 extract.yaml：DebugTalk 去读 extract.yaml 里的 username 值（比如 emilys）
替换：把原来的字符串替换成 emilys
还原：字符串重新变回字典，username 变成了 emilys，最后发送给 execute_api_request 发请求
"""