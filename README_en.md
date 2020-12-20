# openC

[English version]()

> 背景：私有化部署时，需要对数据资产进行加密。
> Background: When privatized deployment, data assets need to be encrypted.

将代码中的open替换为openc即完成对文件的加密
Replace open in the code with openc to complete the file encryption

## 快速使用
1. 安装依赖 ```pip install pycrypto```
2. 导入类```from openc import openc```
3. 将文件里的```open```替换为```openc```
4. 运行一次代码（openC 会自动生成加密后的文件)
5. 删掉未加密的原文件
> 如果将replace参数设置为True，将直接用加密文件覆盖原文件（请提前做好备份），因此无需做上述的第5步。

## 简单介绍
1. 如果没有对应的加密文件：生成对应的加密文件
2. 如果已有对应的加密文件：生成临时解密文件，读数据，删除临时解密文件

## 需要注意
1. 使用前请修改openc的默认密钥，以免密钥雷同
2. 请配合Cython等工具对.py文件加密，避免明文泄露密钥
3. openC在读数据时会临时解密文件，默认解密在原路径下，可以指定一个更隐秘的路径

## 例子

### 例子1
- 最基础的使用方法：将open替换为openc
- 会生成加密文件```example_1_crypto.txt```，之后请删除原文件```example_1.txt```

```python example_1.py```
> ```python
> from openc import openc
> with openc('example_1.txt', 'r') as f:
>     print(f.readlines())
> ```

### 例子2
- 用```replace```参数，直接用加密文件覆盖掉原文件
- 请一定提前备份原文件

```python example_2.py```
> ```python
> from openc import openc
> with openc('example_2.txt', 'r', replace=True) as f:
>     print(f.readlines())
> ```

### 例子3
- 对其他oi方法的支持

```python example_3.py```
> ```python
> from openc import openc
> f = openc('example_3.txt', 'r')
> for l in f:
>     print(l, end='')
> f.close()
> ```

## 参数
```python
'''
:param mode: open方法的参数
:param buffering: open方法的参数
:param encoding: open方法的参数
:param errors: open方法的参数
:param newline: open方法的参数
:param closefd: open方法的参数
:param file: 原文件
:param crypt_path: 加密文件所存放的位置
:param decrypt_path: 临时解密文件所存放的位置
:param key: 加密用的密钥
:param suffix: 为密后文件的文件名添加额外后缀
:param redo_crypto: 重新生成加密文件。默认为False。
                    不推荐使用本参数，如果原文件更新了，直接删除旧的加密文件即可。
:param do_crypto: 进行加密。默认为True。如果为False，openC等同于open
:param replace: 用加密文件替换原文件，即加密文件与原文件同名且同路径。
                会删除原文件，请谨慎使用。
                优点是无需修改make指令，只要将所有open替换为openC即可
:param remove_ori: 加密后删除原文件。请谨慎使用。
:param display_warning: 是否输出警告。
'''
```

## todo
- 本方案目前只支持用open方法
- 目前仅测试了部分读方式open后的oi方法，有待进一步测试
- replace方法的bug：因为目前没有flag表明文件是否加密过，目前的方案是，
尝试解压一次如果出错则认为是原文件，这在原文件长度是16字的整倍数时会出错，
我目前还没想出来如何处理这个问题

## LICENSE
MIT License