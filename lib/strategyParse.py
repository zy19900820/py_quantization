#coding:utf-8
import json

def parseStrategy(strategyPath):
    print("start strategy: %s" % (strategyPath))
    f = open(strategyPath)
    content = f.read()
    f.close()
    return json.loads(content)

if __name__ == '__main__':
    parseStrategy("../strategy/trend.strategy")
