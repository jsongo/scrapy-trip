#!/usr/bin/env python
# coding=utf-8
import scrapy
from scrapy.selector import Selector
from trip.items import CityItem 
from scrapy import log
import json as JSON

class BreadCitySpider(scrapy.Spider):
    name = "breadCity"
    allowed_domains = ["web.breadtrip.com"]
    baseDomain = 'http://web.breadtrip.com'

    def __init__(self, spiderUrl=None, *args, **kwargs):
        super(BreadCitySpider, self).__init__(*args, **kwargs)
        self.start_urls = [ ] 
        if not spiderUrl: 
            spiderUrl = '/scenic/1/3793/city/more/?next_start=0'
        log.msg('visit url=%s' % spiderUrl, level=log.INFO)
        self.start_urls.append(self.baseDomain + spiderUrl)

    def parse(self, response):
        log.msg('got the data', level=log.INFO)
        data = JSON.loads(response.body)
        # cnt = 2
        for city in data['cities']:
            # cnt -= 1
            # if cnt < 0:
                # break
            item = CityItem()
            link = city['url']
            img = city['cover']
            index = img.rfind('?')
            index = index if index >= 0 else 0
            img = img[:index]

            item['nameCn'] = city['name']
            item['id'] = link[len('/scenic/3/'):-1]
            item['src'] = 'bread'
            item['url'] = self.baseDomain + link
            item['img'] = img
            item['wishTo'] = city['wishto_count']
            item['beenTo'] = city['beento_count']
            yield item
        yield {
            'nextUrl': data['next_url'],
            'more': data['more'],
            'nextStart': data['next_start']
        }
