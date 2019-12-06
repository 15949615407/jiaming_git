# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/11/16 9:42 
  @Auth : 可优
  @File : handle_path.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import os

# one_path = os.path.abspath(__file__)
# two_path = os.path.dirname(one_path)
# three_path = os.path.dirname(two_path)
# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取配置文件所在的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

# 获取配置文件所在的路径
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, 'testcase.yaml')

# 获取日志文件所在的目录路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 获取报告文件所在的目录路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 获取excel文件所在的目录路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# 获取用户账号所在配置文件的路径
USER_ACCOUNTS_FILE_PATH = os.path.join(CONFIGS_DIR, 'user_account.yaml')

# 测试用例模块所在目录路径
CASES_DIR = os.path.join(BASE_DIR, 'cases')
pass
