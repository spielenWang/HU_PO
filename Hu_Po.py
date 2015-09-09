#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import requests
import os
import re
from bs4 import BeautifulSoup
import logging

from multiprocessing import Pool
from pyh import *

__author__ = 'Yuan'



tmp_path = os.getcwd() + '\\tmp\\'

# tmp_path = '/volume1/web/book/hupo/'
folder = os.getcwd() + os.path.sep + os.path.splitext(os.path.basename(__file__))[0]
index_url = 'http://www.ranwen.org/files/article/1/1335/index.html'
mainUrl = 'http://www.ranwen.org/files/article/1/1335/'

html_style = '''
    html{ background:#eee; }
    body{ width:90%; max-width: 1448px; background:#fff; margin:3em auto 0; padding-top:2em; border:1px solid #ddd; border-width:0 1px;}
    #wrapper{ padding:1% 3%; position:relative;}
    }
'''

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    filename='myapp.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logging.getLogger("requests").setLevel(logging.WARNING)


def get_catalog(index_url):
    """


    """
    kapitel = {}  # 存储章节信息 ｛章节代号：[（章节名称），（章节URL]｝
    response = requests.get(index_url)
    soup = BeautifulSoup(response.content,"html.parser")
    # print(soup.decode('gbk').encode('utf-8'))
    links = soup.find_all('div', {"class": 'dccss'})
    k_num = 0
    for n in links:
        if k_num == len(links) - 1:
            pass
        else:
            k_num += 1
            k_title = n.get_text()
            k_url = re.findall('href="(.*?)">', str(n))
            kapitel[k_num] = [k_url, k_title]

    logging.info('%s' % ('new capital:' + k_title))
    return kapitel


def find_content(url, title):
    """
    获取每个章节的小说内容，每段为List中的一个元素 2015-07-19 19:28:04

    :param k_url: 输入每个章节的URL
    :return:
    k_content_list 章节内容，每段为List中的一个元素
    """

    logging.info('URL:%s' % (url))
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    content = soup.find_all(id='content')
    # title = soup.find_all('div', {"class": 'ctitle'})
    # title = title[0].get_text()
    logging.info(u'capital:{0:s} get'.format(title))
    text = content[0].get_text()
    k_content = text.encode('utf-8')
    k_content_list = str(k_content).split('    ')
    return k_content_list


def creat_html(kwargs):
    for n in kwargs:
        k_id = n

        path = tmp_path + str(k_id) + '.html'
        if os.path.isfile(path):
            # logging.warning('！！略过！！章节已存在：%s' % (k_id))
            pass
        else:
            if len(kwargs[n][0]) != 0:
                k_url = mainUrl + kwargs[n][0][0]
                k_title = kwargs[n][1]
                # HTML 构建
                page = PyH('%s_琥珀之剑' % (k_title.encode('utf-8')))
                page.addMeta_charset('utf-8')
                page.addMeta('viewport', 'width=device-width, minimal-ui')
                page.addCSS('typo.css')
                page.addStyle(html_style)
                text_div = page << div(id='wrapper', cl='typo typo-selection')
                text_div << h1('%s' % (k_title.encode('utf-8')))
                text_div << br()
                content = find_content(k_url,k_title)
                for n in content:
                    text_div << p('%s' % (n))
                # HTML构建结束
                list_div = page << div(id='wrapper', cl='typo typo-selection',
                                       style='text-align: center; vertical-align: middle;')
                if k_id == 1:
                    list_div << a('章节目录', href='book_list.html')
                    list_div << a('下一章', href='%s.html' % (k_id + 1))
                if k_id != 1:
                    list_div << a('上一章', href='%s.html' % (k_id - 1))
                    list_div << a('章节目录', href='book_list.html')
                    list_div << a('下一章', href='%s.html' % (k_id + 1))
                # if k_id == len(kwargs):
                # list_div << a('上一章', href='%s.html' % (k_id - 1))
                # list_div << a('章节目录', href='book_list.html')

                page.printOut(path)

            else:
                pass


def data(kwargs):  # 解决dict传入问题
    print(kwargs[1])


def run():
    pool = Pool(1)
    k = get_catalog(index_url)

    results = pool.map(creat_html(k))


def runTest():
    # k = find_content('http://www.ranwen.org/files/article/1/1335/14061167.html','test')
    print(folder)


if __name__ == "__main__":
    # runTest()
    # run()
    k = get_catalog(index_url)
    creat_html(k)


