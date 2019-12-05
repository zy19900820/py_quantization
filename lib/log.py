import time
import trade

def doShortLog(trade):
    timeArray = time.localtime(trade.entryTimeStamp_)
    timeStr = time.strftime("%Y-%m--%d %H:%M:%S", timeArray)
    print("do short, price:%lf, count:%d, time:%s" % (trade.entryPrice_,
        trade.position_, timeStr))

def doLongLog(trade):
    timeArray = time.localtime(trade.entryTimeStamp_)
    timeStr = time.strftime("%Y-%m--%d %H:%M:%S", timeArray)
    print("do long, price:%lf, count:%d, time:%s" % (trade.entryPrice_,
        trade.position_, timeStr))

def doCloseLog(trade):
    timeArray = time.localtime(trade.exitTimeStamp_)
    timeStr = time.strftime("%Y-%m--%d %H:%M:%S", timeArray)
    print("do close, price:%lf, coinNum:%lf, time:%s" % (trade.exitPrice_,
        trade.coinNum_, timeStr))

def doCloseErrorLog(timeStamp):
    timeArray = time.localtime(timeStamp)
    timeStr = time.strftime("%Y-%m--%d %H:%M:%S", timeArray)
    print("do close error, time:%s" % timeStr)

def logAllTrade(trades):
    for var in trades:
        print(var.tradeToJson()) 
