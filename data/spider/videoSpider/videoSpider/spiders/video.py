# -*- coding: utf-8 -*-
import scrapy
from videoSpider.items import VideospiderItem

class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['wolongzy.net']

    def __init__(self, mainurl=None, num=1, page=2, *args, **kwargs):
        super(VideoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [mainurl]
        self.page = page
        self.num = int(num)

    def parse(self, response):
        urls = response.xpath("//a[@class='videoName']/@href").getall()
        for href in urls:
            self.logger.info("爬取的url:"+href)
            yield response.follow(href, callback=self.parse_movie)

        self.num = self.num + 1
        next_page = "http://wolongzy.net/?page=" + str(self.num)
        if next_page is not None and self.num <= int(self.page):
            self.logger.info("爬取第"+str(self.num)+"页 url为"+next_page)
            yield response.follow(next_page, callback=self.parse)
        # pass

    def parse_movie(self, response):
        videospiderItem = VideospiderItem()

        #图片地址
        videospiderItem['image'] = response.xpath("//div[@class='left']/img/@src").get()
        #名字 更新到第几集 评分
        mingCheng = response.xpath("//p[@class='whitetitle']/text()").get().strip().split("：")[1]
        if "[" in mingCheng:
            videospiderItem['name'] = mingCheng.split("[")[0]
            videospiderItem['updateTo'] = mingCheng.split("[")[1].split("]")[0]
        else:
            videospiderItem['name'] = mingCheng
            videospiderItem['updateTo'] = ""
        videospiderItem['score'] = "9.0"
        #别名 导演 主演 类型
        videospiderItem['type'] = response.xpath("//div[@class='right']/p[1]/a/text()").get()
        item = {}
        for p in response.xpath("//div[@class='right']/p/text()").getall():
            item[p.split("：")[0]] = p.split("：")[1]
        videospiderItem['director'] = item["导演"] if item.get("导演") else ""
        videospiderItem['star'] = item["演员"] if item.get("演员") else ""
        videospiderItem['alias'] = item["别名"] if item.get("别名") else ""
        videospiderItem['region'] = item["地区"] if item.get("地区") else ""
        videospiderItem['language'] = item["语言"] if item.get("语言") else ""
        videospiderItem['issueTime'] = item["上映"] if item.get("上映") else ""
        videospiderItem['filmLength'] = item["片长"] if item.get("片长") else ""
        videospiderItem['updateTime'] = item["更新时间"] if item.get("更新时间") else ""
        videospiderItem['totalPlay'] = "0"
        videospiderItem['todayPlay'] = "0"
        videospiderItem['totalScore'] = "0"
        videospiderItem['scoreTime'] = "0"
        #描述
        videospiderItem["details"] = response.xpath("//h4[1]/../text()").get().strip().replace("\r\n","")
        #每集的url
        i = 1
        for url in response.xpath("//input[@name='kuyun[]']/@value").getall():
            videospiderItem["episode"] = url.split("$")[0]
            videospiderItem["episodeUrl"] = url.split("$")[1]
            videospiderItem["source"] = "卧龙资源"
            videospiderItem["episodeInt"] = i
            i = i + 1
            yield videospiderItem
            # print(videospiderItem)
