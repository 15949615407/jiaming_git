# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/11/19 20:53 
  @Auth : 可优
  @File : handle_parameterize.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import re

from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import USER_ACCOUNTS_FILE_PATH
# from cases.test_05_invest import load_id


class Parameterize:
    """
    参数化类
    """
    not_existed_tel_pattern = r'{not_existed_tel}'  # 未注册手机号
    not_existed_id_pattern = "{not_existed_id}"     # 不存在的用户id

    invest_user_tel_pattern = r'{invest_user_tel}'  # 投资人手机号
    invest_user_pwd_pattern = r'{invest_user_pwd}'  # 投资人密码
    invest_user_id_pattern = r'{invest_user_id}'    # 投资人用户id

    # 借款人相关正则表达式
    borrow_user_id_pattern = '{borrow_user_id}'  # 借款用户id
    borrow_user_tel_pattern = '{borrow_user_tel}'  # 借款人手机号
    borrow_user_pwd_pattern = '{borrow_user_pwd}'  # 借款人密码

    loan_id_pattern = r'{loan_id}'

    do_user_account = HandleYaml(USER_ACCOUNTS_FILE_PATH)

    @classmethod
    def to_param(cls, data):

        # 不存在的手机号替换
        if re.search(cls.not_existed_tel_pattern, data):
            do_mysql = HandleMysql()
            data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_existed_mobile(), data)
            do_mysql.close()

        # 投资人手机号替换
        if re.search(cls.invest_user_tel_pattern, data):
            # do_user_account = HandleYaml(USER_ACCOUNTS_FILE_PATH)
            invest_user_tel = cls.do_user_account.read('invest', 'mobile_phone')
            data = re.sub(cls.invest_user_tel_pattern, invest_user_tel, data)

        # 投资人密码替换
        if re.search(cls.invest_user_pwd_pattern, data):
            invest_user_pwd = cls.do_user_account.read('invest', 'pwd')
            data = re.sub(cls.invest_user_pwd_pattern, invest_user_pwd, data)

        # 投资人id替换
        if re.search(cls.invest_user_id_pattern, data):
            invest_user_id = cls.do_user_account.read('invest', 'id')
            # 投资人id为int类型, 要转化为str类型
            data = re.sub(cls.invest_user_id_pattern, str(invest_user_id), data)

        # 不存在的用户id替换
        if re.search(cls.not_existed_id_pattern, data):
            do_mysql = HandleMysql()

            sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"
            not_existed_id = do_mysql.run(sql).get('id') + 1  # 获取最大的用户id + 1
            data = re.sub(cls.not_existed_id_pattern, str(not_existed_id), data)
            do_mysql.close()

        # 借款人id替换
        if re.search(cls.borrow_user_id_pattern, data):
            borrow_user_id = cls.do_user_account.read("borrow", "id")  # 获取已经注册的借款人用户id
            data = re.sub(cls.borrow_user_id_pattern, str(borrow_user_id), data)

        # 借款人手机号替换
        if re.search(cls.borrow_user_tel_pattern, data):
            borrow_user_mobile = cls.do_user_account.read("borrow", "mobile_phone")  # 获取已经注册的借款人手机号
            data = re.sub(cls.borrow_user_tel_pattern, borrow_user_mobile, data)

        # 借款人密码替换
        if re.search(cls.borrow_user_pwd_pattern, data):
            borrow_user_pwd = cls.do_user_account.read("borrow", "pwd")  # 获取已经注册的借款人密码
            data = re.sub(cls.borrow_user_pwd_pattern, borrow_user_pwd, data)

        # load_id替换
        if re.search(cls.loan_id_pattern, data):
            loan_id = getattr(cls, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)

        return data


if __name__ == '__main__':
    # 注册接口参数化
    one_str = '{"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "KeYou"}'
    two_str = '{"mobile_phone": "", "pwd": "12345678"}'
    three_str = '{"mobile_phone": "{not_existed_tel}", "pwd": "12345678901234567", "reg_name": "KeYou"}'
    four_str = '{"mobile_phone": "{invest_user_tel}", "pwd": "12345678", "reg_name": "KeYou"}'

    # 登录接口参数化
    five_str = '{"mobile_phone":"{invest_user_tel}","pwd":"{invest_user_pwd}"}'
    six_str = '{"pwd":"{invest_user_pwd}"}'

    # param = Parameterize()
    # print(param.to_param(one_str))
    # print(param.to_param(two_str))
    # print(param.to_param(three_str))
    # print(param.to_param(four_str))

    print(Parameterize.to_param(one_str))
    print(Parameterize.to_param(two_str))
    print(Parameterize.to_param(three_str))
    print(Parameterize.to_param(four_str))
    print(Parameterize.to_param(five_str))
    print(Parameterize.to_param(six_str))
