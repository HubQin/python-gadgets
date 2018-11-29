#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
from PIL import Image
import pytesseract
from io import BytesIO
import os

class BookCrawler(object):

    def __init__(self, session):
        self.session = session
        self.ip_list = []
        self.index = 0
        self.proxies = {}
        self.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    }

    def save_file(self, url, filename):
        # check if file exist in folder
        file_path = 'download/' + filename
        if os.path.isfile(file_path):
            print(file_path + ' 文件已经下载！')
            return

        response = self.get_response(url)
        text = response.text

        if '今天下载次数过多' in text or '下载文件数限制' in text:
            print(filename,'FAIL!!!', BeautifulSoup(text, 'lxml').text)
            exit()

        soup = BeautifulSoup(text, 'lxml')
        a = soup.find('a', class_='madIdea')
        response_a = self.get_response(a['href'])

        with open(file_path,'wb') as f:
            for chunk in response_a.iter_content(128):
                f.write(chunk)
            f.close()
            print(filename, 'SUCCESS！')

    def get_response(self, url):
        response = self.session.get(url, headers = self.headers, proxies = self.proxies)
        if response:
            return response
        else:
            print("No response retuen!")
            exit()
            

    def get_lists(self, page):
        # General URL
        # url_format = r'http://icaredbd.com:6868/src/ebooks.php?&page_no={}'
        # URL with keywords
        url_format = r'http://icaredbd.com:6868/src/search.php?queryinfo=%E6%9C%A8%E5%BF%83&type=ebook&page_no={}'
        url = url_format.format(page)
        response = self.get_response(url)
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', class_='table')
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        
        for tr in trs:
            td = tr.find('td')
            a = td.find('a')
            filename = a.text.replace('\t', '').replace('\n', '').replace(' ', '')
            down_url = a['href']
            yield filename, down_url

    def log(self, page):
        with open('log.txt', 'a') as f:
            f.write('page:' + str(page) + ' ')
            f.close()

    def login(self):
        url = r'http://icaredbd.com:6868/src/login.php'
        captcha_code = self.get_captcha()
        data = {}
        data['my_user_name'] = 'TINA EMARD' # change to your user name
        data['my_password'] = '147258' # change to your password
        data['verify_code'] = captcha_code

        try:
            response = self.session.post(url, headers = self.headers, data = data, proxies = self.proxies)
            if '验证码错误' in response.text:
                print('验证码错误!重新尝试登录！')
                self.login()
        except:
            print('Fail to login!')
            exit()

    def get_captcha(self):
        url = r'http://icaredbd.com:6868/src/verify_code_cn.php'
        response = self.get_response(url)
        content = response.content

        im = Image.open(BytesIO(content))
        captcha_code = pytesseract.image_to_string(im, lang='eng')
        if captcha_code:
            return captcha_code
        else:
            print("验证码识别失败！重新识别！")
            self.get_captcha()

    def get_ip_list(self):
        with open('ip_list.txt', 'r') as f:
            content = f.read()
            f.close()
            self.ip_list = content.splitlines()

if __name__ == '__main__':
    session = requests.Session()
    book = BookCrawler(session)
    book.index = -1
    if book.index >=0:
        book.get_ip_list()
        book.proxies['http'] = 'http://' + book.ip_list[book.index]
    book.login()

    for page in range(1,13):
        print("Start page %s ..." % page)
        book.log(page)
        for data in book.get_lists(page):
            book.save_file(data[1], data[0])
        page = page + 1
        time.sleep(1)