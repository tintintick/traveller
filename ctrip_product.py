# -*- coding:utf-8 -*-

import requests
import json
import common
from lxml import etree


class CtripSaleProductsClass(object):
    def __init__(self):
        self.url_dict = {'host': 'http://vacations.ctrip.com',
                         'path': '/Package-Booking-Promotion/jsondataprovider/Query',
                         'args': {}
                         }

        self.data = {'Data': '{"GroupId":"1",'
                             '"ChannelId":"1",'
                             '"DestinationId":"0",'
                             '"DepartureDate":null,'
                             '"DepartureCityId":"0",'
                             '"Channel":"1",'
                             '"PageIndex":1,'
                             '"SaleCity":0'
                             '}',
                     'QType': 'queryv3'
                     }

        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://vacations.ctrip.com",
            "Referer": "http://vacations.ctrip.com/deals/grouptravel",
            "X-Requested-With": "XMLHttpRequest"
        }

    def request_products(self, method):
        if method == 'get':
            url = common.compose_url(self.url_dict)
            response = requests.get(url, headers=self.header).content.decode('gb2312')
            return response
        if method == 'post':
            self.url_dict['path'] = '/Package-Booking-Promotion/jsondataprovider/Query'
            url = common.compose_url(self.url_dict)
            response = requests.post(url, data=self.data, headers=self.header).content.decode('gb2312')
            cjson = json.loads(response)
            return cjson

    def extract_first_page_products(self):
        response = self.request_products('get')
        page_tree = etree.HTML(response)
        products = page_tree.xpath('//ul[@class ="basefix"]/li/a')
        item = {}
        for product in products:
            item['url'] = product.xpath('./@href')[0]
            pro_info = product.xpath('./div[@class="pro_info"]')[0]
            item['type'] = pro_info.xpath('./h3/span/text()')[0][1:-1]
            item['pname'] = pro_info.xpath('./h3/text()')[0]
            item['deptcity'] = item['pname'].split('出发'.decode('utf-8'))[0].split('[')[-1]
            item['pprice'] = pro_info.xpath('./div/div[2]/div[1]/span/text()')[0]
            item['discount'] = pro_info.xpath('./div/div[2]/div[2]/text()')[0]

            pro_detail = product.xpath('./div[@class="hover_pro_detial"]')[0]
            txt_info = pro_detail.xpath('./div[1]/p/text()')

            item['deptdate'] = ''
            item['description'] = ''
            for txt in txt_info:
                if '出发日期'.decode('utf-8') in txt:
                    item['deptdate'] = txt.split('：'.decode('utf-8'))[-1]
                else:
                    item['description'] += txt + '/'
            item['oprice'] = pro_detail.xpath('./div[2]/div/del/text()')[0]
            # store item into db
            pass

    def extract_product_json(self, cjson):
        if cjson['Msg'] != 'success':
            print 'get product json error\n'
            return None
        product_sum = cjson['PkgsCount']
        products = cjson['Pkgs']
        item = {}
        for product in products:
            item['description'] = product['BriefIntroduction2']
            item['deptcity'] = product['DepartureCityName']
            item['deptdate'] = product['Highlight3'].split('：'.decode('utf-8'))[1]
            item['pname'] = product['ProductName']
            item['type'] = product['ProductTypeName']
            item['url'] = product['ProductUrl']
            item['pprice'] = product['SalesPrice']
            item['oprice'] = product['OriginalPrice']
            item['discoutn'] = product['Discount']
            pass

    def get_products(self):
        page_path = ['/deals/grouptravel',  # GroupId":"1","ChannelId":"1"Channel:1
                     '/deals/freetravel',  # GroupId":"2","ChannelId":"2 Channel:2
                     '/deals/localtravel',  # GroupId":"5","ChannelId":"4 Channel:4
                     # '/deals/cruise',       #
                     '/deals/selfdriving']  # GroupId":"3","ChannelId":"4 Channel:4
        for path in page_path:
            self.url_dict['path'] = path
            self.extract_first_page_products()
            cjson = self.request_products('post')
            self.extract_product_json(cjson)
