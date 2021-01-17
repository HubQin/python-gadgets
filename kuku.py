#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import lxml

baseUrl = 'https://pan.kuku.me/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}

f = open('kuku_url.txt', 'a', encoding='utf8')

# 递归
def walk(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf8'
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find(id="list-table")
    trs = table.find_all('tr')
    # 去除第一个
    trs = trs[1:]
    for tr in trs:
        a = tr.find('a')
        if hasattr(a, 'name') and a['name'] == 'folderlist':
            print("walk:"+baseUrl + a['href'])
            walk(baseUrl + a['href'])
        elif hasattr(a, 'name') and a['name'] == 'filelist':
            print(baseUrl + a.findNext()['href'])
            f.write(baseUrl + a.findNext()['href'] + '\n')



if __name__ == '__main__':
    walk(r"https://pan.kuku.me/kuku/%E4%BA%B2%E5%AD%90%E7%B1%BB%E5%90%88%E9%9B%864T/03%20%E3%80%90%E5%AD%99%E8%B7%AF%E5%BC%98%E3%80%91%2024G/")
    f.close()
