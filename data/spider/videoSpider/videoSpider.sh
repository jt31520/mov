#! /bin/sh
source /etc/profile
cd /data/spider/videoSpider/
nohup scrapy crawl ok -a mainurl=http://www.okzyw.com/ -a num=1 -a page=3 >> /var/log/spider/movie/log_$(date +\%Y-\%m-\%d).log 2>&1 &

