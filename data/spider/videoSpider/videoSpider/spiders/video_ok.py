# -*- coding: utf-8 -*-
import scrapy
from videoSpider.items import VideospiderItem

class VideoSpider(scrapy.Spider):
    name = 'ok'
    allowed_domains = ['okzyw.com']

    def __init__(self, mainurl=None, num=1, page=2, *args, **kwargs):
        super(VideoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [mainurl]
        self.page = page
        self.num = int(num)

    def parse(self, response):
        urls = response.xpath("//span[@class='xing_vb4']/a/@href").getall()
        for href in urls:
            self.logger.info("爬取的url:"+href)
            yield response.follow(href, callback=self.parse_movie)

        self.num = self.num + 1
        next_page = response.xpath("//a[contains(./text(),'下一页')]/@href").get()
        if next_page is not None and self.num <= int(self.page):
            self.logger.info("爬取第"+str(self.num)+"页 url为"+next_page)
            yield response.follow(next_page, callback=self.parse)
        # pass

    def parse_movie(self, response):
        videospiderItem = VideospiderItem()

        #图片地址
        videospiderItem['image'] = response.xpath("//div[@class='vodImg']/img/@src").get()
        #名字 更新到第几集 评分
        videospiderItem['name'] = response.xpath("//div[@class='vodh']/h2/text()").get()
        videospiderItem['updateTo'] = response.xpath("//div[@class='vodh']/span/text()").get()
        videospiderItem['score'] = response.xpath("//div[@class='vodh']/label/text()").get()
        #别名 导演 主演 类型
        videospiderItem['alias'] = response.xpath("//div[@class='vodinfobox']/ul/li[1]/span/text()").get()
        videospiderItem['director'] = response.xpath("//div[@class='vodinfobox']/ul/li[2]/span/text()").get()
        videospiderItem['star'] = response.xpath("//div[@class='vodinfobox']/ul/li[3]/span/text()").get()
        videospiderItem['type'] = response.xpath("//div[@class='vodinfobox']/ul/li[4]/span/text()").get()
        #地区 语言 发行时间 时长 更新时间 总播放量 今日播放量 总评分数 评分次数
        videospiderItem['region'] = response.xpath("//li[@class='sm'][1]/span/text()").get()
        videospiderItem['language'] = response.xpath("//li[@class='sm'][2]/span/text()").get()
        videospiderItem['issueTime'] = response.xpath("//li[@class='sm'][3]/span/text()").get()
        videospiderItem['filmLength'] = response.xpath("//li[@class='sm'][4]/span/text()").get()
        videospiderItem['updateTime'] = response.xpath("//li[@class='sm'][5]/span/text()").get()
        videospiderItem['totalPlay'] = response.xpath("//li[@class='sm'][6]/span/text()").get()
        videospiderItem['todayPlay'] = response.xpath("//li[@class='sm'][7]/span/text()").get()
        videospiderItem['totalScore'] = response.xpath("//li[@class='sm'][8]/span/text()").get()
        videospiderItem['scoreTime'] = response.xpath("//li[@class='sm'][9]/span/text()").get()
        #描述
        videospiderItem["details"] = response.xpath("(//div[@class='vodplayinfo'])[2]/text()").get()
        #每集的url
        url = response.xpath("//div[@id='1']/ul/li/text()").get()
        i = 1
        if 'm3u8' not in url:
            for url in response.xpath("//div[@id='1']/ul/li/text()").getall():
                videospiderItem["episode"] = url.split("$")[0]
                videospiderItem["episodeUrl"] = url.split("$")[1]
                videospiderItem["source"] = "ok资源网"
                videospiderItem["episodeInt"] = i
                i = i + 1
                yield videospiderItem
        else:
            for url in response.xpath("//div[@id='2']/ul/li/text()").getall():
                videospiderItem["episode"] = url.split("$")[0]
                videospiderItem["episodeUrl"] = url.split("$")[1]
                videospiderItem["source"] = "ok资源网"
                videospiderItem["episodeInt"] = i
                i = i + 1
                yield videospiderItem
        # self.log("finish")
