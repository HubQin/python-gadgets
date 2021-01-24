#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''公众号文章生成PDF'''

import pdfkit
import os
import pymongo
import datetime
import time
import sys

# 开始时间，如 19-05-20
START_DATE = '17-01-11'
# 结束时间，如 20-05-20
END_DATE = '22-01-12'
# 公众号BIZ
BIZ = 'MzU0MDE1OTUwNw=='
# PDF 保存目录
DST_ROOT = r'J:/python_work/PDF'

# PDF 页面设置
PDF_OPTIONS = {
    'dpi': 220,
    #'page-size': 'A4',
    'footer-center': '[page]',
    # 'margin-top': '0.5in',
    # 'margin-right': '0.5in',
    # 'margin-bottom': '0.5in',
    # 'margin-left': '0.5in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'minimum-font-size': 16,
}

if START_DATE == '' or END_DATE == '' or BIZ == '':
    print("必填项：开始时间、结束时间或公众号BIZ未填写")
    exit()

START_DICT = time.strptime(START_DATE, '%y-%m-%d')  # Start time
END_DICT = time.strptime(END_DATE, '%y-%m-%d')  # End time

# Mongo 数据库连接
try:
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect to datebase
    mongodb = mongoClient['wechat_spider']  # Select the database
    mongoPostsTable = mongodb['posts']  # Select Posts Collection
except:
    print("数据库连接错误")
    exit()


# parse wechat post content
def parseContent(title, author, pubName, publishAt, htmlContent, htmlString):
    htmlContent = htmlContent.replace('data-src=', 'src=')
    htmlString = htmlString.replace('__AUTHOR__', author)
    htmlString = htmlString.replace('__TITLE__', title)
    htmlString = htmlString.replace('__PUBLIC_NAME__', pubName)
    htmlString = htmlString.replace('__DATE__', publishAt)
    htmlString = htmlString.replace('__RICH_CONTENT__', htmlContent)
    return htmlString


def getAuthorInfo():
    authorCollection = mongodb['profiles']
    return authorCollection.find_one({"msgBiz": BIZ}, {"title": 1})


# generate PDf file
def writePDF(htmlS, title):
    title = title.replace(' ', '-')
    filename = title + '.pdf'
    dst = os.path.join(DST_ROOT, filename)

    print("开始生成PDF:", dst, ' ...')
    pdfkit.from_string(htmlS, dst, options=PDF_OPTIONS)
    print("成功生成PDF！")


def getData():
    query = {
        "publishAt": {
            "$gte": datetime.datetime(START_DICT.tm_year, START_DICT.tm_mon, START_DICT.tm_mday),
            "$lte": datetime.datetime(END_DICT.tm_year, END_DICT.tm_mon, END_DICT.tm_mday)
        },
        "msgBiz": BIZ
    }
    # Get the data we want
    data = mongoPostsTable.find(query, {"title": 1, "html": 1, "author": 1, "publishAt": 1})

    return data


if __name__ == '__main__':
    authorData = getAuthorInfo()

    # 读出模板文件内容
    f = open(r"J:/python_work/wx_pdf/tpl.html", "r", encoding='utf8')
    htmlString = f.read()
    f.close()

    articles = getData()
    for a in articles:
        # title, author, pubName, publishAt, htmlContent, htmlString
        html = parseContent(a['title'], a['author'], authorData['title'], str(a['publishAt']), a['html'], htmlString)
        writePDF(html, a['title'])
    print("已完成！")
