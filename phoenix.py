#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import lxml
import time
from pathlib import Path
import os

base_url = 'http://zt.ppmg.cn/textbook/'

base_path = '江苏凤凰传媒版/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}

def dd(param, breakdown = 1):
    print(param)
    if breakdown:
        exit()

def getCateList():
    print('开始获取分类列表...')
    response = requests.get(base_url, headers=headers)
    response.encoding= 'utf8'
    soup = BeautifulSoup(response.text, 'lxml')

    cate_list = []

    boxes = soup.find_all('div', class_='box')
    for box in boxes:
        cate_title = box.find('div', class_='small-head').text.replace(' ', '-').strip()

        temp = {}
        temp['cate_title'] = cate_title
        temp['book_list'] = []

        uls = box.find('div', class_='list-ul-small').find_all('ul')
        for ul in uls:
            lis = ul.find_all('li')
            for li in lis:
                t = {}
                t['href'] = li.find('a')['href']
                t['book_name'] = li.find('a').text.replace(' ', '-')
                (temp['book_list']).append(t)
        cate_list.append(temp)
    return cate_list


cate_list = getCateList()
print('开始下载...')
for cate in cate_list:
  # 创建分类目录
    Path(base_path + cate['cate_title']).mkdir(parents=True, exist_ok=True)
    print('\n')
    print('下载分类：%s...' % cate['cate_title'])
    print('\n')

    for book in cate['book_list']:
        url = base_url + book['href']
        bookname = book['book_name'] + '.pdf'

        full_file_path = base_path + cate['cate_title'] + '/' + bookname + '.pdf'
        # 文件已存在则跳出
        if os.path.isfile(full_file_path):
            print(full_file_path, ' 文件已存在')
            continue

        responsePDF = requests.get(url, headers=headers)
        with open(full_file_path,'wb') as f:
            for chunk in responsePDF.iter_content(128):
                f.write(chunk)
        f.close()
        print(bookname, '下载成功！')

   