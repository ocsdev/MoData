# -*- coding:utf-8 -*- 
'''
Created on 2012/07/31
@author: Jimmy Liu
'''


#获取数据所在的路
def data_path():
    import inspect, os
    caller_file = inspect.stack()[1][1]  # caller's filename
    pardir = os.path.abspath(os.path.join(os.path.dirname(caller_file), os.path.pardir))
    return os.path.abspath(os.path.join(pardir, os.path.pardir))

PATH = '%s/data/'%data_path()
DAY_PRICE_URL = 'http://api.finance.ifeng.com/index.php/akdaily/?code=%s&type=last'
TICK_PRICE_URL = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s'
DAY_PRICE_COLUMNS = ['date','open','high','close','low','vol','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20','turnover']
TICK_COLUMNS = ['time','price','change','vol','cash','type']
TICK_STAT_COLUMNS = ['date','count','b_count','s_count','bb_count','bs_count','var_num']