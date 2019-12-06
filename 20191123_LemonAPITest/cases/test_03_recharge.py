import unittest
import json

from libs.ddt import ddt, data
from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import do_yaml
from scripts.handle_request import HandleRequest
from scripts.handle_parameterize import Parameterize
from scripts.handle_mysql import HandleMysql
from scripts.handle_log import do_log


@ddt
class TestRecharge(unittest.TestCase):
    """
    测试充值功能
    """
    excel = HandleExcel("recharge")
    cases = excel.read_data_obj()

    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()  # 创建HandleRequest对象
        cls.do_request.add_headers(do_yaml.read('api', 'version'))  # 添加公共的请求头, url版本号
        cls.do_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        cls.do_mysql.close()

    @data(*cases)
    def test_recharge(self, case):
        # 1. 参数化
        new_data = Parameterize.to_param(case.data)

        # 2. 拼接完整的url
        new_url = do_yaml.read('api', 'prefix') + case.url

        check_sql = case.check_sql  # 取出check_sql
        if check_sql:   # 如果check_sql不为空, 则代表当前用例需要进行数据校验
            check_sql = Parameterize.to_param(check_sql)  # 将check_sql进行参数化
            mysql_data = self.do_mysql.run(check_sql)   # 执行sql
            amount_before = float(mysql_data['leave_amount'])    # 不是float类型, 也不是int类型, 是decimal类型
            # 由于使用float转化之后的数, 有可能小数位数超过2位, 需要使用round保留2位小数
            amount_before = round(amount_before, 2)

        # 3. 向服务器发起请求
        # 进行充值
        res = self.do_request.send(url=new_url,  # url地址
                                   # method=case.method,    # 请求方法
                                   data=new_data,  # 请求参数
                                   # is_json=True   # 是否以json格式来传递数据, 默认为True
                                   )
        # 将相应报文中的数据转化为字典
        actual_value = res.json()

        # 获取用例的行号
        row = case.case_id + 1
        # 将expected期望值转化为字典
        expected_result = case.expected

        msg = case.title  # 获取标题
        success_msg = do_yaml.read('msg', 'success_result')  # 获取用例执行成功的提示
        fail_msg = do_yaml.read('msg', 'fail_result')  # 获取用例执行失败的提示

        try:
            self.assertEqual(expected_result, actual_value.get('code'), msg=msg)

            # 如果check_sql不为空, 说明要进行数据校验
            if check_sql:
                mysql_data = self.do_mysql.run(sql=check_sql)
                amount_after = float(mysql_data['leave_amount'])  # 不是float浮点数, 更不是int类型, 而是decimal数据类型
                amount_after = round(amount_after, 2)

                one_dict = json.loads(new_data, encoding='utf-8')
                currrent_recharge_amount = one_dict['amount']
                actual_amount = round(amount_before + currrent_recharge_amount, 2)
                self.assertEqual(actual_amount, amount_after, msg="数据库中充值的金额有误")

        except AssertionError as e:
            # 将相应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "result_col"),
                                  value=fail_msg)
            # do_log.error("断言异常: {}".format(e))
            do_log.error(f"{msg}, 执行的结果为: {fail_msg}\n具体异常为: {e}\n")
            raise e
        else:
            # 如果登录接口断言成功, 则取出token, 并添加到公共请求头中
            if 'token_info' in res.text:
                token = actual_value['data']['token_info']['token']
                headers = {"Authorization": "Bearer " + token}
                self.do_request.add_headers(headers)

            # 将相应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col
            self.excel.write_data(row=row,
                                  column=do_yaml.read("excel", "result_col"),
                                  value=success_msg)

            do_log.info(f"{msg}, 执行的结果为: {success_msg}\n")


if __name__ == '__main__':
    unittest.main()
