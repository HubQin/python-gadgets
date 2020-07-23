# python-gadgets

A collection of my python excise code or gadgets

## crawl-and-parse-a-html-page.py

实现的功能：逐页抓取列表页，获得每页所有单个商品的链接，然后抓取单个商品并使用beautifulsoup解析。html解析过程中，解决的问题有：段落文字空行的去除，html中注释块的提取，多余元素的排除；使用requests实现了网页和图片的抓取，图片的保存；使用pymysql实现数据库连接并将提取的数据存入数据表。

## ebook-downloader
包含文件main.py(主文件，用于下载电子书), get_ip.py（用于获取代理IP）
* 实现电子书按指定页数范围下载或指定关键词下载
* 实现自动登录和验证码自动识别

## words-count-with-lemmatized
使用分词表进行分词还原后统计词频，同时去除常见高频单词。

## phoenix.py
凤凰版春季中小学教材下载

## pep_book.py
人教版春季中小学教材下载

## word_count.py
基于nltk的词频统计
