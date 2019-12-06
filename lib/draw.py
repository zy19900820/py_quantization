import matplotlib
matplotlib.use('Tkagg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import time
from datetime import datetime

def getTimeStr(timeStamp):
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def drawCoinNum(trades):
    fig = plt.figure()

    timeStamp = []
    coinNum = []

    for i in range(len(trades)):
        #timeStamp.append(trades[i].entryTimeStamp_)
        timeStamp.append(datetime.fromtimestamp(trades[i].entryTimeStamp_))
        coinNum.append(trades[i].coinNum_)
    
    plt.plot(timeStamp, coinNum)
    plt.gcf().autofmt_xdate()
    fig.savefig('../pic/coin.png')

def drawPosition(trades):
    fig = plt.figure()

    timeStamp = []
    position = []

    for i in range(len(trades)):
        #timeStamp.append(trades[i].entryTimeStamp_)
        timeStamp.append(datetime.fromtimestamp(trades[i].entryTimeStamp_))
        position.append(trades[i].position_)
    
    plt.plot(timeStamp, position)
    plt.gcf().autofmt_xdate()
    fig.savefig('../pic/position.png')

def drawPrice(trades):
    fig = plt.figure()

    timeStamp = []
    price = []

    for i in range(len(trades)):
        #timeStamp.append(trades[i].entryTimeStamp_)
        timeStamp.append(datetime.fromtimestamp(trades[i].entryTimeStamp_))
        if (trades[i].direction_ == "non-direction"):
            price.append(trades[i].exitPrice_)
        else:
            price.append(trades[i].entryPrice_)
    
    plt.plot(timeStamp, price)
    plt.gcf().autofmt_xdate()
    fig.savefig('../pic/price.png')
