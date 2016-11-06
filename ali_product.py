# -*- coding:utf-8 -*-
import requests
from lxml import etree
import json


def extract_products(ajson):
    products = ajson['items']
    item = {}
    for product in products:
        if product['dep'] is None:
            item['deptcity'] = ''
        else:
            item['deptcity'] = product['dep']

        item['arrcity'] = product['dest']
        item['url'] = product['itemUrl']
        # item['picurl'] = product['picUrlTms']
        item['type'] = product['holidayType']
        item['date'] = product['tuanTime']
        item['pprice'] = product['activityPrice']
        item['oprice'] = product['originalPrice']
        item['discount'] = product['saleCount']
        item['description'] = product['shortNameTms']
        # store item into db
        print item
        item.clear()


class AliProductsClass(object):
    def __init__(self):
        self.url = 'https://traveln.alitrip.com/temai?spm=181.64014.256151.7.8vK6wv'
        self.header = {':authority': 'traveln.alitrip.com',
                       'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'accept-encoding': 'gzip, deflate, sdch, br',
                       'accept-language': 'en-US,en;q=0.8',
                       'cache-control': 'max-age=0',
                       'referer': 'https://temai.alitrip.com/?spm=181.64014.191938.38.KzEuL1',
                       'upgrade-insecure-requests': 1,
                       'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'
                       }

    def get_products(self):
        response = requests.get(self.url).content
        page_tree = etree.HTML(response)
        ajson = json.loads(page_tree.xpath('//script')[-2].text[45:-7])
        if not ajson['success']:
            print 'get page error!'
            return None
        extract_products(ajson)

