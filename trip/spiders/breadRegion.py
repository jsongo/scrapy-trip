#!/usr/bin/env python
# coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy import log
import json as JSON

class BreadRegionSpider(scrapy.Spider):
    name = "breadRegion"
    allowed_domains = ["web.breadtrip.com"]

    def __init__(self, spiderUrl=None, *args, **kwargs):
        super(BreadRegionSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            spiderUrl
        ]

    def parse(self, response):
        log.msg('visit url %s' % self.start_urls, level=log.INFO)
        return JSON.loads(response.body)
