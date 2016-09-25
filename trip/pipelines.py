# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
# import time
import datetime
# from scrapy import log
import logging
from twisted.internet import reactor
from trip.spiders.breadRegion import BreadRegionSpider
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

log = logging.getLogger()

conn = MongoClient('127.0.0.1', 27018)
breadDB = conn['bread']
db = conn['clover']

class TripPipeline(object):
    curCnt = 0

    def process_item(self, item, spider):
        log.debug('pipelines processing item')

        now = datetime.datetime.now()
        dateStr = now.strftime('%Y%m%d%H%M%S')
        item['scrawlDate'] = dateStr

        if spider.name == 'breadDests':
            breadDB.country.update({'nameEn': item['nameEn']}, {'$set': dict(item)}, True)
            self.curCnt += 1 
            # self.runBreadRegion(item['url'])
            log.debug('==>current = %d, %s' % (self.curCnt, item['nameCn']))
        elif spider.name == 'breadCity':
            if item.get('more'):
                # visit next page
                nextUrl = item['nextUrl']
                log.debug('has more. next url= %s' % nextUrl)
                os.popen('python runBreadCity.py %s' % nextUrl)
            elif item.get('id'): # 保存
                log.msg(item, level=log.INFO)
                db.city.update({'id': item['id']}, {'$set': dict(item)}, True)
        elif spider.name == 'breadCityDetail':
            if type(item) == dict:
                db.city.update({'id': item['id']}, {'$set': item}, True)
            else:
                breadDB.province.update({'id': item['id']}, {'$set': dict(item)}, True)
        elif spider.name == 'breadSpots':
            if item.get('more') == False: 
                # 加载完了
                cityId = item['cityId']
                log.debug('finished, cityId=%s' % cityId)
                result = db.city.update({'id': cityId}, {'$set': {'crawled': True}}, True)
                # time.sleep(0.5)
                log.debug(result)
            elif item.get('id'): # 保存
                self.curCnt += 1; 
                log.debug('==>%d' % self.curCnt)
                db.spot.update({'id': item['id']}, {'$set': dict(item)}, True)
            elif item.get('more'):
                # visit next page
                nextUrl = item['nextUrl']
                log.debug('has more. next url= %s' % nextUrl)
                os.popen('python runBreadSpotItem.py %s %s' % (nextUrl, item['cityId']))
            else:
                log.debug(item)
        elif spider.name == 'breadProduct':
            if item.get('more') == False: 
                cityId = item['cityId']
                log.debug('finished, cityId=%s' % cityId)
                result = db.city.update({'id': cityId}, {'$set': {'prodCrawled': True}}, True)
            elif item.get('id'): # 保存
                from trip.items import GuideItem, ProductItem
                if isinstance(item, ProductItem):
                    db.product.update({'id': item['id']}, {'$set': dict(item)}, True)
                    log.debug('product saved')
                elif isinstance(item, GuideItem):
                    db.guide.update({'id': item['id']}, {'$set': dict(item)}, True)
                    log.debug('guide saved')
            elif item.get('more'):
                nextUrl = item['nextUrl']
                log.debug('has more. next url= %s' % nextUrl)
                os.popen('python runBreadProduct.py "%s" %s' % (nextUrl, item['cityId']))
            else:
                log.error(item)
        elif spider.name == 'breadGuide':
            from trip.items import GuideItem, ProductItem
            if isinstance(item, ProductItem):
                pid = item.get('id')
                if pid:
                    prod = db.product.find({'id': pid})
                    if prod.count() <= 0:
                        log.debug('--==>warning... a new product found !')
                        breadDB.leaks.update({'id': pid}, {'$set': dict(item)}) 
                    else:
                        db.product.update({'id': pid, 'tags': {'$exists': False}}, {'$set': dict(item)})
                        log.debug('update product tags info and so on!')
            elif isinstance(item, GuideItem):
                db.guide.update({'id': item['id']}, {'$set': dict(item)}, True)
                log.debug('guide updated')
        elif spider.name == 'breadProdPage':
            from trip.items import GuideItem, ProductItem
            if isinstance(item, ProductItem):
                db.product.update({'id': item['id']}, {'$set': dict(item)}, True)
                log.debug('product saved')
            elif isinstance(item, GuideItem):
                db.guide.update({'id': item['id']}, {'$set': dict(item)}, True)
                log.debug('guide saved')
        return item
    
    def runBreadRegion(self, url):
        os.popen('python runBreadRegion.py %s' % url)
        # process = CrawlerProcess({
            # 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        # })

        # process.crawl(BreadRegionSpider, spiderUrl=url)
        # process.start()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass
