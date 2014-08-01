# -*- coding: utf-8 -*-
'''
Created on 2012/08/11
@author: Jimmy Liu
QQ:52799046
'''
import pandas as pd
import datetime
from modata.utils import constants
import os

def get_stcks(day_from='2014-01-01'):
    starttime = datetime.datetime.now()
    df = pd.read_csv('%sall_stocks_price.csv'%constants.PATH,dtype={'code':object})
    endtime = datetime.datetime.now()
    print 'read the data file used:%s seconds.'%(endtime - starttime).seconds
    df = df[df.date>=day_from]
    grouped = df.groupby(['code','date'])
    #遍历有交易历史的股票代码和日期，用户获取其tick数据
    for name,data in grouped:
        code = 'sh'+name[0] if name[0][:1]=='6' else 'sz'+name[0]
        get_data(constants.TICK_PRICE_URL%(name[1],code),name[0],name[1])
        write_added('%s,%s'%(name[0],name[1])) #记录成功执行的股票
'''
获取股票的tick数据，统计交易信息
cash默认设定每笔30万为大单
'''
def get_data(url,code=None,day=None,cash=300000):
    #通过read_table读取tick详细记录，自动过滤掉head并设置names作为新的head
    df = pd.read_table(url,names=constants.TICK_COLUMNS,skiprows=[0]) 
    
    df = df.ix[df.cash>0]
    df['type'] = df['change']
    df['change'][df.change=='--'] = '0'
    df['change'] = df['change'].astype(float)
    df['type'][df.change<0] = 'S' #与上一笔价格相比小于0的为卖单
    df['type'][df.change>0] = 'B' #与上一笔价格相比大于0的为买单
    df['type'][df.type=='--'] = None
    df = df.fillna(method='bfill') #类型同上一笔交易
    df['change'][df.time.str.contains('09:25:')] = 0 #把集合竞价的价格变动设为0
    df['type'][df.time.str.contains('09:25:')] = 'N' #把集合竞价的类型设为中性
    data =[[day,df['time'].count(),
           df['type'][df.type=='B'].count(),
           df['type'][df.type=='S'].count(),
           df['type'][(df.type=='B') & (df.cash>=cash)].count(),
           df['type'][(df.type=='S') & (df.cash>=cash)].count(),
           round(df['cash'].var()/df['cash'].sum(),2)]]
    df = pd.DataFrame(data,columns=constants.TICK_STAT_COLUMNS)
    df = df.set_index('date')
    if day is None or os.path.exists('%s\\tick_price\\%s.csv'%(constants.PATH,code)) is False:
        df.to_csv('%s\\tick_price\\%s.csv'%(constants.PATH,code))
    else:
        df = df.ix[df.index>=day]
        df.to_csv('%s\\tick_price\\%s.csv'%(constants.PATH,code),mode='a',header=False)
    print '%s at %s done.'% (code,day)
        
'''
写人成功日志
'''
def write_added(text):
    f = open('%stick_done.txt'%constants.PATH,'a')
    f.write(text+'\n')
    f.close()
    
if __name__ == '__main__':
    get_stcks()
    
    