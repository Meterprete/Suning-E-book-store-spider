# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re


class SuningtushuPipeline(object):
    def open_spider(self, spider):
        print("Mongodb is establishing a connection....................")
        client = MongoClient()
        self.connect = client['suning']['data']
        print("===================================================================================")
        print("\n---------Name of the project: 苏宁易购图书爬虫---------------------              ||\n")
        print("---------author: Caiden_Micheal                                                  ||")
        print("---------GitHub address: https://github.com/Meterprete?tab=repositories          ||")
        print("---------Personal mailbox: wangxinqhou@foxmail.com                               ||")
        print("---------time: 2020.2.7                                                          ||\n")
        print("===================================================================================")

    def process_item(self, item, spider):
        self.data_clear(item)
        m = self.connect.insert(dict(item))
        print(m)
        return item

    def data_clear(self, contant):
        '''简单的数据清晰'''
        re_compile = re.compile("\s|\r|\n|\t")
        try:
            contant['Author'] = re_compile.sub("", contant['Author'])
            contant['Press'] = re_compile.sub("", contant['Press'])
        except Exception as e:
            print(e)
        contant['Title'] = re_compile.sub("", contant['Title'])
        return contant
