#coding:utf-8
from commonlib import getDirection
from commonlib import getBeforeClose
import commonlib
import time
from pymongo import MongoClient
from fmex import Fmex
import strategyParse
from trade import Trade
import sys
import conf
import draw

def loadMongoData():
    print("loadMongoData start...")

    global gOneMinListData
    conn = MongoClient('127.0.0.1', 27017)
    db = conn["fmexCandleData"]
    col = db["btcusd_p_M1"]
    for val in col.find().sort("id", 1):
        gOneMinListData.append(val)

    print("loadMongoData end...")

def position1000():
    return 1

def eventJudge(eventType, listIndex):
    global gOneMinListData
    global gNowTrade
    global gRunRealTime

    nowTimeStamp = 0
    if (gRunRealTime == False):
        nowTimeStamp = gOneMinListData[listIndex]["id"]
    else:
        nowTimeStamp = int(time.time())

    position = gNowTrade.position_
    openPositionTimeStamp = gNowTrade.entryTimeStamp_

    eventJudgeStr = eventType["formula"]
    evalStr = commonlib.replaceJudgeStr(eventJudgeStr)
    if (evalStr == ""):
        print("replaceJudgeStr Error, ori string:%s" % eventJudgeStr)
        return False
    return eval(evalStr)

def doShort(listIndex, eventType):
    global gTrades
    global gOneMinListData
    global gNowTrade
    global gRunRealTime
    global gfmex

    if (gRunRealTime == False):
        gNowTrade.entryPrice_ = eval(commonlib.replaceJudgeStr(eventType["price"]))
        gNowTrade.entryTimeStamp_ = gOneMinListData[listIndex]["id"]
        count = eval(commonlib.replaceJudgeStr(eventType["count"]))
        gNowTrade.position_ = gNowTrade.position_ - count
        gNowTrade.direction_ = "short"

        trade = Trade(gNowTrade)

        gTrades.append(trade)    
    else:
        entryPrice = eval(commonlib.replaceJudgeStr(eventType["price"]))
        count = eval(commonlib.replaceJudgeStr(eventType["count"]))
        #5次尝试在那个位置挂单 没挂上去则取消
        for i in range(0, 5):
            orderInfo = gfmex.sell_post_only_limit_short("btcusd_p", entryPrice, count)
            orderStatus = orderInfo["data"]["status"]
            if (orderStatus == "fully_cancelled"):
                time.sleep(1)
                continue
            elif (orderStatus == "pending"):
                gNowTrade.uuid_ = orderInfo["data"]["id"]
                gNowTrade.entryPrice_ = entryPrice
                gNowTrade.entryTimeStamp_ = int(time.time())
                gNowTrade.position_ = count
                gNowTrade.direction_ = "short"
                trade = Trade(gNowTrade)
                gTrades.append(trade)
                print("do short, price:%lf, count:%d time:%d" % (entryPrice, count, trade.entryTimeStamp_,))
                break

def doLong(listIndex, eventType):
    global gTrades
    global gOneMinListData
    global gNowTrade
    global gRunRealTime
    global gfmex

    if (gRunRealTime == False):
        gNowTrade.entryTimeStamp_ = gOneMinListData[listIndex]["id"]
        gNowTrade.entryPrice_ = eval(commonlib.replaceJudgeStr(eventType["price"]))
        gNowTrade.position_ = gNowTrade.position_ + eval(commonlib.replaceJudgeStr(eventType["count"]))
        gNowTrade.direction_ = "long"
    
        trade = Trade(gNowTrade)

        gTrades.append(trade)    
    else:
        entryPrice = eval(commonlib.replaceJudgeStr(eventType["price"]))
        count = eval(commonlib.replaceJudgeStr(eventType["count"]))
        #5次尝试在那个位置挂单 没挂上去则取消
        for i in range(0, 5):
            orderInfo = gfmex.buy_post_only_limit_long("btcusd_p", entryPrice, count)
            orderStatus = orderInfo["data"]["status"]
            if (orderStatus == "fully_cancelled"):
                time.sleep(1)
                continue
            elif (orderStatus == "pending"):
                gNowTrade.uuid_ = orderInfo["data"]["id"]
                gNowTrade.entryPrice_ = entryPrice
                gNowTrade.entryTimeStamp_ = int(time.time())
                gNowTrade.position_ = count
                gNowTrade.direction_ = "long"
                trade = Trade(gNowTrade)
                gTrades.append(trade)
                print("do long, price:%lf, count:%d time:%d" % (entryPrice, count, trade.entryTimeStamp_,))
                break


def doClose(listIndex, eventType):
    global gTrades
    global gOneMinListData
    global gNowTrade
    global gRunRealTime
    global gfmex

    if (gRunRealTime == False):
        gNowTrade.exitPrice_ = eval(commonlib.replaceJudgeStr(eventType["price"]))
        coinNum = gNowTrade.coinNum_
        print("ori coin num:%lf" % coinNum)
        position = gNowTrade.position_
        print(position)
        if (position < 0):
            position = 0 - position
        print(position)
        if (gNowTrade.direction_ == "short"):
            gNowTrade.coinNum_ = gNowTrade.coinNum_ - position / gNowTrade.entryPrice_ + position / gNowTrade.exitPrice_
            print("do short close...")
        else:
            gNowTrade.coinNum_ = gNowTrade.coinNum_ + position / gNowTrade.entryPrice_ - position / gNowTrade.exitPrice_
            print("do long close...")
        gNowTrade.direction_ = "non-direction"

        gNowTrade.position_ = 0

        trade = Trade(gNowTrade)

        print("now coin num:%lf" % trade.coinNum_)
        print("enterPrice:%lf  exitPrice:%lf" % (trade.entryPrice_, trade.exitPrice_,))
        print("      ")
        gTrades.append(trade)    
    else:
        gNowTrade.exitPrice_ = eval(commonlib.replaceJudgeStr(eventType["price"]))
        coinNum = gNowTrade.coinNum_
        print("ori coin num:%lf" % coinNum)
        position = gNowTrade.position_
        print(position)
        if (position < 0):
            position = 0 - position
        print(position)
        if (gNowTrade.direction_ == "short"):
            gNowTrade.coinNum_ = gNowTrade.coinNum_ - position / gNowTrade.entryPrice_ + position / gNowTrade.exitPrice_
            print("do short close...")
            gfmex.buy_limit_long("btcusd_p", gNowTrade.exitPrice_, position)
        else:
            gNowTrade.coinNum_ = gNowTrade.coinNum_ + position / gNowTrade.entryPrice_ - position / gNowTrade.exitPrice_
            print("do long close...")
            gfmex.sell_limit_short("btcusd_p", gNowTrade.exitPrice_, position)
        gNowTrade.direction_ = "non-direction"

        gNowTrade.position_ = 0

        trade = Trade(gNowTrade)

        print("now coin num:%lf" % trade.coinNum_)
        print("enterPrice:%lf  exitPrice:%lf, time:%d"% (trade.entryPrice_, trade.exitPrice_, int(time.time())))
        print("      ")
        gTrades.append(trade)    

def waitEvent(dictStrategy, listIndex):
    global gOneMinListData
    global gTrades
    waitEvent = dictStrategy["waitEvent"]
    for i in range(len(waitEvent)):
        eventType = dictStrategy[waitEvent[i]]
        eventResult = eventJudge(eventType, listIndex)
        if (eventResult == True):
            return waitEvent[i]
    return "nothing happen"

def runRealTime(strategyPath):
    global gRunRealTime
    gRunRealTime = True
    #runReal()
    run(strategyPath)

def runReal():
    dictStrategy = strategyParse.parseStrategy("../strategy/trendFiveMinClose2.strategy")

    global gOneMinListData
    global gfmex
    candleData = gfmex.get_candle_timestamp("M1", "btcusd_p", int(time.time()))["data"]
    for val in candleData:
        gOneMinListData.append(val)

    #increase by id
    gOneMinListData = list(reversed(gOneMinListData))

    listIndex = 20
    while (1):
        event = waitEvent(dictStrategy, listIndex)
        if (event == "openLong"):
            doShort(listIndex, dictStrategy[event])
        elif (event == "openShort"):
            doLong(listIndex, dictStrategy[event])
        elif (event == "closePosition"):
            doClose(listIndex, dictStrategy[event])    
        #else:
            #in this date, nothing happend
        #listIndex = listIndex + 1
        time.sleep(1)
        gOneMinListData = []
        candleData = gfmex.get_candle_timestamp("M1", "btcusd_p", int(time.time()))["data"]
        for val in candleData:
            gOneMinListData.append(val)

        #increase by id
        gOneMinListData = list(reversed(gOneMinListData))

def runSimulation(strategyPath):
    global gRunRealTime
    gRunRealTime = False
    run(strategyPath)

#TODO merge real and simulation
def run(strategyPath):
    loadMongoData()
    # this is test strategy FIXME
    dictStrategy = strategyParse.parseStrategy(strategyPath)

    global gOneMinListData
    listIndex = 0
    while (listIndex < len(gOneMinListData)):
        event = waitEvent(dictStrategy, listIndex)
        if (event == "openLong"):
            doShort(listIndex, dictStrategy[event])
        elif (event == "openShort"):
            doLong(listIndex, dictStrategy[event])
        elif (event == "closePosition"):
            doClose(listIndex, dictStrategy[event])    
        #else:
            #in this date, nothing happend
        listIndex = listIndex + 1

    global gTrades
    print(len(gTrades))
    draw.drawCoinNum(gTrades)
    draw.drawPosition(gTrades)

global gOneMinListData
gOneMinListData = []
global gTrades
gTrades = []
global gNowTrade
gNowTrade = Trade()
global gRunRealTime
gRunRealTime = False
global gfmex
gfmex = Fmex()
gfmex.auth(conf.key, conf.secret)

if __name__ == '__main__':
    runSimulation("../strategy/trendFiveMinClose2.strategy")
