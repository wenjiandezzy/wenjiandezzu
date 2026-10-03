import pytest
from configs.setting import FILE_PATH
from unit_tools.handle_data.yaml_handle import read_yaml, write_yaml
from unit_tools.handle_data.configParser import Configparser
from unit_tools.sendrequests import SendRequest

conf = Configparser()

yaml_path = FILE_PATH['login']

class TestLogin:
    """登录模块"""

    # 参数传递，将yaml_path里的内容传递给test_login_module函数
    @pytest.mark.parametrize('api_info', read_yaml(yaml_path))
    def test_login_module(self, api_info):
        # 从yaml文件获取接口信息
        # conf_url = conf.get_host('host')
        url = api_info['baseInfo']['url']
        method = api_info['baseInfo']['method']
        headers = api_info['baseInfo']['header']
        req_param = api_info['testCase'][0]['json']
        # 调用接口SendRequest类去执行接口请求
        send = SendRequest()
        res = send.execute_api_request(api_name='登录获取 Token', url=url, method=method,
                                 header=headers, case_name=None, cookie=None, file=None, json=req_param)

        #将接口返回信息转换为json格式
        result_json = res.json()
        print(f'\n接口实际返回信息为：\n{result_json}')
        # print(FILE_PATH['login'])
        #把登录接口的返回值token写入到extract.yaml中
        login_token = {}
        login_token['token'] = result_json['token']
        write_yaml(login_token)


        # # 4. 添加断言（这才是测试的灵魂！）
        # # 断言状态码为 200
        # assert res.status_code == 200, f"接口请求失败，状态码：{res.status_code}"
        # # 断言返回结果中包含 accessToken
        # assert 'accessToken' in result_json, "返回结果中缺失 accessToken"
        # # 断言用户名正确
        # assert result_json['username'] == 'emilys', f"用户名错误，实际返回：{result_json['username']}"


