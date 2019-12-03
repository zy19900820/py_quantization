#coding:utf-8
from commonlib import getDirection
from commonlib import getBeforeClose
import commonlib
import time
from pymongo import MongoClient
#from fmex import Fmex
import strategyParse
from trade import Trade
import matplotlib
matplotlib.use('Tkagg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

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
    return 1000

def eventJudge(eventType, listIndex):
    global gOneMinListData
    global gNowTrade

    position = gNowTrade.position_
    nowTimeStamp = gOneMinListData[listIndex]["id"]
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

    gNowTrade.entryPrice_ = eval(commonlib.replaceJudgeStr(eventType["price"]))
    gNowTrade.entryTimeStamp_ = gOneMinListData[listIndex]["id"]
    gNowTrade.position_ = gNowTrade.position_ - eval(commonlib.replaceJudgeStr(eventType["count"]))
    gNowTrade.direction_ = "short"

    trade = Trade(gNowTrade)

    gTrades.append(trade)    

def doLong(listIndex, eventType):
    global gTrades
    global gOneMinListData
    global gNowTrade

    gNowTrade.entryTimeStamp_ = gOneMinListData[listIndex]["id"]
    gNowTrade.entryPrice_ = eval(commonlib.replaceJudgeStr(eventType["price"]))
    gNowTrade.position_ = gNowTrade.position_ + eval(commonlib.replaceJudgeStr(eventType["count"]))
    gNowTrade.direction_ = "long"
    
    trade = Trade(gNowTrade)

    gTrades.append(trade)    

def doClose(listIndex, eventType):
    global gTrades
    global gOneMinListData
    global gNowTrade

    gNowTrade.exitPrice_ = eval(commonlib.replaceJudgeStr(eventType["price"]))
    gNowTrade.position_ = 0
    if (gNowTrade.direction_ == "short"):
        gNowTrade.coinNum_ = gNowTrade.coinNum_ - 10000 / gNowTrade.entryPrice_ + 10000 / gNowTrade.exitPrice_
    else:
        gNowTrade.coinNum_ = gNowTrade.coinNum_ + 10000 / gNowTrade.entryPrice_ - 10000 / gNowTrade.exitPrice_
    gNowTrade.direction_ = "non-direction"

    trade = Trade(gNowTrade)

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

def runSimulation():
    loadMongoData()
    # this is test strategy FIXME
    dictStrategy = strategyParse.parseStrategy("../strategy/trendFiveMinClose2.strategy")

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
    fig1 = plt.figure()
    timeStamp = []
    position = []
    coinNum = []

    for i in range(len(gTrades)):
        timeStamp.append(gTrades[i].entryTimeStamp_)
        position.append(gTrades[i].position_)
        coinNum.append(gTrades[i].coinNum_)
    plt.plot(timeStamp, position)
    fig1.savefig('../pic/position.png')


    fig2 = plt.figure()
    plt.plot(timeStamp, coinNum)
    fig2.savefig('../pic/coin.png')

    plt.show()

global gOneMinListData
gOneMinListData = []
global gTrades
gTrades = []
global gNowTrade
gNowTrade = Trade()

if __name__ == '__main__':
    runSimulation()
