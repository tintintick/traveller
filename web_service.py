# -*- coding:utf-8 -*-
from flask import Flask, request, jsonify
import ctrip_flight
import search

web_service = Flask(__name__)


@web_service.route('/flights/search/')
def search_flights():
    args = request.args.copy()
    # args['type'] = 'flight_search'
    cflight = ctrip_flight.CtripFlightsClass()
    cities = cflight.get_cities()
    # dcity_code = cities
    # acity_code =
    fsearch = search.FlightSearchClass()
    return jsonify(fsearch.search_flight(args['dcity'], args['acity'], args['ddate']))


@web_service.route('/flights/sale/')
def sale_flights():
    # args_dict = jsonify(request.args.copy())
    # # args['type'] = 'flight_sale'
    # dept_city = args_dict['deptCity']
    # dept_date = args_dict['deptDate']
    # arr_city = args_dict['arrCity']
    pass


@web_service.route('/products/sale/')
def sale_products():
    # args = request.args.copy()
    # args['type'] = 'product_sale'
    # return jsonify(args)
    pass


if __name__ == '__main__':
    web_service.run(host='0.0.0.0', debug=True)
