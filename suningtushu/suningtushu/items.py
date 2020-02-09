# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningtushuItem(scrapy.Item):
    # define the fields for your item here like:
    '''图书链接，从一级页面提取'''
    Book_Src = scrapy.Field()
    '''作者'''
    Author = scrapy.Field()
    '''图书标题，从二级页面提取'''
    Title = scrapy.Field()
    '''出版日期，二级页面直接提取'''
    Publish_Time = scrapy.Field()
    '''出版社，二级页面直接提取'''
    Press = scrapy.Field()
    '''图书价格，三级页面构造提取'''
    Price = scrapy.Field()
