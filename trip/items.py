# -*- coding: utf-8 -*-

import scrapy

class ProductItem(scrapy.Item):
    id = scrapy.Field()
    tags = scrapy.Field()
    src = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    whereFrom = scrapy.Field() # 抓取的来源
    banner = scrapy.Field()
    onSale = scrapy.Field()
    likes = scrapy.Field()
    status = scrapy.Field() # prebook
    uid = scrapy.Field()
    addressDisplayType = scrapy.Field()
    address = scrapy.Field()
    soldCount = scrapy.Field()
    dateStr = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    cityId = scrapy.Field()
    scrawlDate = scrapy.Field()
    # 下面几个是分开抓，后面补充的
    banners = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    briefs = scrapy.Field()
    detail = scrapy.Field()
    dest = scrapy.Field() # 具体地址
    addr = scrapy.Field() # 见面地点
    meetCoordinate = scrapy.Field() # 见面坐标
    feeTips = scrapy.Field() # dict, 0->fee includes, 1->fee exclude
    bookTips = scrapy.Field()# array
    noticeTips = scrapy.Field()# array
    meetInfo = scrapy.Field()# array, time/place
    similars = scrapy.Field() # id list, from offical site

class GuideItem(scrapy.Item):
    id = scrapy.Field()
    avatar = scrapy.Field()
    name = scrapy.Field()
    fans = scrapy.Field()
    stars = scrapy.Field() # 关注
    level = scrapy.Field()
    major = scrapy.Field()
    hometown = scrapy.Field()
    intro = scrapy.Field()
    commentCnt = scrapy.Field()
    verify = scrapy.Field()
    src = scrapy.Field()
    url = scrapy.Field()
    whereFrom = scrapy.Field() # 抓取的来源
    scrawlDate = scrapy.Field()

class TagItem(scrapy.Item):
    id = scrapy.Field()
    avatar = scrapy.Field()
    name = scrapy.Field()
    scrawlDate = scrapy.Field()

class SpotItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    parent = scrapy.Field()
    src = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    whereFrom = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    hot = scrapy.Field()
    visit = scrapy.Field()
    description = scrapy.Field()
    wishTo = scrapy.Field() # 访问过这个页面
    img = scrapy.Field()
    scrawlDate = scrapy.Field()

class BreadCountryItem(scrapy.Item):
    # define the fields for your item here like:
    nameCn = scrapy.Field()
    url = scrapy.Field()
    nameEn = scrapy.Field()
    scrawlDate = scrapy.Field()

class BreadProviceItem(scrapy.Item):
    # define the fields for your item here like:
    nameCn = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    nameEn = scrapy.Field()
    scrawlDate = scrapy.Field()

class CityItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    nameCn = scrapy.Field()
    nameEn = scrapy.Field()
    src = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    wishTo = scrapy.Field() # 访问过这个页面
    beenTo = scrapy.Field()
    hot = scrapy.Field()
    scrawlDate = scrapy.Field()
