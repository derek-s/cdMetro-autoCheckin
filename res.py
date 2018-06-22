#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 15:54
# @Author  : Derek.S
# @Site    : 
# @File    : getSign.py

import hashlib
import random
import string
import time


localtime = lambda: str(int(round(time.time() * 1000)))


def getSign(**kwargs):

    d = {
        "Accept-APIVersion": "1.0",
        "appVersionNo": "73",
        "mobileBrand": "Honor",
        "mobileStandard": "WIFI",
        "platformType": "android",
        "platformVersion": "6.0",
        "sign": "p@ssw0rd"
    }

    for kw_key in kwargs:
        d[kw_key] = kwargs[kw_key]

    data = ""
    for key in sorted(d.keys()):
        data += "&" + key + "=" + d[key]

    sign_raw = data[1:]
    h = hashlib.md5()
    h.update(str(sign_raw).encode("utf-8"))
    sign_md5 = h.hexdigest()
    return sign_md5


def generate_randmon_str(strlength):
    str_list = [random.choice(string.digits + string.ascii_lowercase) for i in range(strlength)]
    random_str = ''.join(str_list)
    return random_str


def generate_random_int(strlength):
    str_list = [random.choice(string.digits) for i in range(strlength)]
    random_str = ''.join(str_list)
    return random_str


def randompnId():
    pnId_str = "{s1}" + "-" + "{s2}" + "-" + "{s3}" + "-" + "{s4}" + "-" + "{s5}"
    pnId = pnId_str.format(
        s1=generate_random_int(8),
        s2=generate_randmon_str(4),
        s3=generate_randmon_str(4),
        s4=generate_randmon_str(4),
        s5=generate_randmon_str(12)
    )
    return(pnId)


def pwdMD5(strPwd):
    h = hashlib.md5()
    h.update(str(strPwd).encode("utf-8"))
    pwd_md5 = h.hexdigest()
    return pwd_md5