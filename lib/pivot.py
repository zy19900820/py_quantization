#coding:utf-8
from commonlib import getDirection
from commonlib import getBeforeClose
import commonlib
import time
import strategyParse
from trade import Trade
import sys
import draw
import datamanage
import log

def position1000():
    return 1

def doShort(oneMinListData, listIndex, eventType):
    global gTrades
    global gNowTrade

    entryPrice = eval(commonlib.replaceJudgeStr(eventType["price"]));
    count = eval(commonlib.replaceJudgeStr(eventType["count"]))
    uuid = datamanage.doShort(entryPrice, count)
    if (uuid != -1):
        gNowTrade.entryTimeStamp_ = datamanage.getNowTimeStamp(oneMinListData, listIndex)
        gNowTrade.direction_ = "short"
        gNowTrade.position_ = gNowTrade.position_ - count
        gNowTrade.entryPrice_ = entryPrice
        gNowTrade.uuid_ = uuid

        trade = Trade(gNowTrade)
        gTrades.append(trade)    
        log.doShortLog(trade)

def doLong(oneMinListData, listIndex, eventType):
    global gTrades
    global gNowTrade

    entryPrice = eval(commonlib.replaceJudgeStr(eventType["price"]));
    count = eval(commonlib.replaceJudgeStr(eventType["count"]))
    uuid = datamanage.doLong(entryPrice, count)
    if (uuid != -1):
        gNowTrade.entryTimeStamp_ = datamanage.getNowTimeStamp(oneMinListData, listIndex)
        gNowTrade.direction_ = "long"
        gNowTrade.position_ = gNowTrade.position_ + count
        gNowTrade.entryPrice_ = entryPrice
        gNowTrade.uuid_ = uuid

        trade = Trade(gNowTrade)
        gTrades.append(trade)    
        log.doLongLog(trade)

def doClose(oneMinListData, listIndex, eventType):
    global gTrades
    global gNowTrade

    exitPrice = eval(commonlib.replaceJudgeStr(eventType["price"]))
    position = gNowTrade.position_
    if (position < 0):
        position = 0 - position

    timeStamp = datamanage.getNowTimeStamp(oneMinListData, listIndex)
    uuid = datamanage.doClose(exitPrice, position, gNowTrade.direction_)
    if (uuid != -1):
        gNowTrade.exitPrice_ = exitPrice
        coinNum = gNowTrade.coinNum_
        if (gNowTrade.direction_ == "short"):
            gNowTrade.coinNum_ = gNowTrade.coinNum_ - position / gNowTrade.entryPrice_ + position / gNowTrade.exitPrice_
        else:
            gNowTrade.coinNum_ = gNowTrade.coinNum_ + position / gNowTrade.entryPrice_ - position / gNowTrade.exitPrice_
        gNowTrade.exitTimeStamp_ = datamanage.getNowTimeStamp(oneMinListData, listIndex)
        gNowTrade.direction_ = "non-direction"
        gNowTrade.position_ = 0

        trade = Trade(gNowTrade)
        gTrades.append(trade)    
        log.doCloseLog(trade)
    else:
        log.doCloseErrorLog(timeStamp)


def eventJudge(eventType, oneMinListData, listIndex):
    global gNowTrade

    nowTimeStamp = datamanage.getNowTimeStamp(oneMinListData, listIndex)
    position = gNowTrade.position_
    openPositionTimeStamp = gNowTrade.entryTimeStamp_

    eventJudgeStr = eventType["formula"]
    evalStr = commonlib.replaceJudgeStr(eventJudgeStr)
    if (evalStr == ""):
        print("replaceJudgeStr Error, ori string:%s" % eventJudgeStr)
        return False
    return eval(evalStr)

def waitEvent(dictStrategy, oneMinListData, listIndex):
    waitEvent = dictStrategy["waitEvent"]
    for i in range(len(waitEvent)):
        eventType = dictStrategy[waitEvent[i]]
        eventResult = eventJudge(eventType, oneMinListData, listIndex)
        if (eventResult == True):
            return waitEvent[i]
    return "nothing happen"

def runRealTime(strategyPath):
    datamanage.setRunType(True)
    run(strategyPath)

def runSimulation(strategyPath):
    datamanage.setRunType(False)
    run(strategyPath)

def run(strategyPath):
    dictStrategy = strategyParse.parseStrategy(strategyPath)
    oneMinListData = datamanage.getOneMinData()

    listIndex = datamanage.getStartIndex()
    while (datamanage.ifHaveData(listIndex)):
        event = waitEvent(dictStrategy, oneMinListData, listIndex)
        if (event == "openLong"):
            doLong(oneMinListData, listIndex, dictStrategy[event])
        elif (event == "openShort"):
            doShort(oneMinListData, listIndex, dictStrategy[event])
        elif (event == "closePosition"):
            doClose(oneMinListData, listIndex, dictStrategy[event])    
        #else:
            #in this date, nothing happend
        listIndex = datamanage.getNextListIndex(listIndex)
        #think...   bug?? data in real time is change
        oneMinListData = datamanage.getOneMinData()
        datamanage.sleepSomeTime()

    global gTrades
    print(len(gTrades))
    draw.drawCoinNum(gTrades)
    draw.drawPosition(gTrades)
    draw.drawPrice(gTrades)

global gTrades
gTrades = []
global gNowTrade
gNowTrade = Trade()

if __name__ == '__main__':
    runSimulation("../strategy/trendFiveMinClose.strategy")
