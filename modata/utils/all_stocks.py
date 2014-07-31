# -*- coding: UTF-8 -*-

import pandas as pd
'''
按条件获取股票基本信息,默认为全部
返回DataFrame
'''
def get_stocks(priceLt=None, priceGt=None, 
                        outLt=None,outGt=None, 
                        peLt=None, peGt=None,
                        gjjLt=None, gjjGt=None,
                        epsLt=None,epsGt=None, 
                        industry=None,notST=False):
    '''
    priceLt:当前价小于等于
    priceGt:当前价大于等于
            其他Lt Gt类同
            属性代码表：
            代码    名称    现价    市盈(动) 流通股本    细分行业    地区org 每股收益eps 每股公积gjj  人均持股rjcg   股东人数gdrs 每股净资mgjzc    市净率sjl    利润同比lrtb    每股未分配 mgwfp   收入同比srtb    上市日期    昨收
    Index(['code', 'name', 'price', 'pe', 'out', 'industry', 'org', 'eps', 'gjj', 'rjcg', 'gdrs', 'mgjzc', 'sjl', 'lrtb', 'mgwfp', 'srtb', 'date','yes'], dtype='object')
    '''
    
    path = '%s/data/20140722_all.csv' % script_path()
    df = pd.read_csv(path, dtype={'code':object, 'eps':float}, encoding='GBK')
    df = df.set_index(['code'])
    df['pe'] = df['pe' == '--'] = '0'
    df['pe'] = df['pe'].astype(float)
    df['price'][df.price == 0] = df['yes']  # 如果当日收盘价是0，则等于昨日收盘（当日停牌）
    df = df.dropna(how='all')
    
    if priceLt is not None:
        df = df.ix[df.price<=priceLt]
    if priceGt is not None:
        df = df.ix[df.price>=priceGt]
    if outLt is not None:
        df = df.ix[df.out<=outLt]
    if outGt is not None:
        df = df.ix[df.out>=outGt]
    if peLt is not None:
        df = df.ix[df.pe<=peLt]
    if peGt is not None:
        df = df.ix[df.pe>=peGt]
    if gjjLt is not None:
        df = df.ix[df.gjj<=gjjLt]
    if gjjGt is not None:
        df = df.ix[df.gjj>=gjjGt]
    if epsLt is not None:
        df = df.ix[df.eps<=epsLt]
    if epsGt is not None:
        df = df.ix[df.eps>=epsGt]  
    if industry is not None:
        df = df.ix[df.industry==industry]
    if notST is True:
        df = df.ix[df.name.str.contains('ST') == False]

    return df

'''
获取csv数据的路径
'''
def script_path():
    import inspect, os
    caller_file = inspect.stack()[1][1]  # caller's filename
    pardir = os.path.abspath(os.path.join(os.path.dirname(caller_file), os.path.pardir))
    return os.path.abspath(os.path.join(pardir, os.path.pardir))

        
if __name__ == '__main__':
    df = get_stocks()
    print df

