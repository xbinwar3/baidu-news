# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings
import pymysql
import datetime

class Baidu01Pipeline:
    
    def open_spider(self, spider):
        self.fp = open('news.json', 'w', encoding='utf-8')
        
    def process_item(self, item, spider):
        self.fp.write(str(item)+"\n")
        return item

    def close_spider(self, spider):
        self.fp.close()
       

class Baidu01DownloadPipeline:
    def process_item(self, item, spider):

        return item


class ScrapyDataBasesPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.database = settings['DB_DATABASE']
        self.charset = settings['DB_CHARSET']
        self.connect()
    def connect(self):
        self.conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            charset = self.charset,
            db = self.database,
        )
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        csql= 'SELECT COUNT(*) FROM (SELECT * FROM baidu_news  ORDER BY id DESC LIMIT 200) a WHERE url= "{}"'.format(item['url']);
        self.cursor.execute(csql)
        cnt = self.cursor.fetchone()[0]
        print('count:' + str(cnt))
        if cnt == 0 :
            sql = 'insert into baidu_news(name,url,create_time) values("{}","{}","{}")'.format(item['name'], item['url'],datetime.datetime.now())
            self.cursor.execute(sql)
 
        self.conn.commit()
    
    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()