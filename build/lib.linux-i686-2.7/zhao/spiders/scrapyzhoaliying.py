import datetime
import urlparse
import socket
import scrapy
import json

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.http import Request

from zhao.items import PicItem
import requests

class ApiSpider(scrapy.Spider):
    name = 'zhao'
    allowed_domains = ["pic.sogou.com"]

    # Start on the first index page
    url = 'http://pic.sogou.com/pics?query=%D5%D4%C0%F6%D3%B1&mode=1&start={}&reqType=ajax&reqFrom=result&tn=0';
    urls = []
    for n in range(0,196,48):
        aurl = url.format(n) 
        urls.append(aurl) 
 
    start_urls = (urls)

    # Format the URLs based on the API call response
    def parse(self, response):
        resp = requests.get(response.url)
        js = resp.json()['items']
        
        img = []
        for item in js:
            imgurl = item['pic_url_noredirect']
            if imgurl != None:
                img.append(imgurl)
        
        # Create the loader using the response
        l = ItemLoader(item=PicItem(), response=response)

        # Load fields using XPath expressions
        l.add_value('image_urls', img,
                    MapCompose(unicode.strip))

        return l.load_item()        

