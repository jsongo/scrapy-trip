#!/usr/bin/env python
# coding=utf-8
import sys
from scrapy.crawler import CrawlerProcess

from trip.spiders.breadCity import BreadCitySpider
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    '''
    {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Referer': 'https://www.google.com.hk/',
    }
    '''
    process = CrawlerProcess(get_project_settings())

    process.crawl(BreadCitySpider, spiderUrl=sys.argv[1])
    process.start()
