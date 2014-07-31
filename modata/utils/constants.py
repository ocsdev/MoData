# -*- coding:utf-8 -*- 
'''
Created on 2012/07/31
@author: Jimmy Liu
'''

'''
获取数据所在的路径
'''
def data_path():
    import inspect, os
    caller_file = inspect.stack()[1][1]  # caller's filename
    pardir = os.path.abspath(os.path.join(os.path.dirname(caller_file), os.path.pardir))
    return os.path.abspath(os.path.join(pardir, os.path.pardir))


DAY_PRICE_URL = 'http://api.finance.ifeng.com/index.php/akdaily/?code=%s&type=last'
DAY_PRICE_COLUMNS = ['date','open','high','close','low','vol','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20','turnover']