# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/11/16 11:11 
  @Auth : 可优
  @File : handle_re.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import re

# 正则表达式相当于一个模子, 可以拿这个模子去把符合这个模子的内容全部找出来
from scripts.handle_mysql import HandleMysql

# 1. 创建待替换的字符串
one_str = '{"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "KeYou"}'

# 2. 创建正则表达式
# re.match方法
# a. 正则表达式中一定要加r, 如果有些字符有特殊含义, 需要在前面加一个\
# re_str = r'{not_existed_tel}'
# b. match方法第一个参数为正则表达式, 第二个参数为待查询的字符串
# c. match方法只能从头开始匹配
# d. 如果匹配不上, 会返回None
# f. 如果能匹配上, 会返回Match对象
# mtch = re.match(r'${not_existed_tel}', one_str)
# 可以使用mtch.group()获取匹配成功之后的值
# mtch = re.match(r'{"mobile_phone": "{not_existed_tel}', one_str)

# 3. re.search方法
# search方法, 不用从头开始匹配, 只要能匹配上, 就直接返回
# 如果能匹配上, 返回Match
# 如果匹配不上, 会返回None
# 可以使用mtch.group()获取匹配成功之后的值
# mtch = re.search(r'{not_existed_tel}', one_str)

# 3. re.sub方法
# sub方法, 第一个参数为正则表达式字符串, 第二个参数为新的值(字符串),
# 第三个参数为待替换的字符串(原始字符串)
# 如果能匹配上, 会返回替换之后的值(一定为字符串类型)
# 如果匹配不上, 会返回原始字符
res = re.sub(r'{not_existed_tel}', '18822223333', one_str)


# 在项目中search方法和sub方法会合在一起用
# 如果one_str原始字符串中能匹配{not_existed_tel}, 则if条件为True, 否则if为False
if re.search('{not_existed_tel}', one_str):
    res = re.sub(r'{not_existed_tel}', '18822223333', one_str)

# split
# findall
# finditer

do_mysql = HandleMysql()
real_existed_tel = do_mysql.create_not_existed_mobile()

do_mysql.close()
