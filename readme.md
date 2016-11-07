
1、航班搜索

GET请求
http://112.74.219.150:5000/flights/search/?dcity=%E6%88%90%E9%83%BD&acity=%E5%8C%97%E4%BA%AC&ddate=2016-12-03

参数
dcity 出发城市
acity 到达城市
ddate 出发日期

结果
{
	# 城市名称及在ctrip的对应code(Unicode编码)
	cities: {"\u4e07\u5dde": "WXN", 
		     "\u4e09\u4e9a": "SYX", 
		     "\u4e09\u660e": "SQJ", 
		     "\u4e0a\u6d77": "SHA"
			} 

	# 从当前日期开始，近三个月的低价日历
	low_price_calendar: {"2016-11-07":"490",
	                     "2016-11-08":"452",
						 ...
						 "2017-02-04":"250"} 

	# 所有航班信息(Unicode编码)
	flight_list: {"airCom": "\u4e2d\u56fd\u56fd\u822a", 航空公司
			      "arrPort": "\u9996\u90fd\u56fd\u9645\u673a\u573aT3", 到达机场
			      "arrTerm": "T3", 到达航站楼
			      "arrTime": "2016-12-03 09:40:00", 到达时间
			      "arr_city": "\u5317\u4eac", 到达城市
			      "bestDiscount": 0.44, 折扣
			      "bestEclassPrice": 750, 最低经济舱价格
			      "bestFclassPrice": 1660, 最低头等舱价格
			      "depPort": "\u53cc\u6d41\u56fd\u9645\u673a\u573aT2", 出发机场
			      "deptTerm": "T2", 出发航站楼
			      "deptTime": "2016-12-03 06:55:00", 出发时间
			      "dept_city": "\u6210\u90fd", 出发城市
			      "flightNo": "CA4193", 航班号
			      "flightType": "\u7a7a\u5ba2330|\u5bbd\u4f53", 机型
			      "onTimeRate": "93.27%" 准点率
                  } 
	# 航班总数
	flight_sum: (str) 

	# 查询是否成功
	success: (bool) 
}
