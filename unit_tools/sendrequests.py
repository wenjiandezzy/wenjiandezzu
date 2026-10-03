import re
from http.client import responses
from unit_tools.handle_data.yaml_handle import read_yaml, write_yaml
import requests
from requests import utils

class SendRequest:

    def __init__(self):
        pass

    @classmethod
    def _text_encode(cls, res_text):
        """
        处理接口返回值出现uncode编码时，如：\\u767b
        :param res_text:
        :return:
        """
        match = re.search(r"\\u[0-9a-fA-F]{4}", res_text)
        if match:
            result = res_text.encode().decode('unicode-escape')
        else:
            result = res_text
        return result


    def send_request(self, **kwargs):
        #创建一个会话
        session = requests.Session()
        response = None
        try:
            response = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(response.cookies)
            if set_cookie:
                # print(f'获取到cookie：{set_cookie}')
                write_yaml({'获取到cookie': set_cookie})
            res = self._text_encode(response.text)
            # print(res)
        except requests.exceptions.ConnectionError:
            print('接口请求异常，可能是request的连接数过多或者速度过快导致程序报错。')
        except requests.exceptions.RequestException as e:
            print(f'请求异常，请检查系统或数据是否正常,原因：{e}')

        return response

    def execute_api_request(self, api_name, url, method, header, case_name, cookie=None, file=None, **kwargs):
        """
        发起接口请求
        :param api_name: 接口名称
        :param url: 接口地址
        :param method: 请求方法
        :param header: 请求头
        :param case_name: 测试用例名称
        :param cookie: cookie
        :param file: 文件上传
        :param kwargs: 未知数量的关键字参数
        :return:
        """
        # 从 kwargs 中取出 timeout，如果没有则使用默认值 10
        timeout = kwargs.pop('timeout', 10)
        # 从 kwargs 中取出 verify，如果没有则使用默认值 False
        verify = kwargs.pop('verify', False)

        resp = requests.request(method=method,
                                url=url,
                                headers=header,
                                cookies=cookie,
                                files=file,
                                timeout=timeout,
                                verify=verify,
                                **kwargs)

        #添加写入 Cookie 的逻辑
        # set_cookie = requests.utils.dict_from_cookiejar(resp.cookies)
        # if set_cookie:
        #     write_yaml({'获取到cookie': set_cookie},mode='w')

        return resp

if __name__ == '__main__':
    from unit_tools.handle_data import configParser
    import requests

    # url_login = 'url'
    # header_login = 'header'
    # data_login = {
    #     'username': 'username',
    #     'password': 'password',
    # }
    # url = 'http://127.0.0.1:8787' + data['baseInfo']['url']

    data = read_yaml('../../test_project/data/login.yaml')[0]
    url = data['baseInfo']['url']
    method = data['baseInfo']['method']
    header = data['baseInfo']['header']
    req_data = data['testCase'][0]['data']
    send = SendRequest()
    res = send.execute_api_request(api_name=None, url=url, method=method, header=header, case_name=None,
                                   json=req_data)

    if res.status_code == 200:
        res_json = res.json()

        # 构建提取出来的变量字典
        extract_data = {
            'accessToken': res_json.get('accessToken'),
            'user_id': res_json.get('id'),
            'username': res_json.get('username'),
            # 模拟一个列表变量，供后续随机取值测试
            'usernames': ['emilys', 'michaelw', 'sophiab']
        }

        # 写入 extract.yaml (使用 mode='w' 覆盖，保持文件干净)
        write_yaml(extract_data, mode='w')

        print('已成功提取变量并写入extract.yaml：')
    else:
        print(f'请求失败，状态码：{res.status_code}')