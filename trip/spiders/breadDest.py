#!/usr/bin/env python
# coding=utf-8
import scrapy
from scrapy.selector import Selector
from trip.items import BreadCountryItem
from scrapy import log
import json as JSON

class BreadDestsSpider(scrapy.Spider):
    name = "breadDests"

    rootUrl = 'http://web.breadtrip.com'
    allowed_domains = ["web.breadtrip.com"]
    start_urls = [
        'http://web.breadtrip.com/destinations/'
    ]

    def parse(self, response):
        selector = Selector(response)
        sels = response.xpath('//div[@id="foreign-dest-popup"]/div[@class="content"]/ul/li/div[@class="level-2 float-left"]') # @id="domestic-dest-popup" or 
        log.msg('got the data: %s' % len(sels), level=log.INFO)
        # cnt = 4
        for sel in sels:
            item = BreadCountryItem()
            link = sel.xpath('a/@href').extract()[0] 
            item['url'] = self.rootUrl + link
            item['nameCn'] = sel.xpath('a/span[@class="ellipsis_text"]/text()').extract()[0]
            item['nameEn'] = link[1:-1]

            # cnt -= 1
            # if cnt <= 0:
                # break
            yield item
