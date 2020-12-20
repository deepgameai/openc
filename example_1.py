# -*- coding: UTF-8 -*-
# @Time    : 2020/12/20
# @Author  : xiangyuejia@qq.com
from openc import openc

with openc('example_1.txt', 'r') as f:
    print(f.readlines())

with openc('example_1.txt', 'r') as f:
    print(f.readlines())
