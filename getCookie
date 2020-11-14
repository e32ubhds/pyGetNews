#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from lxml.html import etree

from time import sleep
import ujson as json
import re
from pathlib2 import Path

from configEdit import configEdit as editini

# import pysnooper


# @pysnooper.snoop()
# 获取cookies和token
class CookieClass(object):
    # 初始化
    def __init__(self):
        self.url = 'https://mp.weixin.qq.com'
        self.html = None
        self.editini = editini('../../config.ini')

    def getpath(self):
        print(self.editini.get('path', 'chromedriver'))

    # 获取cookie
    def getCookie(self):
        Browner = webdriver.Chrome(
            self.editini.get('path', 'chromedriver') + 'chromedriver.exe')
        Browner.get(self.url)
        Browner.implicitly_wait(20)
        accountInput = Browner.find_element_by_xpath(
            '//*/a[@class="login__type__container__select-type"]')
        accountInput.click()
        # 获取账号输入框
        input_ID = Browner.find_element_by_name('account')
        # 获取密码输入框
        input_PW = Browner.find_element_by_name('password')
        id = ''  # 输入账号
        pw = ''  # 输入密码
        # id = input('请输入账号:')
        # pw = input('请输入密码:')
        input_ID.send_keys(id)
        input_PW.send_keys(pw)
        # 获取登录button，点击登录
        Browner.find_element_by_class_name('btn_login').click()
        # 等待扫二维码
        sleep(10)
        self.html = Browner.page_source

        # 等待扫二维码
        sleep(10)
        ck = Browner.get_cookies()
        #         print(ck)
        ck1 = json.dumps(ck)
        with open(self.editini.get('path', 'cookie') + 'cookie.txt',
                  'w',
                  encoding='utf-8-sig') as f:
            f.write(ck1)
            f.close()
        Browner.quit()
        # 获取token，在页面中提取

    def getToken(self):
        html = etree.HTML(self.html)
        url = html.xpath('//a[@title="首页"]/@href')[0]
        # print(url)
        token = re.findall('\d+', url)[0]
        # print(token)
        with open(self.editini.get('path', 'cookie') + 'token.txt',
                  'w',
                  encoding='utf-8-sig') as f:
            f.write(token)
            f.close()


def main():
    C = CookieClass()
    C.getCookie()
    C.getToken()
    print("已获取token")


if __name__ == '__main__':
    main()
