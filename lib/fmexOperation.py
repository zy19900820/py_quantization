from fmex import Fmex
import conf
import time

def getOneMinData():
    oneMinListData = []

    candleData = gfmex.get_candle_timestamp("M1", "btcusd_p", int(time.time()))["data"]
    for val in candleData:
        oneMinListData.append(val)
    return list(reversed(oneMinListData))

def doShort(entryPrice, count):
    global gfmex
    for i in range(0, 5):
        orderInfo = gfmex.sell_post_only_limit_short("btcusd_p", entryPrice, count)
        orderStatus = orderInfo["data"]["status"]
        if (orderStatus == "fully_cancelled"):
            time.sleep(1)
        elif (orderStatus == "pending"):
            return orderInfo["data"]["id"]
    return -1

def doLong(entryPrice, count):
    global gfmex
    for i in range(0, 5):
        orderInfo = gfmex.buy_post_only_limit_long("btcusd_p", entryPrice, count)
        orderStatus = orderInfo["data"]["status"]
        if (orderStatus == "fully_cancelled"):
            time.sleep(1)
        elif (orderStatus == "pending"):
            return orderInfo["data"]["id"]
    return -1

def doClose(entryPrice, count, direction):
    #if direction == short     do long
    if (direction == "short"):
        return doLong(entryPrice, count)
    else:
        return doShort(entryPrice, count)

global gfmex
gfmex = Fmex()

gfmex.auth(conf.key, conf.secret)
