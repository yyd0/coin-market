import json
import time
import urllib.request


class CoinInfo:

    def __init__(self, id, name, symbol, lastPrice, price):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.lastPrice = lastPrice
        self.price = price
        change = (self.price - self.lastPrice) / self.lastPrice
        self.change = change
        self.updateTime = time.strftime("%H:%M:%S", time.localtime())

    def __str__(self):
        s = ' 涨 ↑↑↑↑↑ '
        if self.change < 0:
            s = ' ↓↓↓↓↓ 跌 '
        return ' %s --- %s --- %f --- %f --- %s' % (self.name, s, self.change * 100, self.price, self.updateTime)


lastList = []
curList = []
while True:
    try:
        response = urllib.request.urlopen("https://api.coinmarketcap.com/v2/ticker/?structure=array&start=1&limit=5")
        result = response.read().decode('utf-8')
        jsonObj = json.loads(result)
        datas = jsonObj['data']
        curList.clear()
        for data in datas:
            id = data['id']
            name = data['name']
            symbol = data['symbol']
            price = data['quotes']['USD']['price']
            lastPrice = price
            if len(lastList) != 0:
                for i in lastList:
                    if i.id == id:
                        lastPrice = i.price
                        break
            coinInfo = CoinInfo(id, name, symbol, lastPrice, price)
            curList.append(coinInfo)
            # print(coinInfo)
            if abs(coinInfo.change) > 0.001:
                print(coinInfo)
        lastList.clear()
        lastList = lastList + curList
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('错误原因是' + str(e.reason))
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print('错误状态码是' + str(e.code))
    time.sleep(60)
