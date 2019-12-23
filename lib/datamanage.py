#coding:utf-8
import time
from pymongo import MongoClient
import sys
import fmexOperation
from commonlib import getOpenOrderStatus
import json
import traceback

def loadMongoData():
    print("loadMongoData start...")
    #traceback.print_stack()

    global gOneMinListData
    conn = MongoClient('127.0.0.1', 27017)
    db = conn["fmexCandleData"]
    col = db["btcusd_p_M1"]
    for val in col.find().sort("id", 1):
        gOneMinListData.append(val)

    #clear old data
    #for i in range(0, len(gOneMinListData)):
    #    if (gOneMinListData[i]["id"] == gOneMinListData[i - 1]["id"]):
    #        col.remove(gOneMinListData[i - 1])

    print("loadMongoData end...")
    print("end data...")
    print(gOneMinListData[-1])

def saveDay2Txt():
    OneDayListData = list()
    conn = MongoClient('127.0.0.1', 27017)
    db = conn["fmexCandleData"]
    col = db["btcusd_p_D1"]
    for val in col.find().sort("id", 1):
        OneDayListData.append(val)

    f = open("../datas/fmexDay2019.txt", "w+")
    f.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
    for i, data in enumerate(OneDayListData):
        timeArray = time.localtime(data["id"])
        timeStr = time.strftime("%Y-%m-%d", timeArray)
        f.write("%s,%.1f,%.1f,%.1f,%.1f,%.1f,%f\n" % (timeStr, data["open"],
            data["high"], data["low"], data["close"], data["close"], data["quote_vol"]))
    f.close()

def saveOneMin2Txt():
    OneMinListData = list()
    conn = MongoClient('127.0.0.1', 27017)
    db = conn["fmexCandleData"]
    col = db["btcusd_p_M1"]
    for val in col.find().sort("id", 1):
        OneMinListData.append(val)

    f = open("../datas/fmexOneMin2019.txt", "w+")
    f.write("Date,Time,Open,High,Low,Close,Volume,OpenInterest\n")
    for i, data in enumerate(OneMinListData):
        timeArray = time.localtime(data["id"])
        timeDataStr = time.strftime("%Y-%m-%d", timeArray)
        timeTimeStr = time.strftime("%H:%M:%S", timeArray)
        f.write("%s,%s,%.1f,%.1f,%.1f,%.1f,%f, 0.0\n" % (timeDataStr, timeTimeStr, data["open"],
            data["high"], data["low"], data["close"], data["quote_vol"]))
    f.close()

def saveFourHour2Txt():
    fourHourListData = list()
    conn = MongoClient('127.0.0.1', 27017)
    db = conn["fmexCandleData"]
    col = db["btcusd_p_H4"]
    for val in col.find().sort("id", 1):
        fourHourListData.append(val)

    f = open("../datas/fmexFourHour2019.txt", "w+")
    f.write("Date,Time,Open,High,Low,Close,Volume,OpenInterest\n")
    for i, data in enumerate(fourHourListData):
        timeArray = time.localtime(data["id"])
        timeDataStr = time.strftime("%Y-%m-%d", timeArray)
        timeTimeStr = time.strftime("%H:%M:%S", timeArray)
        f.write("%s,%s,%.1f,%.1f,%.1f,%.1f,%f, 0.0\n" % (timeDataStr, timeTimeStr, data["open"],
            data["high"], data["low"], data["close"], data["quote_vol"]))
    f.close()

def printDataToFile():
    global gOneMinListData
    for val in gOneMinListData:
        print(val)

def printSameIDDataToFile():
    global gOneMinListData
    for i in range(0, len(gOneMinListData)):
        if (gOneMinListData[i]["id"] == gOneMinListData[i - 1]["id"]):
            print(gOneMinListData[i-1])
            print(gOneMinListData[i])
            print("       ")

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

def dbGetOpenOrderStatus(oneMinListData, listIndex, orderStatusStr, trade):
    global gRunRealTime
    if (gRunRealTime == False):
        direction = trade.direction_
        entryPrice = trade.entryPrice_
        #print(direction)
        #print(entryPrice)
        #print(trade.entryTimeStamp_)
        return eval(orderStatusStr)
    else:
        return fmexOperation.getOpenOrderStatus(trade.uuid_)

def cancelOrder(uuid):
    global gRunRealTime
    if (gRunRealTime == False):
        return "fully_cancelled"
    else:
        return fmexOperation.cancelOrder(uuid)

def getOrderFillNum(uuid):
    global gRunRealTime
    if (gRunRealTime == False):
        return 0
    else:
        return fmexOperation.getOrderFillNum(uuid)

global gRunRealTime
gRunRealTime = False

global gOneMinListData
gOneMinListData = []
#loadMongoData()

if __name__ == '__main__':
    #printDataToFile()
    #printSameIDDataToFile()
    #saveDay2Txt()
    saveOneMin2Txt()
    #saveFourHour2Txt()
