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
        sqlEpisodeExist = 'select name from film_video_episode where name = "%s" and episode = "%s"' % (item["name"],item["episode"])
        self.cursor.execute(sqlEpisodeExist)
        result = self.cursor.fetchone()
        nameMd5 = hashlib.md5(item["name"].encode(encoding='UTF-8')).hexdigest()
        if not result: #不存在
            #写集数入表
            sqlInVideoEpisode = """ insert into film_video_episode(name,nameMd5,episode,episodeUrl,episodeMd5)
                                    value(%s,%s,%s,%s,%s)"""
            # episodeMd5 = hashlib.md5(item["episode"].encode(encoding='UTF-8')).hexdigest()[0:10]
            videoEpisodeData = (item["name"],nameMd5,item["episode"],item["episodeUrl"],item["episodeInt"])
            self.cursor.execute(sqlInVideoEpisode,videoEpisodeData)
            self.connect.commit()
            spider.logger.info("%s的第%s集已写入video_episode集数表"%(item["name"],item["episode"]))

            #判断详细信息在不在
            sqlIsExist = 'select name from film_video_detail where name = "%s"' % (item["name"])
            self.cursor.execute(sqlIsExist)
            result = self.cursor.fetchone()

            if not result: #不在则写入
                spider.logger.info("%s 不在video_detail详情表" % (item["name"]))
                sqlInVideoDetail = """ insert into film_video_detail(name,nameMd5,image,updateTo,score,alias,director,star,type,region,language,issueTime,filmLength,updateTime,
                                    details,totalPlay,todayPlay,totalScore,scoreTime,source)
                                  value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                videoDetailData = (
                item["name"], nameMd5, item["image"], item["updateTo"], item["score"], item["alias"], item["director"],
                item["star"]
                , item['type'], item["region"], item["language"], item["issueTime"], item["filmLength"],
                item["updateTime"]
                , item["details"], item["totalPlay"], item["todayPlay"], item["totalScore"], item["scoreTime"],
                item["source"])
                self.cursor.execute(sqlInVideoDetail, videoDetailData)
                self.connect.commit()
                spider.logger.info("%s 已写入video_detail详情表" % (item["name"]))
            else: #在则更新
                spider.logger.info("%s 已存在video_detail详情表" % (item["name"]))
                sqlUpdateDetail = "update film_video_detail set updateTo=%s,updateTime=%s,type=%s where nameMd5=%s"
                sqlUpdateData = (item['updateTo'], item['updateTime'], item['type'], nameMd5)
                self.cursor.execute(sqlUpdateDetail, sqlUpdateData)
                self.connect.commit()
                spider.logger.info("%s 已在video_detail详情表更新 更新的值为%s" % (item['name'],sqlUpdateData))
        else: #集数在，不处理
            spider.logger.info("%s 的 %s 已存在video_episode集数表"%(item["name"],item['episode']))
        return item
