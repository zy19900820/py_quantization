#coding:utf-8
from fmex import Fmex
from time import strftime, localtime
import time
import json
from pymongo import MongoClient
import thread

def getHighR1(fourHourList, listIndex):
    high = 0
    for i in range (listIndex - 12, listIndex):
        if (fourHourList[i]["high"] > high):
            high = fourHourList[i]["high"]
    return high

def getLowR1(fourHourList, listIndex):
    low = 99999999
    for i in range (listIndex - 12, listIndex):
        if (fourHourList[i]["low"] < low):
            low = fourHourList[i]["low"]
    return low

def getHighR2(fourHourList, listIndex):
    high = 0
    for i in range (listIndex - 18, listIndex):
        if (fourHourList[i]["high"] > high):
            high = fourHourList[i]["high"]
    return high

def getLowR2(fourHourList, listIndex):
    low = 99999999
    for i in range (listIndex - 18, listIndex):
        if (fourHourList[i]["low"] < low):
            low = fourHourList[i]["low"]
    return low

fourHourList = []
conn = MongoClient('127.0.0.1', 27017)

fmex = Fmex()
db = conn["fmexCandleData"]
col = db["btcusd_p_H4"]
for val in col.find().sort("id", 1):
    fourHourList.append(val)

#long_limit = open - R1 * 0.12
#profit_target = R1 * 0.32


for slope in range(5, 30, 1):
    slope = slope / 100
    print "slope start:" + str(slope)
    for profitSlope in range(10, 50, 1):
        profitSlope = profitSlope / 100
        print "profitSlope start:" + str(profitSlope)
        for stopless in range(100, 2000, 10):
            print "stopless start:" + str(stopless)
            totalBTC = 1
            listIndex = 18
            alreadyBuy = False
            buyNum = 0
            longLimit = 0
            sellPrice = 0

            while (listIndex < len(fourHourList)):
                #未挂买单
                if (alreadyBuy == False):
                    #获取R1高点低点
                    highR1 = getHighR1(fourHourList, listIndex)
                    lowR1 = getLowR1(fourHourList, listIndex)
                    R1 = highR1 - lowR1
                    #本次4小时 开盘挂单
                    longLimit = fourHourList[listIndex]["open"] - slope * R1
                    #4小时线最低点没打到 到下一个4小时
                    if (fourHourList[listIndex]["low"] > longLimit):
                        listIndex = listIndex + 1
                        continue
        
                    alreadyBuy = True
                    sellPrice = longLimit + R1 * profitSlope
                    print "buy time btc:" + str(totalBTC)
                    print "buy price:" + str(longLimit)
                    buyNum = totalBTC / longLimit
                    #到这里表示挂买单成交 如果4小时低点打到止损,则这次4小时交易亏损
                    if (longLimit - stopless > fourHourList[listIndex]["low"]):
                        alreadyBuy = False
                        totalBTC = buyNum * (longLimit - stopless)
                        print "buy time btc:" + str(totalBTC)
                        print "sell price:" + str(longLimit - stopless)

                    #到这里表示止损没打到 到下一个4小时
                    listIndex = listIndex + 1
                    continue
                else:
                    #FIXME 假设先到低点 再判断止盈 
                    #止损打到了
                    if (longLimit - stopless > fourHourList[listIndex]["low"]):
                        alreadyBuy = False
                        totalBTC = buyNum * (longLimit - stopless)
                        listIndex = listIndex + 1
                        print "buy time btc:" + str(totalBTC)
                        print "sell price:" + str(longLimit - stopless)
                        continue
                    #止盈没打到
                    if (sellPrice > fourHourList[listIndex]["high"]):
                        listIndex = listIndex + 1
                        continue
                    else:
                        alreadyBuy = False
                        totalBTC = buyNum * sellPrice
                        listIndex = listIndex + 1
                        print "buy time btc:" + str(totalBTC)
                        print "sell price:" + str(longLimit - stopless)

            print "one finish, btc count:" + str(totalBTC)
