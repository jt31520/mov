# -*- coding: utf-8 -*-
import scrapy
from videoSpider.items import VideospiderItem

class VideoSpider(scrapy.Spider):
    name = 'xvideo'
    allowed_domains = ['apilj.com']

    def __init__(self, mainurl=None, num=1, page=2, *args, **kwargs):
        super(VideoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [mainurl]
        self.page = page
        self.num = int(num)

    def parse(self, response):
        urls = response.xpath("//a[@class='address']/@href").getall()
        for href in urls:
            self.logger.info("爬取的url:"+href)
            yield response.follow(href, callback=self.parse_movie)

        self.num = self.num + 1
        next_page = "http://apilj.com/?page=" + str(self.num)
        if next_page is not None and self.num <= int(self.page):
            self.logger.info("爬取第"+str(self.num)+"页 url为"+next_page)
            yield response.follow(next_page, callback=self.parse)
        pass

    def parse_movie(self, response):
        videospiderItem = VideospiderItem()

        #图片地址
        videospiderItem['image'] = response.xpath("//div[@class='left']/img/@src").get()
        #名字
        videospiderItem['name'] = response.xpath("//h4[@class='list-title']/text()").get().strip().split("：")[1]
        #类型
        videospiderItem['type'] = response.xpath("//div[@class='new_right']/p[1]/a/text()").get()
        videospiderItem['updateTime'] = response.xpath("//div[@class='new_right']/p[2]/text()").get().split("：")[1]

        videospiderItem["episodeUrl"] = response.xpath("//div[@class='yyxf']/p/a/text()").get()

        videospiderItem["source"] = 'lajiao'

        yield videospiderItem
        # print(videospiderItem)
