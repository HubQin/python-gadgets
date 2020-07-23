#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import lxml
import time
from pathlib import Path
import os

base_url = 'https://bp.pep.com.cn/jc'

base_path = '人教版春季2/'

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

    list_divs = soup.find_all('div', class_='list_sjzl_jcdzs2020')

    for list_div in list_divs:
        cate_title = list_div.find('h5').text.replace(' ', '-')
        temp = {}
        temp['cate_title'] = cate_title
        temp['sub_list'] = []

        uls = list_div.find_all('ul')
        for ul in uls:
            lis = ul.find_all('li')
            for li in lis:
                child = {}
                child['link'] = (li.find('a')['href']).lstrip('.')
                child['link_title'] = li.find('a').text.replace(' ', '-')
                (temp['sub_list']).append(child)
        cate_list.append(temp)
    print('分类列表获取完毕，共%s分类' % len(cate_list))
    return cate_list


cate_list = getCateList()
print('开始下载...')
for cate in cate_list:
    print('\n')
    print('下载分类：%s...' % cate['cate_title'])
    print('\n')
    for child in cate['sub_list']:
        print('--下载子分类：%s...' % child['link_title'])
        # 创建分类目录
        Path(base_path + cate['cate_title'] + '/' + child['link_title']).mkdir(parents=True, exist_ok=True)

        url = base_url + child['link']
        response = requests.get(url, headers=headers)
        response.encoding= 'utf8'
        soup = BeautifulSoup(response.text, 'lxml')

        divs = soup.find_all('div', class_='con_list_jcdzs2020')
        for div in divs:
            uls = div.find_all('ul')
            for ul in uls:
                lis = ul.find_all('li')
                for li in lis:
                    all_a = li.find_all('a')
                    title = (all_a[1]['title']).replace(' ', '-') + '.pdf'
                    pdf = (all_a[3]['href']).lstrip('.').lstrip('/')

                    full_file_path = base_path + cate['cate_title'] + '/' + child['link_title'] + '/' + title
                    # 文件已存在则跳出
                    if os.path.isfile(full_file_path):
                        print(full_file_path, ' 文件已存在')
                        continue

                    responsePDF = requests.get(url+pdf, headers=headers)
                    with open(full_file_path,'wb') as f:
                        for chunk in responsePDF.iter_content(128):
                            f.write(chunk)
                    f.close()
                    print(title, '下载成功！')
