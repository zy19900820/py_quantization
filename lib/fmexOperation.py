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

def getOpenOrderStatus(uuid):
    global gfmex
    return gfmex.get_order(uuid)["data"]["status"]

def cancelOrder(uuid):
    global gfmex
    gfmex.cancel_order(uuid)
    orderStatus = gfmex.get_order(uuid)["data"]["status"]
    while(orderStatus != "partial_cancelled" and orderStatus != "fully_cancelled"):
        time.sleep(0.3)
        orderStatus = gfmex.get_order(uuid)["data"]["status"]
    return orderStatus

def getOrderFillNum(uuid):
    global gfmex
    orderInfo = gfmex.get_order(uuid)["data"]
    return orderInfo["quantity"] - orderInfo["unfilled_quantity"]

global gfmex
gfmex = Fmex()

gfmex.auth(conf.key, conf.secret)
