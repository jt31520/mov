#! /bin/sh
name=$1
mainurl=$2
num=$3
page=$4
source /etc/profile
cd /data/spider/xvideoSpider/
nohup scrapy crawl $name  -a mainurl=$mainurl -a num=$num -a page=$page >>/var/log/spider/xmovie/log_$(date +\%Y-\%m-\%d).log 2>&1 &

