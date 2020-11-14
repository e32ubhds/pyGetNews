#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import pysnooper
# from fasttest import run_time

import base64  #加密解密需要

import os
import re  #黑白名单依赖

import arrow
from time import sleep

from threadingpp import MyThread
import threading

import requests

# from itertools import chain
from configEdit import configEdit as editini
from time import sleep

import pandas as pd  #格式化,csv依赖
import ujson as json
# import csv

import itertools

sem = threading.Semaphore(6)  # 限制线程的最大数量为

eini = editini('../../config.ini')
today_timestamp = arrow.get(
    arrow.now().date()).replace(tzinfo='local').shift(hours=-2).timestamp

code = {
    '央视新闻': '1240574601',
    '人民日报': '2392014380',
    '易即今日': '3287706685',
    '早晨简报': '3269744997',
    '阅读简报': '3594457542',
    '央微语简报': '3233112410',
    '每日微简报': '3570720091',
    '读报时间到了': '3523795590',
}




black_list = ['朋友圈']

white_list = [
    '早报', '分享图片', '简报', '新闻', '每天60秒'
    #'三分钟财经'
]

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

#服务器变量


def Cookie_jsontostr():
    with open(eini.get('path', 'cookie') + 'cookie.txt',
              'r',
              encoding='utf-8-sig') as f:
        str_cookie = f.read()
        f.close()
    mem_cookie = json.loads(str_cookie)
    result_cookie = ''
    for i in range(len(mem_cookie)):
        result_cookie += str(mem_cookie[i]['name']) + '=' + str(
            mem_cookie[i]['value']) + ';'
    return '\'' + result_cookie[:-1] + '\''


def open_token():
    with open(eini.get('path', 'cookie') + 'token.txt',
              'r',
              encoding='utf-8-sig') as f:
        token = f.read()
        f.close()
        return str(token)


token = open_token()
cookie = Cookie_jsontostr()

# 使用Cookie，跳过登陆操作
headers = {
    'cookie':
    cookie,
    'accept-encoding':
    'gzip, deflate, br',
    'accept-language':
    'zh,zh-CN;q=0.9',
    'user-agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'accept':
    '*/*',
    'referer':
    'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=0&token='
    + cookie + '&lang=zh_CN',
    'authority':
    'mp.weixin.qq.com',
    'x-requested-with':
    'XMLHttpRequest',
}


def encodeb64(code):
    code = code.encode()
    b64 = base64.b64encode(code)
    str_b64 = str(b64, encoding='utf-8')
    return str_b64


def search_ifs(white_list, search_str):
    for i in range(len(white_list)):
        if re.search(white_list[i], search_str) is not None:
            return True
    return False


def data(code):
    code = code.encode()
    b64 = base64.b64encode(code)
    str_b64 = str(b64, encoding='utf-8')
    return {
        "action": "list_ex",
        "begin": "0",
        "count": "5",
        "fakeid": str_b64,
        "type": "9",
        "query": "",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
    }


def data_count(code, count):
    code = code.encode()
    b64 = base64.b64encode(code)
    str_b64 = str(b64, encoding='utf-8')
    return {
        "action": "list_ex",
        "begin": str(count),
        "count": "5",
        "fakeid": str_b64,
        "type": "9",
        "query": "",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
    }


# @pysnooper.snoop()


# @run_time
def News_content(data):
    content_list = []
    sem.acquire()
    sleep(4)
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        if item["create_time"] >= today_timestamp:
            if search_ifs(white_list, item["title"]):
                if not search_ifs(black_list, item["title"]):
                    content_list.append('=HyperLink("%s","%s")' %
                                        (item["link"], item["title"]))
    sem.release()
    return content_list


# @run_time
def toCsv(f_path, name, content):
    #     content = list(chain.from_iterable(content))
    content = pd.DataFrame(columns=name, data=content)
    content.to_csv(f_path, mode='a', encoding='utf-8-sig')


def del_file(f_path):
    if os.path.exists(f_path):
        os.remove(f_path)


def muiltLine(value, count):
    sem = threading.Semaphore(5)  # 限制线程的最大数量为
    with sem:
        jl = jobLine(value, count)
        while jl:
            count += 5
            jf = jobFlow(value, count)
        else:
            news.extend(jf)


def jobFlow(key, count):
    names = locals()
    d = data_count(key, count)
    names[key] = MyThread(target=News_content, kwargs={'data': d})
    names[key].start()
    for key, value in code.items():
        names[value].join()
    return names[value].get_result()


def main():
    f_path = eini.get('path', 'news') + '简报.csv'
    name = ['HyperLink']
    names = locals()
    news = []
    #判断是否该删除文件
    del_file(f_path)
    for value in code.values():
        for i in range(0, 10, 5):
            d = data_count(value, i)
            names[value + str(i)] = MyThread(target=News_content,
                                             kwargs={'data': d})
            names[value + str(i)].start()

    for key, value in code.items():
        for i in range(0, 10, 5):
            names[value + str(i)].join()
            if names[value + str(i)].get_result():
                news.extend(names[value + str(i)].get_result())
                print('{0:<{1}}\t已收录'.format(key,
                                             25 - len(str(key).encode('GBK'))))
    toCsv(f_path, name, news)
    print("收录完毕")


if __name__ == '__main__':
    main()
