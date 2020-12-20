# -*- coding: UTF-8 -*-
# @Time    : 2020/12/20
# @Author  : xiangyuejia@qq.com
from openc import openc

with openc('example_2.txt', 'r', replace=True) as f:
    print(f.readlines())

with openc('example_2.txt', 'r', replace=True) as f:
    print(f.readlines())
