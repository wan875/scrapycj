# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from scrapy.exceptions import DropItem
import json
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy.crawler import Settings as settings
import pymysql
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')


class ScrapycjPipeline(object):
    def process_item(self, item, spider):
        return item

class YunshiPipeline(object):
    #def __init__(self):
        #打开文件
        #self.file = open('data.json', 'w', encoding='utf-8')
    #该方法用于处理数据
    def process_item(self, item, spider):
        dbargs = dict(
            host=spider.settings["DB_HOST"],
            db=spider.settings["DB_DATABASE"],
            user=spider.settings["DB_USER"],  # replace with you user name
            passwd=spider.settings["DB_PASSWORD"],  # replace with you password
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True, )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

        self.db = pymysql.connect(
            host=spider.settings["DB_HOST"],
            db=spider.settings["DB_DATABASE"],
            user=spider.settings["DB_USER"],  # replace with you user name
            passwd=spider.settings["DB_PASSWORD"],  # replace with you password
            charset='utf8'
        )

        res = self.dbpool.runInteraction(self.insert_into_table, item)
        #print(item['title'])
        #读取item中的数据
        #line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #写入文件
        #self.file.write(line)
        #返回item
        return item
    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass
    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass

    def insert_into_table(self, conn, item):
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #item['title'] = MySQLdb.escape_string(item['title'])
        #item['content'] = MySQLdb.escape_string(item['content'])
        item['content'] = item['content'].replace('/storage','https://31qu.cn/storage')
        thumbarr = item['thum'].split('?')

        cursor = self.db.cursor()
        cursor.execute('select id from crawled_post where post_title = %s', (item['title']))
        rs = cursor.fetchall()
        self.db.commit()
        if not rs:
            conn.execute('insert into crawled_post(post_title,post_content,thum,created_at,source,type,url) values(%s,%s,%s,%s,%s,%s,%s)', (item['title'], item['content'], thumbarr[0], nowTime, item['source'], item['type'], item['url']))
