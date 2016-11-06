# -*- coding:utf-8 -*-
import requests
import json
import common
import ctrip_flight


def extract_flight_info(data, dept_city_name, arr_city_name, type_map):
    aircom_map = data['als']
    airport_map = data['apb']
    flights = data['fis']

    flight_list = []
    for flight in flights:
        type_code = flight['cf']['c']
        item = {'arr_city': arr_city_name,
                'dept_city': dept_city_name,
                'airCom': aircom_map[flight['alc']],
                'flightNo': flight['fn'],
                'flightType': type_map[type_code],
                'arrPort': flight['apbn'],
                'arrTerm': flight['asmsn'],
                'arrTime': flight['at'],
                'depPort': flight['dpbn'],
                'deptTerm': flight['dsmsn'],
                'deptTime': flight['dt'],
                'onTimeRate': json.loads(flight['confort'])['HistoryPunctuality'],
                # 'basicCabinPrice': flight[''],
                'bestDiscount': flight['scs'][0]['rate'],
                'bestEclassPrice': flight['lp'],
                'bestFclassPrice': flight['lcfp'],
                # 'insurePrice': flight['cabin']['insureBasePrice'],
                # 'buildPrice': flight['buildPrice'],
                # 'oilPrice': flight['oilPrice']
                }

        flight_list.append(item)

    return flight_list


def get_craft_type(header):
    type_dict = {}
    url = 'http://webresource.c-ctrip.com/code/js/resource/jmpinfo_tuna/CraftType_gb2312.js?ReleaseNo='
    response = requests.get(url, headers=header).content.decode('gb2312')
    start_pos = response.index('\"')
    type_data = response[start_pos + 1:-3]
    for data in type_data.split('@'):
        if len(data) != 0:
            code = data.split('|')[0]
            craft_type = data.split('|')[1] + '|' + data.split('|')[2]
            type_dict[code] = craft_type

    return type_dict


class FlightSearchClass(object):
    def __init__(self):
        self.url_dict = {'host': 'http://flights.ctrip.com',
                         'path': '/domesticsearch/search/SearchFirstRouteFlights',
                         'args': {'DCity1': '',
                                  'ACity1': '',
                                  'DDate1': ''
                                  }
                         }
        self.header = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'accept-encoding': 'gzip, deflate, sdch',
                       'accept-language': 'en-US,en;q=0.8',
                       'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                       'Upgrade-Insecure-Requests': '1',
                       'cookie': '_abtest_userid=92262f04-2b5d-4667-8a3a-ab2cdf30cc3d; adscityen=Chengdu; Customer=HAL=ctrip_gb; FD_SearchHistorty={"type":"S","data":"S%24%u5317%u4EAC%28BJS%29%24BJS%242016-11-16%24%u4E0A%u6D77%28SHA%29%24SHA%24%24%24"}; _bfa=1.1478434194582.229h46.1.1478434194582.1478434194582.1.4; _ga=GA1.2.1274455234.1478434201; __zpspc=9.1.1478434201.1478434246.3%234%7C%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C1478434201319%7C1.1439032278.1478434201186.1478434216227.1478434246211.1478434216227.1478434246211.undefined.0.0.3.3; MKT_Pagesource=PC; _bfi=p1%3D101027%26p2%3D101027%26v1%3D4%26v2%3D3'
                       }

    def search_flight(self, dept_city_name, dept_city_code, arr_city_name, arr_city_code, dept_date):
        self.url_dict['args']['DCity1'] = dept_city_code
        self.url_dict['args']['ACity1'] = arr_city_code
        self.url_dict['args']['DDate1'] = dept_date.encode('utf-8')
        url = common.compose_url(self.url_dict)
        ret = json.loads(requests.get(url, headers=self.header).content.decode('gb2312'))
        # if 'url' in ret.keys():
        #     return {'success': False, 'msg': 'error: need to login!'}
        type_map = get_craft_type(self.header)
        flight_list = extract_flight_info(ret, dept_city_name, arr_city_name, type_map)
        ret_dict = {'success': True, 'flight_list': flight_list, 'flight_sum': str(len(flight_list))}
        return ret_dict
