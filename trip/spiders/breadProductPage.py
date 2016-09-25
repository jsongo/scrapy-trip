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

class BreadProductPageSpider(scrapy.Spider):
    name = "breadProdPage"
    allowed_domains = ["web.breadtrip.com"]
    # guideUrl = 'http://web.breadtrip.com/hunter/%s/v2/'
    baseDomain = 'http://web.breadtrip.com'

    def __init__(self, urls=[], *args, **kwargs):
        super(BreadProductPageSpider, self).__init__(*args, **kwargs)
        self.urls = urls

    def start_requests(self):
        for data in self.urls:
            url = data.get('url')
            pid = data.get('pid')
            exists = data.get('exists')
            self.start_urls.append(url)
            yield self.make_requests_from_url(url, {'pid': pid, 'exists': exists})

    def make_requests_from_url(self, url, meta):
        return Request(url, callback=self.parse, dont_filter=True, meta=meta, headers={
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'https://www.google.com.hk/',
        }, cookies={
            'btuid': '0677ddba6c6311e6aee7061ada095ede'
        })
        # FormRequest(url="http://www.example.com/post/action", formdata={'name': 'John Doe', 'age': '27'}, callback=self.after_post)

    def parseImg(self, url, sep='?'):
        url = url.replace('\\','')
        url = url[:url.rfind(sep)]
        return url

    def parse(self, response):
        meta = response.request.meta;
        pid = meta['pid']
        exists = meta['exists']
        url = response.request.url
        log.debug('%s==>exists: %s' % (pid, exists))

        # selector = Selector(response)
        prod = ProductItem()
        prod['id'] = pid
        prod['url'] = url
        prod['src'] = 'bread' 
        # header banner
        swiperWrapper = response.xpath('//div[@class="swiper-wrapper"]')
        if not swiperWrapper:
            raise Exception('Not such product.... %s' % pid)
        banners = swiperWrapper.xpath('//div[contains(@class, "swiper-slide") and not(contains(@class, "swiper-slide-duplicate"))]/@data-src').extract()
        bs = []
        for banner in banners:
            bs.append(banner[:banner.find('?')])
        # log.debug(bs)
        prod['banners'] = bs
        if not exists:
            prod['banner'] = bs[0]
            prodInfo = response.xpath('//div[@class="product-info"]')
            title = prodInfo.xpath('div[@class="product-title"]/h1/text()').extract()[0]
            prod['title'] = title
            priceDom = prodInfo.xpath('div[@class="product-title"]//span[@class="present-price"]')
            prod['price'] = priceDom.xpath('string()').extract()[0].strip()
            dateDom = prodInfo.xpath('p[@id="calendar"]')
            # log.debug('==>%s' % dateDom)
            if dateDom:
                prod['dateStr'] = dateDom.xpath('string()').extract()[0].strip()
                prod['onSale'] = True
            else:
                prod['onSale'] = False
            # 新的才有
            prod['whereFrom'] = url

            # user
            guide = GuideItem()
            userSec = response.xpath('//div[@id="userInfo"]')
            uid = int(userSec.xpath('@data-id').extract()[0])
            name = userSec.xpath('@data-name').extract()[0]
            guide['id'] = uid
            guide['name'] = name
            avatar = userSec.xpath('img/@src').extract()[0]
            self.parseImg(avatar, '-')
            guide['avatar'] = self.parseImg(avatar, '-')
            prod['uid'] = uid

            guide['whereFrom'] = url
            guide['src'] = 'bread'
            guide['url'] = self.baseDomain + '/hunter/%d/v2'%uid
            # log.debug(guide)
            yield guide
        # brief
        briefs = response.xpath('//div[@class="product-point"]/p')
        intros = []
        for brief in briefs:
            # intros.append(''.join(brief.xpath('//text()').extract()))
            intros.append(brief.xpath('string()').extract()[0]) 
        prod['briefs'] = intros 
        map = response.xpath('//div[@id="address-map"]')
        if map:
            prod['longitude'] = map.xpath('@data-lng').extract()[0]
            prod['latitude'] = map.xpath('@data-lat').extract()[0]
            prod['dest'] = map.xpath('@data-title').extract()[0]
            
        # content
        contents = response.xpath('//div[@id="desc"]/div[@class="content"]/*')
        # log.debug(len(contents))
        details = []
        for dom in contents:
            img = dom.xpath('img/@src')
            if img:
                imgUrl = self.parseImg(img.extract()[0])
                details.append({
                    'type': 'image',
                    'content': imgUrl
                })
            else:
                s = dom.xpath('.').extract()[0]
                if s.startswith('<p>'):
                    details.append({
                        'type': 'text',
                        'content': s[3:-4]
                    })
                elif s.startswith('<p>'):
                    details.append({
                        'type': 'title',
                        'content': s[4:-5]
                    })
        prod['detail'] = details

        # notice
        notices = response.xpath('//div[contains(@class, "tab-1")]')
        # 费用说明
        feeDom = notices.xpath('div[contains(@class, "fee-info")]/div[@class="content"]/*')
        index = -1
        fees = {0: [], 1: []}
        for dom in feeDom:
            s = dom.xpath('.').extract()[0]
            if s.startswith('<h4>'):
                subtitle = s[4:-5]
                if subtitle == u'费用包含':
                    index = 0
                elif subtitle == u'费用不含':
                    index = 1
            elif s.startswith('<p>'):
                text = dom.xpath('string()').extract()[0]
                if text and index >= 0:
                    fees[index].append(text)
        prod['feeTips'] = {
            'include': ';'.join(fees[0]),
            'exclude': ';'.join(fees[1])
        }
        # 预订须知
        bookInfo = notices.xpath('div[contains(@class, "book-info")]/div[@class="content"]/p')
        bookTips = []
        for info in bookInfo:
            text = info.xpath('string()').extract()[0]
            if text:
                bookTips.append(text)
        prod['bookTips'] = bookTips
        # 注意事项
        noticeDom = notices.xpath('div[contains(@class, "notice-info")]/div[@class="content"]/p')
        noticeArr = []
        for dom in noticeDom:
            text = dom.xpath('string()').extract()[0]
            if text:
                noticeArr.append(text)
        prod['noticeTips'] = noticeArr
        # 见面地点
        meetDom = notices.xpath('div[contains(@class, "meet-info")]/p')
        if meetDom:
            meetInfo = []
            for dom in meetDom:
                text = dom.xpath('string()').extract()[0]
                if text:
                    meetInfo.append(text)
            prod['meetInfo'] = meetInfo 
            map = notices.xpath('//div[@id="meet-map"]')
            # log.debug(map)
            if map:
                prod['addr'] = map.xpath('@data-title').extract()[0]
                prod['meetCoordinate'] = {
                    'lat': map.xpath('@data-lat').extract()[0],
                    'lng': map.xpath('@data-lng').extract()[0]
                }

        similarDom = response.xpath('//div[@id="similar-product"]/div[@class="content"]/div[@class="item"]')
        similars = []
        for dom in similarDom:
            attr = dom.xpath('@data-type').extract()[0]
            if attr == 'product':
                pid2 = dom.xpath('@data-id').extract()[0]
                similars.append(int(pid2))
        prod['similars'] = similars

        log.debug(prod)
        yield prod 
