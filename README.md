# python-gadgets

A collection of my python excise code or gadgets

## crawl-and-parse-a-html-page.py

实现的功能：逐页抓取列表页，获得每页所有单个商品的链接，然后抓取单个商品并使用beautifulsoup解析。html解析过程中，解决的问题有：段落文字空行的去除，html中注释块的提取，多余元素的排除；使用requests实现了网页和图片的抓取，图片的保存。