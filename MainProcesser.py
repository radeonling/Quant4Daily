# -*- coding: utf-8 -*-

import pandas as pd
import sqlite3 as sqlt
import datetime as dt
from DailyFactorCaculator import DailyFactorCaculatorC
from DataDetector import DataDetectorC
from OnePeriodReturnCaculator import OnePeriodReturnCaculatorC
from DataAggregator import DataAggregatorC
from Config import *

# 主程序
# 循环每个交易日，计算股票因子、收益，并按照因子对收益进行分组统计。
class MainProcesserC(object):

    # 股票日行情元数据（数据存放于SQLite DB文件，变量用于保存文件路径。）
    multiFactorDBFile = ""

    # 类初始化
    def __init__(self, multiFactorDBFile):
        self.multiFactorDBFile = multiFactorDBFile

    # 设定SQLite DB文件路径
    def setMultiFactorDBFile(self, multiFactorDBFile):
        self.multiFactorDBFile = multiFactorDBFile

    # 读取SQLite DB文件路径
    def getMultiFactorDBFile(self):
        return self.multiFactorDBFile

    # 循环每个交易日，计算因子与收益，并完成分组收益统计
    def dailyLoopProcess(self):

        # 探测数据，读取交易日列表
        ddc = DataDetectorC(self.multiFactorDBFile)
        txDateList = ddc.getTxDateList()

        # 获得DB访问连接，进入主处理。
        conn = sqlt.connect(self.multiFactorDBFile)
        dfCul = pd.DataFrame({})
        loopCount = len(txDateList) - 1 - HOLDING_DAYS
        rateOfPrgss = 0
        for i in range(0, loopCount):

            # 计算每日因子
            dfcc = DailyFactorCaculatorC(conn, baseDate=txDateList[i][0], buyDate=txDateList[i + 1][0], sellDate=txDateList[i + 1 + HOLDING_DAYS][0])
            dfFcts = dfcc.caculateFactors()
            if TEMP_FILE_OUTPUT:
                dfFcts.to_csv(TempFileDir + str(txDateList[i][0]) + "-StockFactors.csv", index=True)

            # 计算每日收益
            oprcc = OnePeriodReturnCaculatorC(conn, baseDate=txDateList[i][0], buyDate=txDateList[i + 1][0], sellDate=txDateList[i + 1 + HOLDING_DAYS][0])
            dfRtns = oprcc.caculateReturns()
            if TEMP_FILE_OUTPUT:
                dfRtns.to_csv(TempFileDir + str(txDateList[i][0]) + "-StockReturns.csv", index=True)

            # 将因子与收益信息做合并处理
            dfFctsAndRtns = pd.merge(dfFcts, dfRtns, on='S_INFO_WINDCODE', how='left')
            if TEMP_FILE_OUTPUT:
                dfFctsAndRtns.to_csv(TempFileDir + str(txDateList[i][0]) + "-StockFactorAndReturns.csv", index=True)

            # 对分组收益进行统计
            dac = DataAggregatorC()
            dfSttcs = dac.getGroupAvgRtn(dfFctsAndRtns)
            if TEMP_FILE_OUTPUT:
                dfSttcs.to_csv(TempFileDir + str(txDateList[i][0]) + "-GroupReturnsRelative.csv", index=True)

            # 记录运行结果
            if i==0:
                # 叠加收益
                dfSum = dfSttcs.copy(deep=True)
            else:
                dfSum = dac.getGroupAvgRtnSum(dfSum, dfSttcs)

            # 保存每日收益信息
            dfCul = dfCul.append(dfSum)
            if TEMP_FILE_OUTPUT:
                dfSum.to_csv(TempFileDir + str(txDateList[i][0]) + "-GroupReturnsRelativeSum.csv", index=True)

            if rateOfPrgss < round(i/loopCount*100):
                rateOfPrgss = round(i/loopCount*100)
                if MESSAGE_ON:
                    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"  "+"已处理"+str(rateOfPrgss) + "%...")

        # 保存每日累计收益数据
        resultFile = WorkDir + "每日因子分组累计收益统计.csv"
        dfCul.to_csv(resultFile, index=True)
        if MESSAGE_ON:
            print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + "分析结果已保存至文件：" + resultFile)

        # 关闭DB连接
        conn.close()

def main():
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + "处理开始：" )

    mpc = MainProcesserC(MultiFactorDB)
    mpc.dailyLoopProcess()

    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + "处理结束！" )

if __name__ == '__main__':
    main()