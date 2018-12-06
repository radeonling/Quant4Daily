# -*- coding: utf-8 -*-

import pandas as pd

#计算股票每个投资周期收益
class OnePeriodReturnCaculatorC(object):

    conn = None
    baseDate = ""
    buyDate = ""
    sellDate = ""

    def __init__(self, conn, baseDate, buyDate, sellDate):
        self.conn = conn
        self.baseDate = baseDate
        self.buyDate = buyDate
        self.sellDate = sellDate

    def caculateReturns(self):
        c = self.conn.cursor()
        sql = '''
            SELECT 
              /*股票wind代码*/
              T1.S_INFO_WINDCODE,
              /*因子基准日*/
              T1.TRADE_DT AS BASE_DATE,
              /*买入日*/
              T2.TRADE_DT AS BUY_DATE,
              /*买入均价--以买入日复权后均价作为买入均价*/
              T2.S_DQ_AVGPRICE*T2.S_DQ_ADJFACTOR AS BUY_PRICE_ADJ,
              /*卖出日*/
              T3.TRADE_DT AS SELL_DATE,
              /*卖出均价--以卖出日复权后均价作为卖出均价*/
              T3.S_DQ_AVGPRICE*T3.S_DQ_ADJFACTOR AS SELL_PRICE_ADJ,
              /*一个周期（From 买入日 To 卖出日）内的收益率*/
              (T3.S_DQ_AVGPRICE*T3.S_DQ_ADJFACTOR-T2.S_DQ_AVGPRICE*T2.S_DQ_ADJFACTOR)/(T2.S_DQ_AVGPRICE*T2.S_DQ_ADJFACTOR) AS ONE_PERIOD_RTN
            FROM DAILY_TX_DATA T1
            LEFT OUTER JOIN DAILY_TX_DATA T2 ON T1.S_INFO_WINDCODE = T2.S_INFO_WINDCODE
            LEFT OUTER JOIN DAILY_TX_DATA T3 ON T1.S_INFO_WINDCODE = T3.S_INFO_WINDCODE
            WHERE 
              /*因子基准日没停牌*/
              T1.TRADE_DT = '{1}'
            AND
              /*买入日没停牌*/
              T2.TRADE_DT = '{2}'
            AND 
              /*买入日未涨跌停*/
              T3.TRADE_DT = '{3}'
            '''
        sql= sql.replace('{1}', self.baseDate)
        sql= sql.replace('{2}', self.buyDate)
        sql= sql.replace('{3}', self.sellDate)
        cursor = c.execute(sql)

        # 获取每个投资周期收益回报数据
        dataList = list()
        for row in cursor:
            dataList.append(row)

        cursor.close()
        c.close()
        cursor = None
        c = None

        df = pd.DataFrame(dataList, columns=['S_INFO_WINDCODE', 'BASE_DATE', 'BUY_DATE', 'BUY_PRICE_ADJ', 'SELL_DATE', 'SELL_PRICE_ADJ', 'ONE_PERIOD_RTN'])
        return df
