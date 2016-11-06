# -*- coding:utf-8 -*-
import requests
import json
import common
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def extract_flight_info(data):
    aircom_map = data['aircodeNameMap']
    airport_map = data['airportMap']
    type_map = data['flightTypeMap']
    flights = data['flight']

    flight_list = []
    for flight in flights:
        item = {'arr_city': data['arrCityName'],
                'dept_city': data['depCityName'],
                'airCom': aircom_map[flight['airlineCode']],
                'flightNo': flight['flightNo'],
                'flightType': [key for key, value in type_map.items() if flight['flightType'] in value][0],
                'arrPort': airport_map[flight['arrAirport']],
                'arrTerm': flight['arrTerm'],
                'arrTime': flight['arrTime'],
                'depPort': airport_map[flight['depAirport']],
                'deptTerm': flight['depTerm'],
                'deptTime': flight['depTime'],
                'onTimeRate': '',
                'basicCabinPrice': flight['cabin']['basicCabinPrice'],
                'bestDiscount': flight['cabin']['bestDiscount'],
                'bestPrice': flight['cabin']['bestPrice'],
                'insurePrice': flight['cabin']['insureBasePrice'],
                'buildPrice': flight['buildPrice'],
                'oilPrice': flight['oilPrice']
                }
        try:
            item['onTimeRate'] = flight['onTimeRate']
        except:
            item['onTimeRate'] = ''

        # show
        flight_list.append(item)

    return flight_list


class FlightSearchClass(object):
    def __init__(self):
        self.url_dict = {'host': 'http://flights.ctrip.com/',
                         'path': '/domesticsearch/search/SearchFirstRouteFlights',
                         'args': {'callback': 'ajson',
                                  'depCityName': '',
                                  'arrCityName': '',
                                  'depDate': '',
                                  '_input_charset': 'utf-8'
                                  # 'tripType': '0',
                                  # 'depCity': depCity,
                                  # 'arrCity': arrCity,
                                  # 'searchSource': '99',
                                  # 'searchBy': '1280',
                                  # 'needMemberPrice': 'true',
                                  }
                         }
        self.header = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'accept-encoding': 'gzip, deflate, sdch, br',
                       'accept-language': 'en-US,en;q=0.8',
                       'cache-control': 'max-age=0',
                       'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                       'upgrade - insecure - requests': '1',
                       'cookie': 'cna=fI+YEH7Dw10CAW64BNuRKi6Q; cookie2=1c77fdca0ddc3c4acde5014f4de58f97; t=b19a8c4d17f59c005cb99905735de97e; _tb_token_=A2MesRfzlWjK; CNZZDATA30066717=cnzz_eid%3D258578843-1477547258-https%253A%252F%252Fwww.alitrip.com%252F%26ntime%3D1477547258; l=AvX1qnEuxWcpwN/LogT5jY9hhXuvi6mM; isg=Ap2dqAyhmS3vAX0Bbv6faRfIrHCArtEMeS1wLl9iIvQrFr1IJwrh3GuEJr3q'
                       }

    def search_flight(self, dept_city_name, arr_city_name, dept_date):
        self.url_dict['args']['depCityName'] = dept_city_name.encode('utf-8')
        self.url_dict['args']['arrCityName'] = arr_city_name.encode('utf-8')
        self.url_dict['args']['depDate'] = dept_date.encode('utf-8')
        url = common.compose_url(self.url_dict)
        ret = requests.get(url, headers=self.header).content.decode('gbk').encode('utf-8')
        start_pos = ret.index('{')
        ajson = json.loads(ret[start_pos:-3])
        if 'url' in ajson.keys():
            return {'success': False, 'msg': 'error: need to login!'}

        flight_list = extract_flight_info(ajson['data'])
        ret_dict = {'success': True, 'flight_list': flight_list, 'flight_sum': str(len(ajson['data']['flight']))}
        return ret_dict
