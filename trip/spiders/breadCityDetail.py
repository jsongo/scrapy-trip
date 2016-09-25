#!/usr/bin/env python
# coding=utf-8
import scrapy
import re
from scrapy.selector import Selector
from trip.items import BreadProviceItem 
from scrapy import log
from scrapy.http import Request
import json as JSON

class BreadCityDetailSpider(scrapy.Spider):
    name = "breadCityDetail"
    allowed_domains = ["web.breadtrip.com"]
    baseDomain = 'http://web.breadtrip.com'

    def __init__(self, urls=[], *args, **kwargs):
        super(BreadCityDetailSpider, self).__init__(*args, **kwargs)
        self.urls = urls
        # log.msg('url count=%d' % len(self.start_urls), level=log.INFO)

    def start_requests(self):
        for data in self.urls:
            url = data['url']
            self.start_urls.append(url)
            cid = data['id']
            yield self.make_requests_from_url(url, {'cid': cid})

    def make_requests_from_url(self, url, meta):
        return Request(url, callback=self.parse, dont_filter=True, meta=meta, headers={
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'https://www.google.com.hk/',
        }, cookies={
            'btuid': '0677ddba6c6311e6aee7061ada095ede'
        })
        # FormRequest(url="http://www.example.com/post/action", formdata={'name': 'John Doe', 'age': '27'}, callback=self.after_post)

    def parse(self, response):
        if not self.start_urls:
            raise 'fail'
        selector = Selector(response)
        preLevel = response.xpath('//p[@class="hero-info-eng"]/a')[1]
        # log.msg(preLevel, level=log.INFO)
        link = preLevel.xpath('@href').extract()[0]
        tmp = link.split('/')
        level = tmp[-3]
        id = tmp[-2]
        # 记录第2级的信息
        if level == '2': 
            name = preLevel.xpath('text()').extract()[0]
            log.msg('==>: %s' % name, level=log.INFO)
            item = BreadProviceItem()
            item['nameEn'] = name
            item['url'] = self.baseDomain + link 
            item['id'] = id
            yield item

        # 更新城市的图片列表到原city中
        banners = response.xpath('//div[@id="hero-header"]/ul/li')
        styles = banners.xpath('@style').extract()
        imgs = []
        for style in styles:
            img = re.search(r'background-image: url([^?]+)', style).group(1)[1:]
            imgs.append(img)
            log.msg(img, level=log.INFO)
        curData = response.meta
        cityId = curData.get('cid')
        log.msg(cityId, level=log.INFO)
        log.msg(response.request.headers, level=log.INFO)
        yield {
            'imgs': imgs,
            'parent': id,
            'id': cityId
        }
