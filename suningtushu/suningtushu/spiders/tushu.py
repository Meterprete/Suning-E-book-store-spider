# -*- coding: utf-8 -*-
import scrapy
import time
import re
from suningtushu.items import SuningtushuItem

count = 0


class TushuSpider(scrapy.Spider):
    name = 'tushu'
    allowed_domains = ['suning.com']
    start_urls = ['http://book.suning.com']

    def parse(self, response):
        list = response.xpath("//div[@class='menu-list']")
        div_list = list.xpath("./div[@class='menu-item']")

        '''把大分类放到列表中'''
        liname_list = []
        for div in div_list:
            liname_list.append(div.xpath("./dl/dt/h3/a/text()").extract_first())

        '''打印对应的分类目录'''
        print("\n一级分类：", end="    ")
        for index in range(len(liname_list)):
            print("【{}】{}".format(index, liname_list[index]), end="  ")

        '''获取待爬取的目录的索引值【需要判断是否为数字】'''
        li_index = int(input("\n\n请输入待抓取的图书前面'【】'中对应的序号：\n"))
        div00 = list.xpath("./div[@class='menu-sub']")[li_index]
        p_list = div00.xpath("./div[1]/p")
        if p_list != []:
            '''把待爬取的p标签对应的里面的文本放到 p_data_list 中'''
            p_data_list = []
            for p in p_list:
                p_data_list.append(p.xpath("./a/text()").extract_first())
            '''列出待爬取的p标签的小题目'''
            print("\n二级分类({})：".format(liname_list[li_index]), end="    ")
            for p_index in range(len(p_data_list)):
                print("【{}】{}".format(p_index, p_data_list[p_index]), end="  ")
            '''输入待爬取的二级目录索引值【需要验证是否输入数字】'''
            print("\n\n请输入待抓取的二级目录 {}种类 的图书前面'【】'中对应的序号：\r".format(liname_list[li_index]))
            pi_index = int(input())
            '''获取备爬取的二级目录对应索引的图书'''
            ul_list = div00.xpath("./div[1]/ul")
            ul_li_list = ul_list[pi_index].xpath("./li")
            '''遍历li，取出对应的链接以及名字，存到字典里'''
            ul_li_dict_list = []
            for li in ul_li_list:
                li_dict = {}
                li_dict['name'] = li.xpath("./a/text()").extract_first()
                li_dict['href'] = li.xpath("./a/@href").extract_first()
                ul_li_dict_list.append(li_dict)
            '''取得列表中的字典，输出三级目录'''
            print("\n三级分类({})：".format(p_data_list[pi_index]), end="    ")
            for ul_li_dict_index in range(len(ul_li_dict_list)):
                print("【{}】{}".format(ul_li_dict_index, ul_li_dict_list[ul_li_dict_index]['name']), end="  ")
            '''输入三级目录待抓取的图书的分类的索引【需要验证是否输入数字】'''
            print("\n\n请输入待抓取的三级目录 {}种类 的图书前面'【】'中对应的序号:\r".format(p_data_list[pi_index]))
            ul_index = int(input())

            '''Xpath效率来说比不上正则，但是稳定，所以这个事吧，我一部分用的正则，一部分用的xpath'''
            '''输入完以后，需要取出对应的字典中的href，进行初始页面的请求'''
            data_href = ul_li_dict_list[ul_index]['href']
            # https://list.suning.com/1-502314-0.html
            '''下一页根据'''
            data = re.findall(r"https://list.suning.com/1-(.*)-0.html", data_href)[0]

            '''请求一级图书页面'''
            yield scrapy.Request(
                data_href,
                callback=self.seconed_html_request,
                meta={"data": data}
            )
        else:
            '''获取备爬取的二级目录对应索引的图书'''
            ul_list = div00.xpath("./div[1]/ul")
            ul_li_list = ul_list.xpath("./li")
            # print(ul_li_list)
            '''遍历li，取出对应的链接以及名字，存到字典里'''
            ul_li_dict_list = []
            for li in ul_li_list:
                li_dict = {}
                li_dict['name'] = li.xpath("./a/text()").extract_first()
                li_dict['href'] = li.xpath("./a/@href").extract_first()
                ul_li_dict_list.append(li_dict)
            # print(ul_li_dict_list)
            '''取得列表中的字典，输出图书种类目录'''
            for ul_li_dict_index in range(len(ul_li_dict_list)):
                print("【{}】{}".format(ul_li_dict_index, ul_li_dict_list[ul_li_dict_index]['name']), end="  ")
            '''输入三级目录待抓取的图书的分类的索引【需要验证是否输入数字】'''
            print("\n\n请输入待抓取的图书种类前面'【】'中对应的序号:\r")
            ul_index = int(input())

            '''Xpath效率来说比不上正则，但是稳定，所以这个事吧，我一部分用的正则，一部分用的xpath'''
            '''输入完以后，需要取出对应的字典中的href，进行初始页面的请求'''
            data_href = ul_li_dict_list[ul_index]['href']
            # https://list.suning.com/1-502314-0.html
            '''下一页根据'''
            data = re.findall(r"https://list.suning.com/1-(.*)-0.html", data_href)[0]

            '''请求一级图书页面'''
            yield scrapy.Request(
                data_href,
                callback=self.seconed_html_request,
                meta={"data": data}
            )

    def seconed_html_request(self, response):
        li_list = response.xpath("//ul[@class='clearfix']/li")
        '''list_al内部存放的有 每个图书的 'prdid','shopid' 以及图书不完整的url地址'''
        list_all = []
        for li in li_list:
            '''匹配图书的url以及图书价格url的重要参数'''
            li_list = li.xpath(".//*").re(
                '''sa-data="{'eletp':'prd','prdid':'(.*?)','shopid':'(.*?)'.*?href="(.*?)" name''')[
                      0:3]
            '''提取的过程中，拿着 'prdid','shopid' 以及图书不完整的url地址去请求第三个页面，取得所有数据'''
            url = "https:" + li_list[-1]
            yield scrapy.Request(
                url,
                callback=self.third_html_request,
                meta={"data": li_list}
            )
            list_all.append(li_list)
        # print(len(list_all))
        '''下一页请求'''
        res = re.findall('''title="(下一页)"''', response.text)[0]
        if res == '下一页':
            global count
            count = count + 1
            nex_url = "https://list.suning.com/1-" + response.meta['data'] + "-{}".format(
                count) + "-0-0-0-0-14-0-4.html"
            print(nex_url)
            yield scrapy.Request(
                nex_url,
                callback=self.seconed_html_request,
                meta={"data": response.meta['data']}
            )

    def third_html_request(self, response):
        '''第三页进行数据的提取以及存放'''
        li_list = response.meta["data"]
        item = SuningtushuItem()
        '''Book_Src提取'''
        item['Book_Src'] = response.url
        item['Title'] = response.xpath("//h1/text()").extract()[1]
        rbq_list = response.xpath("//ul[@class='bk-publish clearfix']/li")

        '''修补的bug'''
        count = len(rbq_list)
        try:
            if count > 0:
                '''作者'''
                item['Author'] = rbq_list[0].xpath('./text()').extract_first()
            if count > 1:
                '''出版社'''
                item['Press'] = rbq_list[1].xpath('./text()').extract_first()
            if count > 2:
                '''出版日期'''
                item['Publish_Time'] = rbq_list[2].xpath('./span[2]/text()').extract_first()
        except:
            item['Author'] = " "
            item['Press'] = " "
            item['Publish_Time'] = " "
            print("异常图书。。。。。。。")
        # print(item)
        '''构造价格请求的url'''
        url = "https://pas.suning.com/nspcsale_0_0000000" + li_list[0] + "_0000000" + li_list[0] + "_" + li_list[
            1] + "_120_534.html?"
        # print(url)
        yield scrapy.Request(
            url,
            callback=self.Fourth_html_request,
            meta={"item": item}
        )

    def Fourth_html_request(self, response):
        item = response.meta['item']
        '''进行图书价格的提取'''
        text = response.text
        '''原谅我，对速度无能为力了，本来价格这个获取的时候解析主机就很慢的'''
        item['Price'] = re.findall('''"netPrice":"(.*?)"''', text)[0]
        yield item
