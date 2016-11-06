# -*- coding:utf-8 -*-

import requests
import json


def extract_flights_info(flights):
    item = {}
    for flight in flights:
        item['deptcity'] = flight['dc'].encode('utf-8')
        item['arrcity'] = flight['ac'].encode('utf-8')
        item['price'] = flight['pr']
        item['discount'] = flight['dis']
        item['date'] = flight['dd'].encode('utf-8')
        item['time'] = flight['dt'].encode('utf-8')
        item['source'] = 'qunar'
        item[
            'url'] = 'http://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport={0}&searchArrivalAirport={1}&searchDepartureTime={2}'.format(
            item['deptcity'], item['arrcity'], item['date'])
        # print item
        item.clear()
        # store it into mongodb


def compose_url(url, city, curdate, page):
    url = "{0}&dcity={1}&ddate={2}&page={3}".format(url, city.encode('utf-8'), curdate, str(page))
    return url


class QunarFlightClass(object):
    def __init__(self, url, curdate):
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        self.url = url
        self.curdate = curdate

    def get_cities(self):
        url = "http://lp.flight.qunar.com/api/qdclowprice?callback=qjson&drange=7&query=search&sort=S1&asc=true&page=1&from=tejia_d_mr&ex_track=&searchType=domestic&per=40&perScrollPage=10&_=abc&ddate="
        qjson = json.loads(requests.get(url + self.curdate, headers=self.header).content[6:-2])['options']['dcity_more']
        cities = []
        for item in qjson:
            for city in item['list']:
                cities.append(city['key'])

        return cities

    def get_flights(self, cities):
        pagenum = 1

        for city in cities:
            # get totoal page number
            url = compose_url(self.url, city, self.curdate, pagenum)
            qjson = json.loads(requests.get(url, headers=self.header).content[6:-2])
            page_sum = int(qjson['data']['info']['tp'])
            # flight_sum = int(qjson['data']['info']['total'])
            extract_flights_info(qjson['data']['list'])

            # get flights
            for page in range(2, page_sum + 1):
                url = compose_url(self.url, city, self.curdate, pagenum)
                flights = json.loads(requests.get(url, headers=self.header).content[6:-2])['data']['list']
                extract_flights_info(flights)


                # if amount != flight_sum:
                #     print "{0} flight number is error, amount is {1}".format(city, amount)
                #     exit()
