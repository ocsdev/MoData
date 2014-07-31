# -*- coding: UTF-8 -*-
import glob
import json
import socket
import requests
from modata.utils import all_stocks
from modata.utils import constants
import pandas as pd

PATH = '%s/data/'%constants.data_path()

'''
获取所有每日交易数据
'''
def from_ifeng(day=None):
    data = all_stocks.get_stocks()
    df = data[['name']]
    for code in df.index:
        symbol = code_str(code)
        try:
            get_data(constants.DAY_PRICE_URL%symbol,code,day=day)
            write_added(code) #记录成功执行的股票
#            time.sleep(3)
        except socket.timeout as er:
            print "Timed out。 %s" % er
        except Exception as e:
            print e,'error occured when getting data of %s '% code[:-3] 

'''
解析每日交易的json数据，根据日期过滤
保存DataFrame数据为csv格式
'''
def get_data(url,code=None,day=None):
    resp = requests.get(url)
    text = resp.text
    js = json.loads(text)
    df = pd.DataFrame(js['record'],columns=constants.DAY_PRICE_COLUMNS)
    df = df.applymap(lambda x: x.replace(u',', u'')) #删除千位分隔符,
    df = df.drop('price_change',axis=1)
    df = df.set_index(['date'])
    
    if day is None:
        df.to_csv('%s/day_price/%s.csv'%(PATH,code)) #生产新的文件
    else:
        df = df.ix[df.index>=day]
        df.to_csv('%s/day_price/%s.csv'%(PATH,code),mode='a',header=False) #追加行
 
'''
将所有股票数据合成一个大文件，csv格式
'''   
def to_a_big_file():
    files = glob.glob('%sday_price/*.csv'%PATH)
    for file in files:
        print file[-10:-4]
        df = pd.read_csv(file,names=constants.DAY_PRICE_COLUMNS)
        df['code'] = file[-10:-4]
        df = df.set_index(['code','date'])
        df.to_csv('%sall_stocks_price.csv'%PATH,header=False,mode='a')

'''
将所有股票数据合成一个大文件，HDF5格式
'''  
def to_a_big_file_hdf():
    files = glob.glob('%sday_price/*.csv'%PATH)
    i = 0
    data = pd.DataFrame()
    df = pd.read_csv(files[0])
    for file in files[1:]:
        df = pd.read_csv(file)
        df['code'] = file[-10:-4]
        if i==0:
            data = df
        else:
            data = data.append(df)
        i += 1
    data.to_hdf('%sall_stocks_price.h5'%PATH, 'price',format='t',complevel=9, complib='bzip2',append=True)    

'''
生成symbol代码标志
'''
def code_str(code):
    code = 'sh'+code if code[:1]=='6' else 'sz'+code
    return code

'''
写人成功日志
'''
def write_added(text):
    f = open('%sadded.txt'%PATH,'a')
    f.write(text+'\n')
    f.close()

if __name__ == '__main__':
    to_a_big_file()