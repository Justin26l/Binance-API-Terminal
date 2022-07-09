import hmac, hashlib ,json,time
from pip._vendor import requests

def HMAC_SHA256(Key:str,Msg:str):
    return hmac.new(key=Key.encode(),msg=Msg.encode(),digestmod=hashlib.sha256).hexdigest()

def localTimeMS():
    return int(time.time()*1000)

def getM(futuresType:str,symbol:str,TimeFrame:str,limit:int):
    if futuresType == 'usd-m': routes='fapi'
    if futuresType == 'coin-m': routes='dapi'
    dataget = json.loads(requests.get(f"{urlhead}{ROUTES(futuresType)}{domain}{ROUTES(futuresType)}/v1/klines?symbol={symbol}&interval={TimeFrame}&limit={limit}").text)
    data=[]
    for x in dataget:
        data.append([int(float(x[0])),int(float(x[1])),int(float(x[2])),int(float(x[3])),int(float(x[4]))])
    return data

def ROUTES(futuresType):
    routes=''
    FT=futuresType.lower()
    if FT == 'usd-m': routes='fapi'
    if FT == 'coin-m': routes='dapi'
    if FT == 'spot': routes='api'
    return routes

####################
def ChangeLeverage(ApiKey:str,ApiSecret:str,futuresType:str,LV_symbol:str,leverage:int):
    if testnet :HeadRoute="testnet"
    else:HeadRoute=ROUTES(futuresType)
    if 1 <= leverage <= 125 :
        URL=urlhead+HeadRoute+domain+ROUTES(futuresType)+'/v1/leverage'
        LV_Head={'X-MBX-APIKEY': ApiKey}
        LV_Query=f'symbol={LV_symbol}&leverage={leverage}&timestamp={localTimeMS()}'
        LV_Data=f'{LV_Query}&signature={HMAC_SHA256(ApiSecret,LV_Query)}'
        Order=json.loads(requests.post(URL,headers=LV_Head,params=LV_Data).text)
        try :
            if Order['leverage'] == leverage :
                return {'Leverage':True,"Result":leverage}
        except : 
            return {'Leverage':False,"Result":Order}
    elif 0 == leverage : 
        return {'Leverage':False,"Result":"No Check 'Leverage'"}
    else  : 
        return {'Leverage':False,"Result":"Syntax Error 'Leverage'"}

def ChangeMarginType(ApiKey:str,ApiSecret:str,futuresType:str,MT_symbol:str,MarginType:str):
    if testnet :HeadRoute="testnet"
    else:HeadRoute=ROUTES(futuresType)
    if MarginType == 'CROSSED' or MarginType =='ISOLATED':
        URL=urlhead+HeadRoute+domain+ROUTES(futuresType)+'/v1/marginType'
        MT_Head={'X-MBX-APIKEY': ApiKey}
        MT_Query=f'symbol={MT_symbol}&marginType={MarginType}&timestamp={localTimeMS()}'
        MT_Data=f'{MT_Query}&signature={HMAC_SHA256(ApiSecret,MT_Query)}'
        Order=json.loads(requests.post(URL,headers=MT_Head,params=MT_Data).text)
        if Order['code'] == 200 :
            return {'MarginType':True,"Result":MarginType}
        elif Order['code'] == -4046:
            return {'MarginType':True,"Result":MarginType}
        else : 
            return {'MarginType':False,"Result":Order}
    else : 
        return {'MarginType':False,"Result":"Syntax Error 'MarginType'"}

def ClearOpenOrder(ApiKey:str,ApiSecret:str,futuresType:str,CO_symbol:str):
    if testnet :HeadRoute="testnet"
    else:HeadRoute=ROUTES(futuresType)
    URL=urlhead+HeadRoute+domain+ROUTES(futuresType)+'/v1/allOpenOrders'
    CO_Head={'X-MBX-APIKEY': ApiKey}
    CO_Query=f'symbol={CO_symbol}&timestamp={localTimeMS()}'
    CO_Data=f'{CO_Query}&signature={HMAC_SHA256(ApiSecret,CO_Query)}'
    Order=json.loads(requests.delete(URL,headers=CO_Head,params=CO_Data).text)
    if Order == 200 :
        return {'ClearOpenOrder':True,"Result":CO_symbol}
    else : 
        return {'ClearOpenOrder':False,"Result":Order}
    
def EntryMarket(ApiKey:str,ApiSecret:str,futuresType:str,EM_symbol:str,EM_side:str,EM_Quantity:float,ID:str):
    if testnet :HeadRoute="testnet"
    else:HeadRoute=ROUTES(futuresType)
    EM_URL=urlhead+HeadRoute+domain+ROUTES(futuresType)+'/v1/order'
    EM_Head={'X-MBX-APIKEY': ApiKey}
    EM_Query=f'symbol={EM_symbol}&side={EM_side}&type=MARKET&quantity={EM_Quantity}&newClientOrderId={ID+str(localTimeMS())}&timestamp={localTimeMS()}'
    EM_Data=f'{EM_Query}&signature={HMAC_SHA256(ApiSecret,EM_Query)}'
    EM_Order=''
    try:
        Order=json.loads(requests.post(EM_URL,headers=EM_Head,params=EM_Data).text)
        EM_Order={'EntryMarket':True,"Result":{"id":Order['clientOrderId'], "symbol":Order['symbol'], "type":Order['type'], "side":Order['side'], "Qty":Order['origQty'], "reduceOnly":Order['reduceOnly'], "updateTime":Order['updateTime']}}
    except:
        EM_Order={'EntryMarket':False,"Result":Order}
    return EM_Order

def CloseMarket(ApiKey:str,ApiSecret:str,futuresType:str,Close_symbol:str,Close_side:str,Close_Quantity:str):
    if testnet :HeadRoute="testnet"
    else:HeadRoute=ROUTES(futuresType)
    
    if Close_side == "BUY":TPSL_side="SELL"
    elif Close_side == "SELL":TPSL_side="BUY"
    Close_URL=urlhead+HeadRoute+domain+ROUTES(futuresType)+'/v1/order'
    Close_Head={'X-MBX-APIKEY': ApiKey}
    Close_Query=f'symbol={Close_symbol}&side={TPSL_side}&type=MARKET&reduceOnly=true&quantity={Close_Quantity}&timestamp={localTimeMS()}'
    Close_Data=f'{Close_Query}&signature={HMAC_SHA256(ApiSecret,Close_Query)}'
    Order=json.loads(requests.post(Close_URL,headers=Close_Head,params=Close_Data).text)
    Close_Order=''
    try:
        Close_Order={'CloseMarket':True,"Result":{"id":Order['orderId'], "symbol":Order['symbol'], "type":Order['type'], "side":Order['side'], "Qty":Order['origQty'], "reduceOnly":Order['reduceOnly'], "updateTime":Order['updateTime']}}
    except:
        Close_Order={'CloseMarket':False,"Result":Order}
    return Close_Order

def SetTP(ApiKey:str,ApiSecret:str,futuresType:str,TP_symbol:str,TP_side:str,TP_Price:float,TP_Quantity:float):
    if testnet :HeadRoute="testnet"
    else:HeadRoute=ROUTES(futuresType)
    
    if TP_side == "BUY":TPSL_side="SELL"
    elif TP_side == "SELL":TPSL_side="BUY"
    TP_URL=urlhead+HeadRoute+domain+ROUTES(futuresType)+'/v1/order'
    TP_Head={'X-MBX-APIKEY': ApiKey}
    TP_Query=f'symbol={TP_symbol}&side={TPSL_side}&type=TAKE_PROFIT_MARKET&stopPrice={float(str(TP_Price)[0:6])}&quantity={TP_Quantity}&closePosition=false&newClientOrderId=TP/SL{localTimeMS()}&timestamp={localTimeMS()}'
    TP_Data=f'{TP_Query}&signature={HMAC_SHA256(ApiSecret,TP_Query)}'
    tpOrder=json.loads(requests.post(TP_URL,headers=TP_Head,params=TP_Data).text)
    TP_Order=''
    try:
        TP_Order={'SetTP':True,"Result":{"id":tpOrder['orderId'],"symbol":tpOrder['symbol'],"type":tpOrder['type'],"side":tpOrder['side'],"OrderQTY":tpOrder['origQty'],"reduceOnly":tpOrder['reduceOnly'],"closePosition":tpOrder['closePosition'],"updateTime":tpOrder['updateTime']}}
    except:
        TP_Order={'SetTP':False,"Result":tpOrder}
    return TP_Order

def SetSL(ApiKey:str,ApiSecret:str,futuresType:str,SL_symbol:str,SL_side:str,SL_Price:float,SL_Quantity:float):
    if testnet :HeadRoute="testnet"
    else:HeadRoute=ROUTES(futuresType)
    
    if SL_side == "BUY":TPSL_side="SELL"
    elif SL_side == "SELL":TPSL_side="BUY"
    SL_URL=urlhead+HeadRoute+domain+ROUTES(futuresType)+'/v1/order'
    SL_Head={'X-MBX-APIKEY': ApiKey}
    SL_Query=f'symbol={SL_symbol}&side={TPSL_side}&type=STOP_MARKET&stopPrice={float(str(SL_Price)[0:6])}&quantity={SL_Quantity}&closePosition=false&newClientOrderId=TP/SL{localTimeMS()}&timestamp={localTimeMS()}'
    SL_Data=f'{SL_Query}&signature={HMAC_SHA256(ApiSecret,SL_Query)}'
    slOrder=json.loads(requests.post(SL_URL,headers=SL_Head,params=SL_Data).text)
    SL_Order=''
    try:
        SL_Order={'SetSL':True,"Result":{"id":slOrder['orderId'],"symbol":slOrder['symbol'],"type":slOrder['type'],"side":slOrder['side'],"OrderQTY":slOrder['origQty'],"reduceOnly":slOrder['reduceOnly'],"closePosition":slOrder['closePosition'],"updateTime":slOrder['updateTime']}}
    except:
        SL_Order={'SetSL':False,"Result":slOrder}
    return SL_Order

# baseurl='https://testnet.binancefuture.com/'
# url='https://testnet.binancefuture.com/fapi/v1/allOpenOrders'
testnet=True
urlhead='https://'
domain='.binancefuture.com/'
# domain='.binance.com/'

# apiKey='9ef7ed2db9de19f8b38056abefc3d18237e826aae02bea548c8f6c2a55ba9cc1'
# secretKey='236586d2c0788febb9a4b2a7a0865ea75a0cf1642867639e39dbda44a4e154f0'

# Symbol = 'BTCUSDT'
# Side = 'BUY' # 'BUY' 'SELL'
# Quantity=0.001
# Price=40000
# TP_Price=24000
# SL_Price=19000

# print(ChangeLeverage(apiKey,secretKey,'usd-m',Symbol,10))
# print(ClearOpenOrder(apiKey,secretKey,'usd-m',Symbol))
# print(EntryMarket(apiKey,secretKey,'usd-m',Symbol,Side,Quantity,"CustomID"))
# print(SetTP(apiKey,secretKey,'usd-m',Symbol,Side,TP_Price,Quantity))
# print(SetSL(apiKey,secretKey,'usd-m',Symbol,Side,SL_Price,Quantity))
# CloseMarket
# TPSL will auto convert to order side by input
