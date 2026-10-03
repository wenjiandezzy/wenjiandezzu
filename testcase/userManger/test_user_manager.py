import pytest
from configs.setting import FILE_PATH
from unit_tools.handle_data.configParser import Configparser

conf = Configparser()

class TestUserManager:
    """用户管理模块"""

    @pytest.mark.parametrize()
    def test_user_add(self, api_info):
        pass