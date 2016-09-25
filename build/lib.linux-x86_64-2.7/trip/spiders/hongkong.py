#!/usr/bin/env python
# coding=utf-8
import scrapy
from scrapy.selector import Selector
from trip.items import TripItem 

class HongkongSpider(scrapy.Spider):
    name = "hongkong"
    allowed_domains = ["web.breadtrip.com"]
    start_urls = [
        'http://web.breadtrip.com/scenic/1/3814/sight/'
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        # selector = Selector(response)
        sels = response.xpath('//ul[@id=dropdown-menu]/*[@class=one-row-ellipsis]')
        # print sels
        for sel in sels:
            item = TripItem()
            item['name'] = sel.xpath('text()').extract()
            yield item
