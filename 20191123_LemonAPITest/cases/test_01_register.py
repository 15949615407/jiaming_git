import os
import unittest
import re

from scripts.handle_excel import HandleExcel
from libs.ddt import ddt, data
from scripts.handle_yaml import do_yaml
from scripts.handle_log import do_log
from scripts.handle_parameterize import Parameterize
from scripts.handle_request import HandleRequest


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel('register')   # 创建HandleExcel对象
    cases = excel.read_data_obj()     # 获取excel中register表单下的所有数据

    @classmethod
    def setUpClass(cls): # 所有用例执行前, 会被调用一次
        cls.do_request = HandleRequest()    # 创建HandleRequest对象
        cls.do_request.add_headers(do_yaml.read('api', 'version'))  # 添加公共的请求头, url版本号

    @classmethod
    def tearDownClass(cls): # 所有用例执行结束之后, 会被调用一次
        cls.do_request.close()  # 释放session会话资源

    @data(*cases)
    def test_register(self, case):
        # src_data = case.data
        # re.sub(r'{not_existed_tel}', '', src_data)
        # 1. 参数化
        new_data = Parameterize.to_param(case.data)

        # 2. 拼接完整的url
        new_url = do_yaml.read('api', 'prefix') + case.url

        # 3. 向服务器发起请求
        res = self.do_request.send(url=new_url,  # url地址
                                   # method=case.method,    # 请求方法
                                   data=new_data,   # 请求参数
                                   # is_json=True   # 是否以json格式来传递数据, 默认为True
                                   )
        # 将相应报文中的数据转化为字典
        actual_value = res.json()

        # 获取用例的行号
        row = case.case_id + 1
        # 获取预期结果
        # excepted = eval(case.excepted)
        expected_result = case.expected

        msg = case.title    # 获取标题
        success_msg = do_yaml.read('msg', 'success_result')  # 获取用例执行成功的提示
        fail_msg = do_yaml.read('msg', 'fail_result')       # 获取用例执行失败的提示

        try:
            # assertEqual第三个参数为用例执行失败之后的提示信息
            # assertEqual第一个参数为期望值, 第二个参数为实际值
            self.assertEqual(expected_result, actual_value.get('code'), msg=msg)
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
