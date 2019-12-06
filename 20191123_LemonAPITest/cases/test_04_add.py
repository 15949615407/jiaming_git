import unittest
import json

from libs.ddt import ddt, data
from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import do_yaml
from scripts.handle_request import HandleRequest
from scripts.handle_parameterize import Parameterize
from scripts.handle_log import do_log
from scripts.handle_mysql import HandleMysql


@ddt
class TestAdd(unittest.TestCase):
    """
    加标接口测试类
    """
    do_excel = HandleExcel("add")
    cases = do_excel.read_data_obj()

    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        api_version = do_yaml.read("api", "version")
        cls.do_request.add_headers(api_version)
        cls.do_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        cls.do_mysql.close()

    @data(*cases)
    def test_add(self, case):
        # 1. 参数化
        new_data = Parameterize.to_param(case.data)

        # 2. 拼接完整的url
        new_url = do_yaml.read('api', 'prefix') + case.url

        # 3. 向服务器发起请求
        res = self.do_request.send(url=new_url,
                                   data=new_data)

        # 将相应报文中的数据转化为字典
        actual_value = res.json()

        row = case.case_id + 1
        expect_result = case.expected

        msg = case.title  # 获取用例标题
        success_msg = do_yaml.read("msg", "success_result")  # 获取用例执行成功的提示信息
        fail_msg = do_yaml.read("msg", "fail_result")  # 获取用例执行失败的提示信息

        try:
            self.assertEqual(expect_result, actual_value.get('code'), msg=msg)

        except AssertionError as e:
            # 将执行结果写入到日志中
            do_log.error(f"{msg}, 执行的结果为: {fail_msg}\n具体异常为: {e}\n")

            # 将响应数据写入excel
            self.do_excel.write_data(row=row,
                                     column=do_yaml.read("excel", "actual_col"),
                                     value=res.text)
            # 将测试结果写入excel
            self.do_excel.write_data(row=row,
                                     column=do_yaml.read("excel", "result_col"),
                                     value=fail_msg)
            raise e
        else:
            # 如果登录接口断言成功, 则取出token, 并添加到公共请求头中
            if 'token_info' in res.text:
                token = actual_value['data']['token_info']['token']
                headers = {"Authorization": "Bearer " + token}
                self.do_request.add_headers(headers)

            # 将执行结果写入到日志中
            do_log.info(f"{msg}, 执行的结果为: {success_msg}\n")
            # 将响应数据写入excel
            self.do_excel.write_data(row=row,
                                     column=do_yaml.read("excel", "actual_col"),
                                     value=res.text)
            # 将测试结果写入excel
            self.do_excel.write_data(row=row,
                                     column=do_yaml.read("excel", "result_col"),
                                     value=success_msg)


if __name__ == '__main__':
    unittest.main()
