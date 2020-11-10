# -*- coding: utf-8 -*-
import scrapy
from videoSpider.items import VideospiderItem

class VideoSpider(scrapy.Spider):
    name = 'ixxy'
    allowed_domains = ['iixxzyapi.com']

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
        next_page = "http://api.iixxzyapi.com/?m=vod-index-pg-" + str(self.num) + ".html"
        if next_page is not None and self.num <= int(self.page):
            self.logger.info("爬取第"+str(self.num)+"页 url为"+next_page)
            yield response.follow(next_page, callback=self.parse)
        pass

    def parse_movie(self, response):
        videospiderItem = VideospiderItem()

        #图片地址
        videospiderItem['image'] = response.xpath("//div[@class='vodImg']/img/@src").get()
        #名字
        videospiderItem['name'] = response.xpath("//h2/text()").get()
        #类型
        videospiderItem['type'] = response.xpath("//div[@class='vodinfobox']/ul/li[4]/span/text()").get()
        videospiderItem['updateTime'] = response.xpath("//li[@class='sm'][5]/span/text()").get()

        for url in response.xpath("//input[@name='copy_sel']/@value").getall():
            if 'm3u8' in url:
                videospiderItem["episodeUrl"] = url

        videospiderItem["source"] = 'ixxy'

        yield videospiderItem
        # print(videospiderItem)
