#coding:utf-8
def getOneDataDirection(oneListData):
    if (oneListData["open"] > oneListData["close"]):
        return "short"
    elif (oneListData["open"] < oneListData["close"]):
        return "long"
    else:
        return "null"

def getDirection(listData, index, num):
    firstDirection = getOneDataDirection(listData[index - num])
    for i in range(0, num - 1):
        direction = getOneDataDirection(listData[index - num + 1 + i])
        if (direction != firstDirection):
            return "null"
    return firstDirection

def getBeforeClose(listData, index, num):
    return listData[index - num]["close"]
    
def replaceJudgeStr(judgeStr):
    evalStr = judgeStr
    startIndex = evalStr.find("${")
    while (startIndex != -1):
        endIndex = evalStr.find("}", startIndex)
        if (endIndex == -1):
            return ""

        oriStr = evalStr[startIndex:endIndex+1]
        newStr = evalStr[startIndex+2:endIndex]
        evalStr = evalStr.replace(oriStr, newStr)
        startIndex = evalStr.find("${")
    return evalStr
