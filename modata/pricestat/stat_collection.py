# -*- coding:utf-8 -*- 
'''
Created on 2014/06/11
@author: Jimmy Liu
QQ:52799046
'''
import pandas as pd
from modata.utils import constants

'''
统计阶段涨跌幅
startDate:开始日期
endDate:结束日期
sortAsc:升序排序，默认为False
rowNum:显示条数，默认10条
'''
def span_stat(startDate=None,endDate=None,
                    sortAsc=False,rowNum=10):
    df = pd.read_csv('%sall_stocks_price.csv'%constants.PATH,dtype={'code':object})
    if startDate is not None:
        df = df.ix[df.date>=startDate]
    if endDate is not None:
        df = df.ix[df.date<=endDate]
    p_sum = df.groupby(['code'])['p_change','turnover'].sum()
    p_sum = p_sum.sort('p_change',ascending=sortAsc)
    print p_sum['p_change'].head(rowNum)


if __name__ == '__main__':
    span_stat('2014-07-01',sortAsc=True,rowNum=20)