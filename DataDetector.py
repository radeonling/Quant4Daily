# -*- coding: utf-8 -*-

import sqlite3 as sqlt

#数据探测器--用于初步统计可分析数据信息
class DataDetectorC(object):

    multiFactorDBFile = ""

    def __init__(self, multiFactorDBFile):
        self.multiFactorDBFile = multiFactorDBFile

    def setMultiFactorDBFile(self, multiFactorDBFile):

        self.multiFactorDBFile = multiFactorDBFile

    def getMultiFactorDBFile(self):
        return self.multiFactorDBFile

    #获取交易日历清单
    def getTxDateList(self):
        conn = sqlt.connect(self.multiFactorDBFile)

        c = conn.cursor()
        sql = 'SELECT TRADE_DT FROM DAILY_TX_DATA GROUP BY TRADE_DT ORDER BY TRADE_DT;'
        cursor = c.execute(sql)

        # 获取交易日历清单
        txDateList = list()
        for row in cursor:
            txDateList.append(row)
        cursor.close()
        c.close()
        conn.close()

        return txDateList
