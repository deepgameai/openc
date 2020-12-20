# -*- coding: UTF-8 -*-
# @Time    : 2020/12/18
# @Author  : xiangyuejia@qq.com
import os
import warnings
from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr


def add_to_16(text):
    if len(text) % 16:
        add = 16 - (len(text) % 16)
    else:
        add = 0
    text = text + (bchr(0x01) * add)
    return text


def do_open(
        file,
        mode='r',
        buffering=None,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
):
    # 由于buffering=None时open会报错所以要分别处理
    if buffering:
        return open(
            file,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
        )
    else:
        return open(
            file,
            mode=mode,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
        )


class openc:
    def __init__(
            self,
            file,
            mode='r',
            buffering=None,
            encoding=None,
            errors=None,
            newline=None,
            closefd=True,
            crypt_path=None,
            decrypt_path=None,
            key='a4a2c12ae250ab3a01b3f2f423c37c3e',
            suffix='_crypto',
            redo_crypto=False,
            do_crypto=True,
            replace=False,
            remove_ori=False,
            display_warning=True,
    ):
        '''
        使用方法：
        1、安装依赖 pip install pycrypto
        2、导入类 from openC import openC
        3、将文件里的 open 替换为 openC
        4、运行一次代码（openC 会自动生成加密后的文件)
        5、删掉未加密的原文件

        主要流程：
        1、如果file没有对应的加密文件：生成对应的加密文件
        2、如果file已有对应的加密文件：生成临时解密文件，读数据，删除临时解密文件

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
        self.file = file
        self.mode = mode
        self.buffering = buffering
        self.encoding = encoding
        self.errors = errors
        self.newline = newline
        self.closefd = closefd
        self.crypt_path = crypt_path
        self.decrypt_path = decrypt_path
        self.key = key
        self.suffix = suffix
        self.redo_crypto = redo_crypto
        self.do_crypto = do_crypto
        self.replace = replace
        self.remove_ori = remove_ori
        self.display_warning = display_warning
        self.file_handle = None
        self.need_clean = False
        self.init()
        self.open_file()

    def clean(func):
        def clean_func(self, *args, **args2):
            try:
                return func(self, *args, **args2)
            except Exception as err:
                if self.need_clean:
                    os.remove(self.file_tmp)
                raise err
        return clean_func

    @clean
    def init(self):
        # 冲突：如果replace=False则suffix==''和crypt_path==None不可以同时成立
        if not self.replace and (self.suffix == '' and self.crypt_path is None):
            raise Exception('If replace=False, suffix=='' and crypt_path==None cannot be established at the same time')
        # 警告：replace=True时suffix和crypt_path将无效
        if self.display_warning and self.replace and (self.suffix != '_crypto' or self.crypt_path):
            warnings.warn(
                'Suffix and crypt_path will be invalid when replace=True',
                SyntaxWarning
            )
        if self.replace:
            self.suffix = ''
            self.crypt_path = None
        # 警告：本方法只对读操作加密，写操作等同于open
        if self.display_warning and 'r' not in self.mode:
            warnings.warn(
                'This method only encrypts the read operation, '
                'and the write operation is equivalent to open',
                SyntaxWarning
            )

        # 确定路径
        file_path_ori, file_full_name = os.path.split(self.file)
        file_name, file_ext = os.path.splitext(file_full_name)
        file_path = file_path_ori
        if self.crypt_path:
            file_path = self.crypt_path
        self.file_crypto = os.path.join(file_path, file_name + self.suffix + file_ext)
        file_path = file_path_ori
        if self.decrypt_path:
            file_path = self.decrypt_path
        self.file_tmp = os.path.join(file_path, file_name + self.suffix + '_tmp' + file_ext)

        # 处理加密密钥
        if len(self.key) < 16:
            self.key += 'a' * (16 - len(self.key))
        elif len(self.key) > 16:
            self.key = self.key[:16]

    @clean
    def open_file(self):
        need_crypto = True
        # 无需加密
        if not self.do_crypto:
            need_crypto = False
        # 文件不存在
        if not os.path.isfile(self.file) and not os.path.isfile(self.file_crypto):
            need_crypto = False
        # 非读模式
        if 'r' not in self.mode:
            need_crypto = False

        if not need_crypto:
            self.file_handle = do_open(
                self.file,
                mode=self.mode,
                buffering=self.buffering,
                encoding=self.encoding,
                errors=self.errors,
                newline=self.newline,
                closefd=self.closefd,
            )
            return

        # 如果没有加密过或者redo_crypto=True会在crypt_path目录下生成一次加密文件
        if self.redo_crypto or not os.path.isfile(self.file_crypto):
            self.make_crypto()
        # 解密文件
        try:
            self.decrypt_data()
        except ValueError as err:
            if self.replace:
                self.make_crypto()
                self.decrypt_data()
            else:
                raise err
        self.need_clean = True
        # 读加密文件
        self.file_handle = do_open(
            self.file_tmp,
            mode=self.mode,
            buffering=self.buffering,
            encoding=self.encoding,
            errors=self.errors,
            newline=self.newline,
            closefd=self.closefd,
        )
        return

    @clean
    def __enter__(self):
        return self.file_handle

    @clean
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.need_clean:
            os.remove(self.file_tmp)

    @clean
    def __iter__(self):
        return self.file_handle.__iter__()

    @clean
    def __next__(self):
        return self.file_handle.__next__()

    @clean
    def read(self):
        return self.file_handle.read()

    @clean
    def readline(self):
        return self.file_handle.readline()

    @clean
    def readlines(self):
        return self.file_handle.readlines()

    @clean
    def write(self, *args, **args2):
        return self.file_handle.write(*args, **args2)

    @clean
    def tell(self):
        return self.file_handle.tell()

    @clean
    def seek(self, *args, **args2):
        return self.file_handle.seek(*args, **args2)

    @clean
    def close(self):
        self.file_handle.close()
        if self.need_clean:
            os.remove(self.file_tmp)
        return

    @clean
    def make_crypto(self):
        with open(self.file, 'rb') as f:
            data = f.read()
        mode = AES.MODE_ECB
        data = add_to_16(data)
        encryptor = AES.new(str.encode(self.key), mode)
        encrypted_data = encryptor.encrypt(data)
        with open(self.file_crypto, 'wb') as f:
            f.write(encrypted_data)
        if self.remove_ori and not self.replace:
            os.remove(self.file)

    @clean
    def decrypt_data(self):
        with open(self.file_crypto, 'rb') as f:
            data = f.read()
        mode = AES.MODE_ECB
        encryptor = AES.new(str.encode(self.key), mode)
        origin_data = encryptor.decrypt(data).rstrip(bchr(0x01))
        with open(self.file_tmp, 'wb') as f:
            f.write(origin_data)
