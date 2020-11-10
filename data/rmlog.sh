#! /bin/sh
source /etc/profile

#删除spider15天前的日志
find /var/log/spider/movie/ -mtime +15 -name '*.log' -exec rm -rf {} \;
find /var/log/spider/xmovie/ -mtime +15 -name '*.log' -exec rm -rf {} \;


