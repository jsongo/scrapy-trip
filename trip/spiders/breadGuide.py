#!/usr/bin/env python
# coding=utf-8
import scrapy
import re
from scrapy.selector import Selector
from trip.items import ProductItem, GuideItem
# from scrapy import log
import logging
from scrapy.http import Request
import json as JSON

log = logging.getLogger()

class BreadGuideSpider(scrapy.Spider):
    name = "breadGuide"
    allowed_domains = ["web.breadtrip.com"]
    guideUrl = 'http://web.breadtrip.com/hunter/%s/v2/'
    baseDomain = 'http://web.breadtrip.com'

    def __init__(self, urls=[], *args, **kwargs):
        super(BreadGuideSpider, self).__init__(*args, **kwargs)
        self.urls = urls

    def start_requests(self):
        for data in self.urls:
            uid = data['id']
            url = self.guideUrl % uid
            self.start_urls.append(url)
            yield self.make_requests_from_url(url, {'uid': uid})

    def make_requests_from_url(self, url, meta):
        return Request(url, callback=self.parse, dont_filter=True, meta=meta, headers={
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'https://www.google.com.hk/',
        }, cookies={
            'btuid': '0677ddba6c6311e6aee7061ada095ede'
        })
        # FormRequest(url="http://www.example.com/post/action", formdata={'name': 'John Doe', 'age': '27'}, callback=self.after_post)

    def parse(self, response):
        selector = Selector(response)
        # products
        preLevel = response.xpath('//section[@class="experience"]/ul/li')
        for level in preLevel:
            url = level.xpath('@data-url').extract()[0]
            id = url.split('/')[-2]
            url = self.baseDomain + url

            prod = ProductItem()
            prod['id'] = int(id)
            prod['url'] = url 
            log.debug(prod)
            # info, 补充或更新
            infoDom = level.xpath('div[@class="info"]')
            soldCount = infoDom.xpath('span[@class="badge"]/text()').extract()
            if soldCount:
                m = re.search('(\d+)', soldCount[0])
                soldCount = int(m.group(1))
                prod['soldCount'] = soldCount 
            likes = infoDom.xpath('//span[@class="like-count"]/text()').extract()
            if likes:
                m = re.search('(\d+)', likes[0])
                likes = int(m.group(1))
                prod['likes'] = likes 
            tagDom = infoDom.xpath('p[contains(@class, "label")]/span')
            tags = []
            for dom in tagDom:
                tags.append(dom.xpath('text()').extract()[0])
            prod['tags'] = tags

            yield prod
        
        meta = response.request.meta;
        uid = meta['uid']
        # guide
        guide = GuideItem()
        guide['id'] = uid
        profile = response.xpath('//div[@class="profile"]')[0]
        d1 = profile.xpath('//div[@class="top-inner"]/div[contains(@class, "block")]/span/text()').extract()
        guide['fans'] = int(d1[0])
        guide['stars'] = int(d1[1]) # 关注
        guide['level'] = int(profile.xpath('//div[@class="level"]/text()').extract()[0][3:])
        brief = profile.xpath('//div[contains(@class, "middle")]/p/text()')
        if brief:
            brief = brief.extract()[0]
            brief = brief.split(u' ／ ')
            guide['major'] = brief[0]
            if len(brief) > 1:
                guide['hometown'] = brief[1]
        guide['intro'] = profile.xpath('//div[@class="about-me"]/p/text()').extract()[0]
        comment = response.xpath('//section[contains(@class, "comment")]/h1/i/text()')
        if comment:
            guide['commentCnt'] = int(comment.extract()[0])
        verifications = response.xpath('//section[@class="hunter-verify"]/ul/li/text()').extract()
        log.debug(verifications)
        guide['verify'] = verifications
        log.debug(guide)
        yield guide
