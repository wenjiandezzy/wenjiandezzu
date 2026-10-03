import os
import sys

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(DIR_PATH)

FILE_PATH = {
    'extract': os.path.join(DIR_PATH, 'extract.yaml'),
    'ini': os.path.join(DIR_PATH, 'configs', 'config.ini'),
    'login': os.path.join(DIR_PATH, 'data', 'login.yaml'),  # 新增：data目录路径
}
