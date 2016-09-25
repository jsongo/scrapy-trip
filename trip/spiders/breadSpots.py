#!/usr/bin/env python
# coding=utf-8
import scrapy
import re
from scrapy.selector import Selector
from trip.items import SpotItem 
# from scrapy import log
# from logging import Logger as log
import logging
from scrapy.http import Request
import json as JSON

log = logging.getLogger()

class BreadSpotsSpider(scrapy.Spider):
    name = "breadSpots"
    allowed_domains = ["web.breadtrip.com"]
    baseDomain = 'http://web.breadtrip.com'

    def __init__(self, urls=[], spiderUrl=None, cityId=None, *args, **kwargs):
        super(BreadSpotsSpider, self).__init__(*args, **kwargs)
        self.urls = urls
        self.spiderUrl = spiderUrl 
        # self.cityId = cityId
        # log.msg('url count=%d' % len(self.start_urls), level=log.INFO)

    def start_requests(self):
        if self.urls:
            for data in self.urls:
                url = data['url']
                self.start_urls.append(url)
                cid = data['id']
                yield self.make_requests_from_url(url, {'cid': cid})
        else:
            self.start_urls.append(self.spiderUrl)
            yield self.make_requests_from_url(self.spiderUrl, {})

    def make_requests_from_url(self, url, meta):
        return Request(url, callback=self.parse, dont_filter=True, meta=meta, headers={
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'https://www.google.com.hk/',
        }, cookies={
            'btuid': '0677ddba6c6311e6aee7061ada095ede'
        })
        # FormRequest(url="http://www.example.com/post/action", formdata={'name': 'John Doe', 'age': '27'}, callback=self.after_post)

    def parse(self, response):
        url = response.request.url
        cityId = url.split('/')[-4]
        log.debug('got the data, cityId=%s, url len=%d' % (cityId, len(self.start_urls)))
        data = JSON.loads(response.body)
        # cnt = 1
        for city in data['sights']:
            # cnt -= 1
            # if cnt < 0:
                # break
            item = SpotItem()
            link = city['url']
            img = city['cover']
            index = img.rfind('?')
            index = index if index >= 0 else 0
            img = img[:index]
            id = link.split('/')[-2]

            item['name'] = city['name']
            item['whereFrom'] = url
            item['id'] = id
            item['parent'] = cityId
            item['src'] = 'bread'
            item['url'] = self.baseDomain + link
            item['img'] = img
            item['latitude'] = city['latitude']
            item['longitude'] = city['longitude']
            item['visit'] = city['visited_count']
            item['wishTo'] = city['wish_to_go_count']
            item['description'] = city['description']
            # log.msg(item, level=log.INFO)
            yield item
        yield {
            'nextUrl': self.baseDomain + data.get('next_url', ''),
            'more': data.get('more', False),
            'cityId': cityId,
            'nextStart': data.get('next_start')
        }
