# -*- coding:utf-8 -*-

import requests
import json
import re
import common


def extract_flight_info(flights, city_name):
    item = {}
    for flight in flights:
        item['from'] = city_name
        item['to'] = flight['aCityName']
        item['ddate'] = flight['flightDetail']['departDateString']
        item['dweekday'] = flight['flightDetail']['departWeekday']
        item['dflightno'] = flight['flightDetail']['departFlightNo']
        item['rdate'] = flight['flightDetail']['returnDateString']
        item['rweekday'] = flight['flightDetail']['returnWeekday']
        item['rflightno'] = flight['flightDetail']['returnFlightNo']
        item['duration'] = flight['flightDetail']['duration']
        item['price'] = flight['totalNetPrice']
        item['discount'] = flight['discountRate']
        # store item into db
        print item
        item.clear()


class CtripFlightsClass(object):
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://vacations.ctrip.com",
            "Referer": "http://vacations.ctrip.com/deals/grouptravel",
            "X-Requested-With": "XMLHttpRequest"
        }
        pass

    def get_cities(self):
        url_dict = {'host': 'http://webresource.c-ctrip.com',
                    'path': '/code/cquery/resource/address/flight/fuzzy_start_poi_timezone_gb2312.js??CR_2016_04_26_00_00_00',
                    'args': {}
                    }
        url = common.compose_url(url_dict)

        response = requests.get(url, headers=self.header).content[56:-1].decode('gb2312')
        ret = re.sub('\"', '\'', response)
        ret = re.sub('display', '\'display\'', ret)
        ret = re.sub('data', '\'data\'', ret)
        ret = eval(ret)

        cities = {}

        for alpha in 'ABCDEF':
            for city in ret['ABCDEF'][alpha]:
                city = city['data'].split('|')[1].split('(')
                cities[city[0]] = city[1][:-1]

        for alpha in 'GHIJ':
            if alpha != 'I':
                for city in ret['GHIJ'][alpha]:
                    city = city['data'].split('|')[1].split('(')
                    cities[city[0]] = city[1][:-1]

        for alpha in 'KLMN':
            for city in ret['KLMN'][alpha]:
                city = city['data'].split('|')[1].split('(')
                cities[city[0]] = city[1][:-1]

        for alpha in 'PQRSTUVW':
            if alpha not in 'UV':
                for city in ret['PQRSTUVW'][alpha]:
                    city = city['data'].split('|')[1].split('(')
                    cities[city[0]] = city[1][:-1]

        for alpha in 'XYZ':
            for city in ret['XYZ'][alpha]:
                city = city['data'].split('|')[1].split('(')
                cities[city[0]] = city[1][:-1]

        return cities

    def get_flights(self):
        cities = self.get_cities()
        post_data = {"inputDepartureCity": "",
                     "inputDepartureCityName": "",
                     "travelType": "",
                     "departStringDate": "任何时间",
                     "departDateRanges": [],
                     "inputArrivalCities": {"themes": [], "cities": [], "areas": []},
                     "inputArrivalCitiesMap": {"themes": [], "cities": [], "areas": [], "filter": {}},
                     "sortingType": "PRICE_ASC",
                     'inputDepartureCity': '',
                     'inputDepartureCityName': '',
                     'travelType': '',
                     "isSearchPage": 'true',
                     "isIncludedTax": 'true'
                     }

        # post city search data
        for key, value in cities:
            url = 'http://flights.ctrip.com/fuzzy/search'
            post_data['inputDepartureCityName'] = key
            post_data['inputDepartureCity'] = value

            # ONEWAY
            post_data['travelType'] = 'ONEWAY'
            data = json.dumps(post_data)
            self.header['Content-Type'] = 'application/json; charset=utf-8'
            response = requests.post(url, data=data, headers=self.header).content
            ret = json.loads(response)['fuzzyFlightList']
            if len(ret) is not 0:
                flights = ret[0]['flightResultList']
                extract_flight_info(flights, key)
                print 'OK'

                # ROUNDTRIP
                # travelType = 'ROUNDTRIP'
                # temp['travelType'] = travelType
                # data = json.dumps(temp)[:-1] + ' ,"isSearchPage":true, "isIncludedTax":true' + '}'
                # ret = json.loads(requests.post(url, data=data, headers=header).content)['fuzzyFlightList']
                # if len(ret) is not 0:
                #     flights = ret[0]['flightResultList']
                #     getInfo(flights, city)
                #     print 'OK'

# cities = getCities()
# getTickets(cities)
