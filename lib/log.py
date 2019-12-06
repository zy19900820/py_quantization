import time
import trade

def doShortLog(trade):
    timeArray = time.localtime(trade.entryTimeStamp_)
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print("do short, price:%lf, count:%d, time:%s" % (trade.entryPrice_,
        trade.position_, timeStr))

def doLongLog(trade):
    timeArray = time.localtime(trade.entryTimeStamp_)
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print("do long, price:%lf, count:%d, time:%s" % (trade.entryPrice_,
        trade.position_, timeStr))

def doCloseLog(trade):
    timeArray = time.localtime(trade.exitTimeStamp_)
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print("do close, price:%lf, coinNum:%lf, time:%s" % (trade.exitPrice_,
        trade.coinNum_, timeStr))

def doCloseErrorLog(exitPrice, position, direction, timeStamp):
    #direction long  mean do short
    timeArray = time.localtime(timeStamp)
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print("do close error, price:%lf, position:%d, direction:%s time:%s" % (exitPrice,
        position, direction, timeStr))

def logAllTrade(trades):
    f = open("trades.txt", "w+")
    for var in trades:
        #print(var.tradeToJson()) 
        f.write(var.tradeToJson())
        f.write("\n")
    f.close()
