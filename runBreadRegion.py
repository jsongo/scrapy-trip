#!/usr/bin/env python
# coding=utf-8
import sys
from scrapy.crawler import CrawlerProcess

from trip.spiders.breadRegion import BreadRegionSpider

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Referer': 'https://www.google.com.hk/',
    })

    process.crawl(BreadRegionSpider, spiderUrl=sys.argv[1])
    process.start()
