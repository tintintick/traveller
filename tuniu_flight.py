# -*- coding:utf-8 -*-
import requests
import json
import base64


def request_content(url, header):
    tjson = json.loads(requests.get(url, headers=header).content)
    return tjson['data']


def get_cities():
    url = 'http://www.tuniu.com/flight/international/getCities'
    return request_content(url)


class TuniuFlightsClass(object):
    def __init__(self):
        self.header = {"Connection": 'keep-alive',
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                       'Accept': '*/*',
                       'Referer': 'http://www.tuniu.com/flight/',
                       'Accept-Encoding': 'gzip, deflate, sdch, br',
                       'Cookie': 'tuniu_partner=MTAwLDAsLDI2OWJhMjJhNDAxOWQyNDRjYzNkMGU4ODZkMjQ1NGFk; p_phone_400=4007-999-999; OLBSESSID=797c7t0vrebf8dpgtr2cjg6197; _tacau=MCw1YmY4M2ZlYi1lY2QyLTQ3MGItZWE5NC00MjA1ZjM1MDhkN2Us; _tacz2=taccsr%3D%28direct%29%7Ctacccn%3D%28none%29%7Ctaccmd%3D%28none%29%7Ctaccct%3D%28none%29%7Ctaccrt%3D%28none%29; _taca=1477533277619.1477533277619.1477533277619.1; _tacc=1; PageSwitch=1%2C213612736; __xsptplusUT_352=1; MOBILE_APP_SETTING_OPEN-124=1; MOBILE_APP_SETTING_STATE-124=CLOSE; _pzfxuvpc=1477533277671%7C8609357373767715853%7C3%7C1477533290475%7C1%7C%7C1174412762213237200; _pzfxsvpc=1174412762213237200%7C1477533277671%7C3%7C; _tact=N2NlMWE2OTctZjdjYi02NWZkLWRlN2YtNDNmZjI2OGYwZGM3; _tacb=MjU0ZWM0ZGQtNDkzZC0zOTA3LTIyMDItNjNhNGU5ZmQwNTli; __xsptplus352=352.1.1477533281.1477533292.4%234%7C%7C%7C%7C%7C%23%23gRi5UZx0kl22-Dh4Cqk_Ka4_dD7yPq7E%23; Hm_lvt_51d49a7cda10d5dd86537755f081cc02=1477533278; Hm_lpvt_51d49a7cda10d5dd86537755f081cc02=1477533292; __utma=1.1986001297.1477533278.1477533278.1477533278.1; __utmb=1.4.9.1477533278; __utmc=1; __utmz=1.1477533278.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tuniuuser_citycode='
                       }

    def get_flights(self):
        url = 'http://flight-api.tuniu.com/query/queryCheapTickets'
        cities = get_cities()

        for city in cities:
            header = self.header['Cookie'].copy
            header += base64.encodestring(str(city['cityCode'])).strip('\n')
            tjson = request_content(url, header)

            if int(tjson['beginCityCode']) == city['cityCode']:
                flight_info = tjson['cityFlightInfo']
                aircom_flight_info = tjson['airComFlightInfo']  # CA CZ HU MU
                for key in aircom_flight_info.keys():
                    aircom_round_trips = aircom_flight_info[key]['roundTrip']
                    for aircom_round_trip in aircom_round_trips:
                        # store into db
                        print aircom_round_trip
                    aircom_single_trips = aircom_flight_info[key]['singleTrip']
                    for aircom_single_trip in aircom_single_trips:
                        # store into db
                        print aircom_single_trip

                for round_flight in flight_info['roundTrip']:
                    # store into db
                    print round_flight

                for single_flight in flight_info['singleTrip']:
                    # store into db
                    print single_flight