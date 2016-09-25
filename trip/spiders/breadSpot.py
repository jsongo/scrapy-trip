#!/usr/bin/env python
# coding=utf-8
import scrapy
from scrapy.selector import Selector
from trip.items import SpotItem 
from scrapy import log
import json as JSON

class BreadSpotSpider(scrapy.Spider):
    name = "breadSpot"
    allowed_domains = ["web.breadtrip.com"]
    baseDomain = 'http://web.breadtrip.com/'
    start_urls = [
        # 'http://web.breadtrip.com/scenic/1/3814/sight/'
        baseDomain + 'scenic/1/3814/sight/more/?next_start=0'
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        # selector = Selector(response)
        # sels = response.xpath('//ul[@class="poi-list"]/li')
        # with open('resutl.html', 'rw') as f:
            # f.write(sels)
        log.msg('got the data', level=log.INFO)
        data = JSON.loads(response.body)
        nextUrl = self.baseDomain + data['next_url']
        log.msg('next url=%s' % nextUrl, level=log.INFO)
        # self.start_urls.append(self.baseDomain + nextUrl) 
        items = []
        for d in data['sights']:
            item = SpotItem()
            item['name'] = d['name']
            item['latitude'] = d['latitude']
            item['longitude'] = d['longitude']
            item['hot'] = d['visited_count']
            item['description'] = d['description']

            img = d['cover']
            img = img[:img.find('?')]
            item['img'] = img

            items.append(item)

            # item['nextUrl'] = nextUrl
            # log.msg(item, level=log.INFO)
            # yield item
        return items
