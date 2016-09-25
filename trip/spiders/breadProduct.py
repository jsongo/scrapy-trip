#!/usr/bin/env python
# coding=utf-8
import scrapy
import re
from scrapy.selector import Selector
from trip.items import ProductItem, GuideItem, TagItem
# from scrapy import log
# from logging import Logger as log
import logging
from scrapy.http import Request
import json as JSON

log = logging.getLogger()

class BreadProductSpider(scrapy.Spider):
    name = "breadProduct"
    allowed_domains = ["web.breadtrip.com"]
    baseDomain = 'http://web.breadtrip.com'

    def __init__(self, spiderUrl=None, cityId=None, *args, **kwargs):
        super(BreadProductSpider, self).__init__(*args, **kwargs)
        # self.urls = urls 
        self.spiderUrl = spiderUrl 
        self.cityId = (cityId or 0)

    def start_requests(self):
        self.start_urls = [self.spiderUrl]
        yield self.make_requests_from_url(self.spiderUrl, {'cid': self.cityId})

    def make_requests_from_url(self, url, meta):
        return Request(url, callback=self.parse, dont_filter=True, meta=meta, headers={
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'https://www.google.com/',
        }, cookies={
            'btuid': '0702ddba6c6311e7aee7060ada095ede'
        })

    def parseImg(self, url, sep='?'):
        url = url.replace('\\','')
        url = url[:url.rfind(sep)]
        return url

    def parse(self, response):
        url = response.request.url
        data = JSON.loads(response.body)
        meta = response.request.meta
        cid = meta['cid']
        # cnt = 1
        for prod in data['product_list']:
            # cnt -= 1
            # if cnt < 0:
                # break
            item = ProductItem()
            id = prod['product_id']
            item['id'] = id
            item['whereFrom'] = url
            item['src'] = 'bread'
            item['url'] = self.baseDomain + '/hunter/product/%d/'%id
            item['tags'] = prod['tab_list']
            item['title'] = prod['title']
            banner = self.parseImg(prod['title_page'])
            item['banner'] = banner
            item['onSale'] = prod['can_sell']
            item['likes'] = prod['like_count']
            item['status'] = prod['status']
            item['addressDisplayType'] = prod['address_display_type']
            item['address'] = prod['address']
            item['soldCount'] = prod['sold_count']
            item['dateStr'] = prod['date_str']
            item['stock'] = prod['stock']
            item['cityId'] = int(cid)

            # get user
            user = prod['user']
            guide = GuideItem()
            uid = user.get('id')
            guide['id'] = uid
            guide['name'] = user.get('name')
            guide['avatar'] = self.parseImg(user.get('avatar_l'), '-')
            guide['whereFrom'] = url
            guide['src'] = 'bread'
            guide['url'] = self.baseDomain + '/hunter/%d/v2'%uid
            log.debug(guide)
            yield guide

            item['uid'] = uid
            log.debug(user)
            yield item

        nextStart = data['next_start']
        nextUrl = re.sub('start=\d+', 'start=%d' % nextStart, url)
        # log.debug('==>%s' % cid)
        yield {
            'nextUrl': nextUrl,
            'more': (nextStart > 0),
            'cityId': cid,
            'nextStart': nextStart 
        }
