#coding:utf-8
from fmex import Fmex
from time import strftime, localtime
import time
import json
from pymongo import MongoClient
import thread

def insertOne(dbSet, data):
    for value in data:
        dbSet.update_one(value, {"$set":value}, upsert=True)

def insertDataByType(dbSet, intervalType):
    candleData = fmex.get_candle_timestamp(intervalType, "btcusd_p", int(time.time()))["data"]
    id = 0

    #没有获取完数据
    while len(candleData) > 0:
        id = candleData[len(candleData) - 1]["id"] - 1
        insertOne(dbSet, candleData)
        candleData = fmex.get_candle_timestamp(intervalType, "btcusd_p", id)["data"]

    while (1):
        if (intervalType == "D1"):
            time.sleep(60*60*24)
        elif (intervalType == "H6"):
            time.sleep(60*60*6)
        elif (intervalType == "H4"):
            time.sleep(60*60*4)
        elif (intervalType == "H1"):
            time.sleep(60*60)
        elif (intervalType == "M30"):
            time.sleep(60*30)
        elif (intervalType == "M15"):
            time.sleep(60*15)
        elif (intervalType == "M5"):
            time.sleep(60*5)
        elif (intervalType == "M3"):
            time.sleep(60*3)
        else:
            time.sleep(2)

        candleData = fmex.get_candle_timestamp(intervalType, "btcusd_p", int(time.time()))["data"]
        insertOne(dbSet, candleData)

conn = MongoClient('127.0.0.1', 27017)

fmex = Fmex()
db = conn.fmexCandleData

thread.start_new_thread(insertDataByType, (db.btcusd_p_D1, "D1", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_H6, "H6", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_H4, "H4", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_H1, "H1", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_M30, "M30", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_M15, "M15", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_M5, "M5", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_M3, "M3", ))
thread.start_new_thread(insertDataByType, (db.btcusd_p_M1, "M1", ))

while 1:
    time.sleep(1111111)
