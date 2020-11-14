#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests  #网络请求模块
import re  #正则表达式
# import time  #时间模块
import pangu
import arrow


week=['一','二','三','四','五','六','天']
def headersstr2headers(header_str):
    t = arrow.now()
    print('大家好，今天是公历 %d 月 %d 日，星期%s \r\n'% (t.month,t.day,week[t.weekday()]))
    for str_line in header_str.splitlines():
        if str_line != "":
            str_line = re.sub('\.$', '。', str_line)
            str_line = re.sub('。$', '', str_line)
            pangu_text = pangu.spacing_text(str_line)
            print(pangu_text + '\r\n')


header_str = """


社会文化版（3）



经济版（3-1）



政策版（2）


公司版（3）



人工智能专题（1）



太空商业专题（1）



国际版（2）




医疗卫生版（2-1）



科技版（N）



娱乐版（1）


名人版（1）


现象版（1）


辟谣专题（1）



"""
headersstr2headers(header_str)
