#coding:utf-8
from commonlib import getDirection
from commonlib import getBeforeClose
import commonlib
import time
from pymongo import MongoClient
from trade import Trade
import sys
import fmexOperation

def loadMongoData():
    print("loadMongoData start...")

    global gOneMinListData
    conn = MongoClient('127.0.0.1', 27017)
    db = conn["fmexCandleData"]
    col = db["btcusd_p_M1"]
    for val in col.find().sort("id", 1):
        gOneMinListData.append(val)

    print("loadMongoData end...")

def setRunType(bRunRealTime):
    global gRunRealTime
    gRunRealTime = bRunRealTime

def getOneMinData():
    global gRunRealTime
    global gOneMinListData
    if (gRunRealTime == False):
        return gOneMinListData
    else:
        return fmexOperation.getOneMinData()

def getStartIndex():
    global gRunRealTime
    if (gRunRealTime == False):
        return 0
    else:
        #default 20
        return 20

def ifHaveData(listIndex):
    global gRunRealTime
    global gOneMinListData
    if (gRunRealTime == False):
        return listIndex < len(gOneMinListData)
    else:
        return True

def getNextListIndex(listIndex):
    global gRunRealTime
    if (gRunRealTime == False):
        return listIndex + 1
    else:
        return 20

def sleepSomeTime():
    global gRunRealTime
    if (gRunRealTime == False):
        return
    else:
        time.sleep(1)
        return

def getNowTimeStamp(oneMinListData, listIndex):
    global gRunRealTime
    if (gRunRealTime == False):
        return oneMinListData[listIndex]["id"]
    else:
        return int(time.time())
    
def doShort(entryPrice, count):
    global gRunRealTime
    if (gRunRealTime == False):
        return 0
    else:
        return fmexOperation.doShort(entryPrice, count)

def doLong(entryPrice, count):
    global gRunRealTime
    if (gRunRealTime == False):
        return 0
    else:
        return fmexOperation.doLong(entryPrice, count)

def doClose(entryPrice, count, direction):
    global gRunRealTime
    #close mean entry order
    if (gRunRealTime == False):
        return 0
    else:
        return fmexOperation.doClose(entryPrice, count, direction)

global gRunRealTime
gRunRealTime = False

global gOneMinListData
gOneMinListData = []
loadMongoData()

if __name__ == '__main__':
    runSimulation("../strategy/trendFiveMinClose2.strategy")
