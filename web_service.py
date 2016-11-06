#!traveller/bin/python
from flask import Flask, request, jsonify

web_service = Flask(__name__)


@web_service.route('/flights/search/')
def search_flights():
    args = request.args.copy()
    # args['type'] = 'flight_search'
    return jsonify(args)


@web_service.route('/flights/sale/')
def sale_flights():
    args_dict = jsonify(request.args.copy())
    # args['type'] = 'flight_sale'
    dept_city = args_dict['deptCity']
    dept_date = args_dict['deptDate']
    arr_city = args_dict['arrCity']


@web_service.route('/products/sale/')
def sale_products():
    args = request.args.copy()
    args['type'] = 'product_sale'
    return jsonify(args)


if __name__ == '__main__':
    web_service.run(debug=True)
