# -*- coding:utf-8 -*-
import requests
import json


def extract_products_info(qjson):
    if qjson['ret'] == 1:
        head_data = qjson['headData']
        for item in head_data:
            city = item['dest'].split('-')
            product = {'days': item['days'],
                       'deptcity': city[0],
                       'arrcity': city[1],
                       'leftday': item['leftday'],
                       'url': item['linkurl'],
                       'oprice': item['market_price'],
                       'pprice': item['price'],
                       'description': item['pdContain'],
                       'discount': item['rate'],
                       'startdate': item['startDate'],
                       'type': item['type']
                       }
            # store product dict into db
            product.clear()


class QunarProductClass(object):
    def __init__(self, url):
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
        }
        self.product_url = url

    def request_products_dict(self, url, pagenum):
        url += str(pagenum)
        response = requests.get(url, headers=self.header)
        qjson = json.loads(response.content[6:-1])

        return qjson

    def get_products(self):
        # first page
        pagenum = 1
        qjson = self.request_products_dict(self.product_url, pagenum)
        extract_products_info(qjson)
        print int(qjson['AllTeamNum'])
        page_sum = int(qjson['AllPageNum'])

        for i in range(2, page_sum + 1):
            qjson = self.request_products_dict(self.product_url, i)
            extract_products_info(qjson)
