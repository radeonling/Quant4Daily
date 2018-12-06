# -*- coding: utf-8 -*-

import pandas as pd
from Config import *

#计算股票每日因子--单日
class DailyFactorCaculatorC(object):

    conn = None
    baseDate = ""
    buyDate = ""
    sellDate = ""

    def __init__(self, conn, baseDate, buyDate, sellDate):
        self.conn = conn
        self.baseDate = baseDate
        self.buyDate = buyDate
        self.sellDate = sellDate

    def setGroupCount(self, groupCount):
        self.groupCount = groupCount

    def getGroupCount(self):
        return self.groupCount

    def caculateFactors(self):
        c = self.conn.cursor()
        sql = '''
            SELECT 
                T1.TRADE_DT, 
                T1.S_INFO_WINDCODE,
                (T1.S_DQ_OPEN-T1.S_DQ_PRECLOSE)/T1.S_DQ_PRECLOSE AS OPEN_UP
            FROM DAILY_TX_DATA T1 
            LEFT OUTER JOIN DAILY_TX_DATA T2
            ON T1.S_INFO_WINDCODE = T2.S_INFO_WINDCODE
            WHERE T1.TRADE_DT = {1}
            AND T2.TRADE_DT = {2}
            AND T1.S_DQ_TRADESTATUS != '停牌'
            AND T2.S_DQ_TRADESTATUS != '停牌'
            AND (T2.S_DQ_HIGH-T2.S_DQ_AVGPRICE)*(T2.S_DQ_LOW-T2.S_DQ_AVGPRICE) != 0;
            '''
        sql = sql.replace('{1}', self.baseDate)
        sql = sql.replace('{2}', self.buyDate)
        # sql = sql.replace('{3}', self.sellDate)
        cursor = c.execute(sql)

        # 获取每日因子
        dataList = list()
        for row in cursor:
            dataList.append(row)

        cursor.close()
        c.close()
        cursor = None
        c = None

        df = pd.DataFrame(dataList, columns=['TRADE_DT', 'S_INFO_WINDCODE', 'OPEN_UP'])
        return df
