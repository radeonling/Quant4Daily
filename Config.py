# -*- coding: utf-8 -*-

#数据库文件
MultiFactorDB = "D:/homework/股票日行情/MultiFactor.db"

#临时目录根目录，结果报告将输出到该目录下
WorkDir = "D:/homework/工作目录/"

#临时目录子目录， 用于放置每日的因子计算结果
TempFileDir = "D:/homework/工作目录/临时文件/"

#分组组数
GROUP_COUNT=10

#H值—持仓交易日数
HOLDING_DAYS=1

#运行过程是否输出临时文件
#True：输出/False：不输出
#提示；不输出每日因子、收益等临时文件可大幅提升程序运行速度。
TEMP_FILE_OUTPUT=True

#运行过程中是否输出执行进度的提示日志
#True：输出/False：不输出
MESSAGE_ON=True
