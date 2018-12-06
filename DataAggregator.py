# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from Config import *

#数据统计工具--用于分组统计收益信息
class DataAggregatorC(object):

    #附加因子分组信息
    def addGroupInfo(self, df):
        #对数据按照因子排序
        df = df.sort_values(by='OPEN_UP', ascending=False, na_position='last')

        stockCount = df.shape[0]
        groupCount = GROUP_COUNT

        groupStockCount = []
        for i in range(0, groupCount):
            groupStockCount.append(round(stockCount / groupCount * (i + 1), 0))

        for i in range(1, groupCount):
            j = groupCount - i
            groupStockCount[j] = groupStockCount[j] - groupStockCount[j - 1]

        groupCol = []
        for i in range(0, groupCount):
            groupCol = np.append(groupCol, np.linspace(i + 1, i + 1, groupStockCount[i]))

        df['GROUP_ID'] = groupCol

        return df

    # 按照分组计算每组收益信息
    def getGroupAvgRtn(self, df):
        df = self.addGroupInfo(df)
        grouped = df.groupby('GROUP_ID')
        meanReturn = grouped['ONE_PERIOD_RTN'].agg(np.mean)
        meanReturnAll = df.mean()['ONE_PERIOD_RTN']

        dfGrpRtn = pd.DataFrame(meanReturn - meanReturnAll, index=None)
        dfGrpRtn['TRADE_DT'] = df['TRADE_DT'][0]

        return dfGrpRtn

    # 计算叠加收益
    def getGroupAvgRtnSum(self, dfPreSum, dfAdd):
        dfAdd['ONE_PERIOD_RTN'] = dfPreSum['ONE_PERIOD_RTN'] + dfAdd['ONE_PERIOD_RTN']
        return dfAdd
