# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 00:25:50 2024

@author: DELL
"""

import pyecharts
import requests
import csv
import pandas
import jieba
import wordcloud

# 创建文件对象
f = open('data14.csv', mode = 'w', encoding = 'utf-8-sig', newline = '')
# 字典写入方法
csv_writer = csv.DictWriter(f, fieldnames = ['昵称', '地区', '性别', '评论'])
csv_writer.writeheader()

def GetContent(MaxId):
    """发送请求"""
    # 模拟浏览器
    headers = {
        'cookie': 'SINAGLOBAL=9079069003214.062.1714385816745; UOR=,,finance.sina.com.cn; SCF=Ao1viCPJYEZmZaqBtFLIiFjBL1AWFlLlJ3IwOhDwwmkBDYACrG6HTVbGTU379shEH8WIA4RpwOQQ0ZKn08aScCE.; ALF=1738047513; SUB=_2A25KdINJDeRhGeFK7FoX9SbOwj2IHXVpC5qBrDV8PUJbkNANLVXhkW1NQu7Hc1mh4mIqaec61ZS0BQRazJjj8ZBn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWCXrfKb7UqqU2Z4DKzQEGC5JpX5KMhUgL.FoMXS0ncSKnE1K22dJLoIp4IMNzLxKnLBo-LBo-LxK-L1KqL1hBLxKML1-BLB.qt; XSRF-TOKEN=8RGRANZ7a8AdUNV5__3TFn1f; _s_tentry=weibo.com; Apache=5481234675860.071.1735455520119; ULV=1735455520155:10:8:4:5481234675860.071.1735455520119:1734879253085; WBPSESS=N0o07z925RNG4dSBXH43bQ8Zzy6YhmoEG1EitzW-GWbEYZyW4oYi-VEn6VtaOXMfzAqhIuf7D_A0CW5PxX6NfxbQhGWmKL40tcNsI9EJuDuVmRjrUjqlQ4XW_aIAG7b53Lx9qCaGZ0BVULebwvyouA==; wb_view_log_7478658291=1536*8641.25; webim_unReadCount=%7B%22time%22%3A1735464055543%2C%22dm_pub_total%22%3A13%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A15%2C%22msgbox%22%3A0%7D',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }

    # 请求网址
    url = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=5093097113649843&is_show_bulletin=2&is_mix=0&count=10&uid=1649173367&fetch_level=0&locale=zh-CN'

    # 查询参数
    data = {
            'is_reload': '1',
            'id': '5093097113649843',
            'is_show_bulletin': '2',
            'is_mix': '0',
            'max_id': MaxId,
            'count': '20',
            'uid': '1649173367',
            'fetch_level': '0',
            'locale': 'zh-CN',
        }

    # 发送请求
    response = requests.get(url = url ,params = data ,headers = headers)

    """获取数据"""
    # 获取json数据
    json_data = response.json()

    """解析数据"""
    # 字典取值，提取评论信息所在的列表
    data_list = json_data['data']
    # for循环提取列表中的元素
    for index in data_list:
        #提取性别信息
        sex = index['user']['gender']
        if sex == 'f':
            gender = '女'
        elif sex == 'm':
            gender = '男'
        else:
            gender = '保密'
        #提取具体数据内容保存到字典中
        dit = {
            '昵称': index['user']['screen_name'],
            '地区': index['source'].replace('来自', ''),
            '性别': gender,
            '评论': index['text_raw'],
        }
        print(dit)
        """保存数据"""
        csv_writer.writerow(dit)
    # 获取下一页的max_id
    max_id = json_data['max_id']
    # 返回
    return max_id

#翻页采集数据
max_id = ''
for page in range(1, 100):
    print(f'正在采集第{page}页的数据内容')
    max_id = GetContent(MaxId = max_id)