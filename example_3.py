# -*- coding: UTF-8 -*-
# @Time    : 2020/12/20
# @Author  : xiangyuejia@qq.com
from openc import openc

f = openc('example_3.txt', 'r')
for l in f:
    print(l, end='')
f.close()

f = openc('example_3.txt', 'r')
for l in f:
    print(l, end='')
f.close()
