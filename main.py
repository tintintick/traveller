# -*- coding:utf-8 -*-
import qunar_flight
import qunar_product
import ctrip_flight
import ctrip_product
import tuniu_flight
import tuniu_product
import ali_product
import flights_search
import time
import search

# product_url = "https://zt.dujia.qunar.com/tejia/tejia_get_list.php?callback=qjson&displaynum=50&page"
# qproduct = qunar_product.QunarProductClass(product_url)
# qproduct.get_products()

# 11-04
# cproduct = ctrip_product.CtripSaleProductsClass()
# cproduct.get_products()

# cflight = ctrip_flight.CtripFlightsClass()
# cflight.get_flights()

# tflight = tuniu_flight.TuniuFlightsClass()
# tflight.get_flights()

# tproduct = tuniu_product.TuniuProductsClass()
# dept_city_name = '成都'
# tproduct.get_products(dept_city_name)

# aproduct = ali_product.AliProductsClass()
# aproduct.get_products()

fsearch = search.FlightSearchClass()
fsearch.search_flight('上海', '北京', '2017-10-01')
