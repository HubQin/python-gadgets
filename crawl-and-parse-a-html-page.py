#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
crawl-and-parse-a-html-page.py
~~~~~~~~~~~~~~~~~
"""

import requests
from bs4 import BeautifulSoup, Comment
import os
import datetime
import time
import hashlib
import pymysql

def get_datetime():
    now_time = datetime.datetime.now()
    now_date = now_time.strftime('%Y%m%d')
    return now_time, now_date

def get_now_time_md5(now_time):
    return hashlib.md5(str(now_time).encode('utf-8')).hexdigest()

def save_image(url):
    response = get_response(url)
    image_content = response.content

    now_time,now_date = get_datetime()
    md5_str = get_now_time_md5(now_time)

    if not os.path.exists('images/' + now_date):
        os.makedirs('images/' + now_date)
    with open('images/' + now_date + '/' + md5_str + '.jpg','wb') as f:
        f.write(image_content)
        f.close()

    image_url_local = '/images/' + now_date + '/' + md5_str + '.jpg'
    return image_url_local

def get_response(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    }
    return requests.get(url, headers=headers)

def parse_one_item(url):
    response = get_response(url)
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html, 'lxml')
    detail = soup.find('div', class_='detail')

    # Header info
    head = detail.find('div', class_='head')
    title = head.find('h1').text

    # Content
    content = detail.find('div', class_='content')
    template_description = content.find('div', class_='template_description').text.strip()
    big_image = content.find('div', class_='big_image')
    big_image_url = big_image.find('a')['href']

    # save image and return a local url
    big_image_url_local = save_image(big_image_url)

    # feature info
    template_feature_soup = detail.find('div', class_='template_feature')
    template_feature = template_feature_soup.text.replace('\n', '').replace('\t', '').replace(' ', '')

    # price
    buttons_soup = content.find('div', class_='buttons')
    price = buttons_soup.find('span', class_='dlcount').find('strong', class_='orange').text

    # demo url
    demo_soup = content.find('div', id='source_box')
    demo_comment = demo_soup.find(string=lambda text:isinstance(text,Comment))
    demo_comment_soup = BeautifulSoup(demo_comment, 'lxml')
    demo_comment_soup.find('div', id='url_word').extract()
    demo_comment_soup.find('div', id='url_weixin').extract()
    demo_content = demo_comment_soup.find('div', class_='pop_content').text
    demo_content = os.linesep.join([s for s in demo_content.splitlines() if s])

    # except redundant content
    content.find('div',id='source_box').extract()
    content.find('div',id='download_box').extract()
    content.find('div',id='smileBoxOuter').extract()
    content.find('div',class_='detail_foot').extract()
    content.find('div',class_='buttons').extract()
    content.find('div',class_='template_description').extract()
    content.find('div',class_='big_image').extract()
    content.find('p',class_='short_tit').extract()
    template_feature_soup.extract()

    # other detail content
    other_descriptions = content.text.replace('程序员，你不是一个人；网站开发QQ群：698377651，在线充值，或联系QQ3401083589直接充值', '')
    # trim empty lines
    other_descriptions = os.linesep.join([s for s in other_descriptions.splitlines() if s])

    img_tags = content.find_all('img')

    for k,v in enumerate(img_tags):
        image_url_local = save_image(v['src'])
        other_descriptions = other_descriptions + '<br /><img src="' + image_url_local + '"/>'

    # evetually
    template_description = template_description + '<br /><img src="' + big_image_url_local + '"/>'
    template_description = template_description + '<br />' + other_descriptions
    return title, big_image_url_local, price, template_feature, template_description, demo_content

def get_lists(page):
    url_format = r'http://www.sucaihuo.com/source/0-0-0-0-0-{}'
    url = url_format.format(page)
    response = get_response(url)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    list_main_soup = soup.find('div', class_='list_main')
    lists_soup = list_main_soup.find_all('div', class_='per')
    for item in lists_soup:
        item_link = item.find('a')['href']
        yield item_link


def db_connect():
    return pymysql.connect("localhost", "root", "root", "your_database_name", use_unicode=True)

def insert_data(table_name, conn, **kw):
    sql = "INSERT INTO %s" % table_name
    sql += " ("
    tail_part = "VALUES ("
    value_list = []

    # Concat SQL string which format like:"INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    for key,value in kw.items():
        sql += "`" + key +"`,"
        tail_part += "%s,"
        value_list.append(value)

    sql = sql[:-1]
    sql += ") "

    tail_part = tail_part[:-1]
    tail_part += ")"

    value_tuple = tuple(value_list)
    sql = sql + tail_part

    conn.cursor().execute(sql,value_tuple)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    page = 1
    while True:
        print('Start to crawl page %s ...' % page)
        for url in get_lists(page):
            title, big_image_url_local, price, template_feature, template_description, demo_content = parse_one_item(url)
            
            kw = {}
            kw['name'] = title
            kw['cover'] = big_image_url_local
            kw['description'] = template_description
            kw['show_url'] = demo_content
            kw['stock'] = price
            kw['recipe_feature'] = template_feature
            kw['add_time'] = kw['update_time'] = time.time()

            conn = db_connect()
            insert_data('your_table_name', conn, **kw)
            print(title,'SUCCESS!')
            time.sleep(1)
        page = page + 1