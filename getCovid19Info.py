#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

from jmespath import search
import ujson as json

import time
import arrow

# import pysnooper
# from fasttest import run_time

url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner'
verify = '../cert/百度/baidu-com-chain.pem'
file_path = './covid19.txt'
headers = {
    'Host': 'voice.baidu.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':
    'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer':
    'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner',
    'Connection': 'keep-alive',
    'Cookie':
    '',  #请填入自己的Cookie
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}


def spiders(url, cert, header):
    r = requests.get(url, verify=cert, headers=header)
    time.sleep(3)
    demo = r.text
    soup = BeautifulSoup(demo, "lxml")
    txt = soup.find_all('script', {'id': 'captain-config'})[0].string
    return txt


def jsave(file_path, contents):
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        j = contents
        f.write(j)
        f.close()


def fileLoad(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        con = f.read()
        return con
        f.close()


def sti(string):
    i = int(string) / 10000
    r = round(i, 2)
    s = str(r)
    return s


def sav():
    contents = spiders(url, verify, headers)
    jsave(file_path, contents)


def load():
    t = arrow.now()
    a = fileLoad(file_path)
    j = json.loads(a)
    s = search('component', j)  #['page', 'component', 'bundle', 'version']

    # 关键信息段
    s = search('component[*].summaryDataOut',
               j)[0]  #['page', 'component', 'bundle', 'version']
    tt = search('component[0].mapLastUpdatedTime',
                j)  #['page', 'component', 'bundle', 'version']

    #时间字符串处理
    tt = arrow.get(tt, 'YYYY.MM.DD HH:mm', tzinfo='local')

    curConfirm = sti(s['curConfirm'])
    confirmedRelative = sti(s['confirmedRelative'])
    curedRelative = sti(s['curedRelative'])
    diedRelative = sti(s['diedRelative'])
    if tt.day == t.day and tt.month == t.month:
        print(
            '今天是%d月%02d日,现有确诊人数:%s万，昨日确诊病例人数:%s万，昨日治愈人数:%s万，昨日死亡人数:%s万，数据来源Baidu新冠专题'
            % (t.month, t.day, curConfirm, confirmedRelative, curedRelative,
               diedRelative))
    else:
        print('日期与今日不匹配，请检查数据源是否为最新，或本机时间是否与网络时间一致')


# @run_time
def main():
    sav()
    load()


if __name__ == '__main__':
    main()
