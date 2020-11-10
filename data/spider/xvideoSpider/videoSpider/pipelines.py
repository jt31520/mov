# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import hashlib
from videoSpider import settings

class VideospiderPipeline(object):
    def __init__(self):
        self.host=settings.MYSQL_HOST
        self.db=settings.MYSQL_DBNAME
        self.user=settings.MYSQL_USER
        self.passwd=settings.MYSQL_PASSWD

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host=self.host,
            db=self.db,
            user=self.user,
            passwd=self.passwd,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        # 判断episodeUrl
        sqlEpisodeExist = 'select episodeUrl from xvideo_detail where episodeUrl = "%s" ' % (item["episodeUrl"])
        self.cursor.execute(sqlEpisodeExist)
        result = self.cursor.fetchone()
        if not result: #不存在
            #写集数入表
            sqlInVideoEpisode = """ insert into xvideo_detail(name,image,type,updateTime,episodeUrl,source)
                                    value(%s,%s,%s,%s,%s,%s)"""
            videoEpisodeData = (item["name"],item["image"],item["type"],item["updateTime"],item["episodeUrl"],item["source"])
            self.cursor.execute(sqlInVideoEpisode,videoEpisodeData)
            self.connect.commit()
            spider.logger.info("%s的%s地址已写入xvideo_detail表"%(item["name"],item["episodeUrl"]))
        else: #集数在，不处理
            spider.logger.info("%s 的 %s 已存在xvideo_detail表"%(item["name"],item['episodeUrl']))
        return item
