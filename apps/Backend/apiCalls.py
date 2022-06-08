import requests
from dbpass import *
from datetime import datetime

api_key =  getapi()

def listallcompanies():
    request_url = 'https://simfin.com/api/v2/companies/list'

    parameters = {"api-key": api_key}

    request = requests.get(request_url, parameters)
    data = request.json()
    listComp = []
    size = len(data['data'])
    for x in range(size):
        listComp.append(data['data'][x])

    # print(data['columns'])
    # for x in range(size):
    onlyTicker = []
    for x in listComp:
        onlyTicker.append(x[1])

    return onlyTicker

def getShareMarketEarn(t,date):
    allStocksDetails = {}
    startDay = date
    endDay = getEndDay(date)
    tickers = t



    arrayOfArrayOfTickers = []
    shortArrayOftickers = []
    toSize = 0
    tempCount = 0
    for x in tickers:
        shortArrayOftickers.append(x)
        if toSize==799:
            toSize = 0
            arrayOfArrayOfTickers.append(shortArrayOftickers)
            shortArrayOftickers = []
            tempCount = tempCount+1
        toSize = toSize +1

    arrayOfArrayOfTickers.append(shortArrayOftickers)



    for tick in arrayOfArrayOfTickers:
        request_url = 'https://simfin.com/api/v2/companies/prices'
        parameters = {"ticker": ",".join(tick), "start": startDay, "end": endDay, "api-key": api_key,
                      "ratios": ""}
        request = requests.get(request_url, parameters)
        all_data = request.json()


        for response_index, data in enumerate(all_data):
            # make sure that data was found
            if data['found'] and len(data['data']) > 0:
                columns = data['columns']
                tickerPos = -1
                marketCapPos = -1
                SharePricePos = -1
                EVPos = -1
                earningsPos = -1
                count = 0
                for x in columns:
                    if x == "Ticker":
                        tickerPos = count
                    if x == "Market-Cap":
                        marketCapPos = count
                    if x == "Close":
                        SharePricePos = count
                    if x == "Enterprise Value (ttm)":
                        EVPos = count
                    if x == "EV/EBITDA (ttm)":
                        earningsPos = count
                    count = count+1
                firstArray = data['data'][0]
                nameOFstock = firstArray[tickerPos]
                marketCap = firstArray[marketCapPos]
                sharePrice = firstArray[SharePricePos]
                Ev = firstArray[EVPos]
                earnCalc = firstArray[earningsPos]
                earningBefore = None
                if Ev != None and earnCalc != None:
                    earningBefore = float(Ev)/float(earnCalc)


                parameters = [sharePrice,marketCap,str(earningBefore)]
                allStocksDetails[nameOFstock] = parameters
    print("Retrieved Share Price, Market Cap and Earnings Before Interest, Taxes, Depreciation, and Amortization")

    return allStocksDetails

def getEndDay(date):
    strDate = date.split('-')
    year = strDate[0]
    month = strDate[1]
    day = strDate[2]

    intYear = int(year)
    intMonth = int(month)
    intDay = int(day)

    newYear = intYear
    newMonth = intMonth
    newDay = intDay+4

    arrayOf31Days = [1,3,5,7,8,10,12]
    if intMonth in arrayOf31Days:
        if newDay>31:
            newDay = newDay-31
            newMonth = newMonth+1
    else:
        if newMonth == 2:
            if newDay>28:
                newDay = newDay-28
                newMonth = newMonth+1
        else:
            if newDay > 30:
                newDay = newDay -30
                newMonth = newMonth+1

    if newMonth == 13:
        newMonth = 1
        newYear = newYear+1

    strNewMonth= str(newMonth)
    strNewDay = str(newDay)
    if len(strNewMonth) == 1:
        strNewMonth = "0"+strNewMonth
    if len(strNewDay) == 1:
        strNewDay = "0" + strNewDay

    strDate = str(newYear)+"-"+strNewMonth+"-"+strNewDay
    return strDate


