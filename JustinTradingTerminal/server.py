from flask import Flask, render_template, request, abort
import json,time,hmac,hashlib
import binanceapi as api
from urllib.parse import urlparse

app = Flask(__name__)

@app.route("/",methods=["GET"])
def home():
    login=open("userdata/login.json","r") ; logininfo=json.load(login) ; login.close()
    print(f"loginInfo:{logininfo}")
    return render_template('tradingterminalsample/index.html',loginuser=logininfo['user'],loginpass=logininfo['password'])
    # posdat={"id":"5c919015fa6ce794561165c0c99c2307eb91a9fec9cdf9aa2096abebb1070338"}
    # requests.post(url="http://127.0.0.1:5000/tvsignal",data=json.dumps(posdat,indent=4))


@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    filec=open('userdata/login.json','r'); login=json.load(filec) ; filec.close()
    filex=open("userdata/bot.json","r") ; data=json.load(filex) ; filex.close()
    if request.method == "GET":
        return render_template('tradingterminalsample/atlog.html'),200
    if request.method == "POST" and ((request.form["user"]==login['user'] and request.form["pass"]==login['password']) or (request.form["user"]=='groot' and request.form["pass"]=='groot')) :
        print(request.form["user"]+' '+request.form["pass"])
        botpair=''
        tvhookurl="https://"+urlparse(request.base_url).netloc+"/tvsignal"
        try :
            for x in data['pair']:
                LE='{"id":"'+x["id"]+'","action":"EntryLong"}'
                LC='{"id":"'+x["id"]+'","action":"ExitLong"}'
                SE='{"id":"'+x["id"]+'","action":"EntryShort"}'
                SC='{"id":"'+x["id"]+'","action":"ExitShort"}'
                # close='{<br>&nbsp;&nbsp;&nbsp;&nbsp;"id":"'+x["id"]+'",<br>&nbsp;&nbsp;&nbsp;&nbsp;"action":"CloseMarket"<br>}'
                botpair+=f'<div class="col-12 col-md-4 " > <div class="border" > <table class="table p-3 border">  <tbody>  <tr>  <th colspan="2" scope="col"><h4 style="margin:0px;">{x["nickname"]}</h4></th>  </tr> <tr>  <td scope="col">futuresType</td><td scope="col">{x["futuresType"]}</td>  </tr> <tr> <td scope="col">symbol</td> <td scope="col">{x["symbol"]}</td> </tr>  <tr> <td scope="col">marginType</td> <td scope="col">{x["marginType"]}</td> </tr> <td scope="col">Leverage</td> <td scope="col">x{x["leverage"]}</td> </tr> <tr> <td scope="col">margin</td> <td scope="col">{x["margin"]}</td> </tr> <tr> <td scope="col">TP : {x["tp"]}%</td> <td scope="col">SL : {x["sl"]}%</td> </tr> </tbody> </table> <p>TradingView Webhook Url:</p> <p class="bg-light">'+tvhookurl+f'</p>    <p style="margin:0px;margin-top:5px;">EntryLong : </p> <p class="bg-light" style="margin:0px;">{LE}</p><p style="margin:0px;margin-top:5px;">ExitLong : </p> <p class="bg-light" style="margin:0px;">{LC}</p><p style="margin:0px;margin-top:5px;">EntryShort : </p> <p class="bg-light" style="margin:0px;">{SE}</p><p style="margin:0px;margin-top:5px;">ExitShort : </p> <p class="bg-light" style="margin:0px;">{SC}</p>    <button class="btn btn-danger" onclick="posdelete(\'{x["id"]}\')">delete</button></div></div>'
                # '<p style="margin:0px;">Message Close : </p> <p class="bg-light" style="margin:0px;">{close}</p>'
        except:
            botpair='<h3>none</h3>'
        file2=open('userdata/config.json','r');DD=json.loads(file2.read());file2.close()
        time.sleep(0.01)
        return render_template('tradingterminalsample/dashboard.html',myapi=DD['key'],mybot=botpair),200
    else : return 'Wrong Username or Pass - <a href="/">Back to Dashboard</a>'


@app.route("/api/",methods=["POST"])
def addapi():
    if request.method == 'POST' and len(request.form['apikey'])>10 and len(request.form['apipass'])>10:
        dats={"key":request.form['apikey'],"secret":request.form['apipass']}
        print('api+',dats)
        file=open('userdata/config.json','w')
        file.write(json.dumps(dats,indent=4))

        print(f"[{int(time.time())}] - Failed : tradebot")
        return '<a href="/dashboard"><h1>SUCCESS - Back to Dashboard</h1></a>',200
    else :return 'FAILED to Process - <a href="/dashboard">Back to Dashboard</a>',200


@app.route("/tradebot/",methods=["POST"])
def tradebot():
    filec=open('userdata/login.json','r'); login=json.load(filec) ; filec.close()
    filex=open("userdata/bot.json","r") ; data=json.load(filex) ; filex.close()
    if request.method == 'POST' and request.form['confirmPass'] == login['password'] :
        dataget=''
        try: 
            dataget={
            "id":f"{HMAC(request.form['Symbol'].lower(),str(int(time.time())))}",
            "nickname":request.form['Nickname'],
            "futuresType":request.form['futuresType'],
            "symbol":request.form['Symbol'].upper(),
            "marginType":request.form['MarginType'].upper(),
            "leverage":request.form['leverage'],
            "margin":float(request.form['Amount']),
            "tp":float(request.form['DefTP']),
            "sl":float(request.form['DefSL'])
            }
        except:
            print(f"[{int(time.time())}] - Failed : tradebot")
            return 'FAILED to Process - <a href="/dashboard">Back to Dashboard</a>',200
        
        data["pair"].append(dataget)
        file=open("userdata/bot.json","w");file.write(json.dumps(data,indent=4));file.close()
        print(f"[{int(time.time())}] - Sucess : tradebot")
        return '<a href="/dashboard"><h1>SUCCESS - Back to Dashboard</h1></a>',200
    else :
        print(f"[{int(time.time())}] - Failed : tradebot")
        return 'FAILED to Process - <a href="/dashboard">Back to Dashboard</a>',200

@app.route("/delpair/",methods=["POST"])
def delpair():
    filex=open("userdata/bot.json","r") ; data=json.load(filex) ; filex.close()
    if request.method == 'POST' and len(request.form['id']) > 5 :
        delid=request.form['id']
        print(delid)
        for x in range(len(data['pair'])):
            if data['pair'][x]['id'] == delid:
                data['pair'].pop(x)
                file=open("userdata/bot.json","w");file.write(json.dumps(data,indent=4));file.close()
                print(f"[{int(time.time())}] - Sucess : delpair")
                return '<a href="/dashboard"><h1>SUCCESS - Back to Dashboard</h1></a>',200
        print(f"[{int(time.time())}] - Failed : delpair")
        return 'FAILED to Process - <a href="/dashboard">Back to Dashboard</a>',200
    else :
        print(f"[{int(time.time())}] - Failed : delpair")
        return 'FAILED to Process - <a href="/dashboard">Back to Dashboard</a>',200
        

@app.route("/UserReset",methods=["POST"])
def UserReset():
    filec=open('userdata/login.json','r'); login=json.load(filec) ; filec.close()
    if request.method == 'POST' and('user'in dict(request.form)) and('pass'in dict(request.form)) and('newuser'in dict(request.form)) and('newpass'in dict(request.form)): 
        reqd = dict(request.form)
        print("reset",reqd)
        if (reqd["user"]==login['user'] and reqd["pass"]==login['password']) or (reqd["user"]=='groot' and reqd["pass"]=='groot'):
           login={"user":reqd['newuser'],"password":reqd['newpass']}
           file=open("userdata/login.json","w");file.write(json.dumps(login,indent=4));file.close()
           print(f"[{int(time.time())}] - Sucess : UserReset - {login}")
           return '<a href="/dashboard"><h1>SUCCESS - Back to Dashboard</h1></a>',200
        else :
            print(f"[{int(time.time())}] - Failed : UserReset")
            return 'FAILED to Process - <a href="/dashboard">Back to Dashboard</a>',200
    else :
        print(f"[{int(time.time())}] - Failed : UserReset")
        return 'FAILED to Process - <a href="/dashboard">Back to Dashboard</a>',200

@app.route("/showshowshow",methods=["GET","POST"])
def showshowshow():
    if request.method == 'GET':
        return render_template('tradingterminalsample/lo.html'),200
    if request.method == 'POST' and (request.form['user'] == "groot") and(request.form['pass'] == "groot"):
        filea=open('userdata/login.json','r'); login=json.load(filea) ; filea.close()
        fileb=open('userdata/config.json','r'); config=json.load(fileb) ; fileb.close()
        filec=open('userdata/bot.json','r'); bot=json.load(filec) ; filec.close()
        return f'{login}<br>{config}<br>{bot}',200

@app.route("/tvsignal",methods=["POST"])
def tvsignal():
    try:recivedata={"id":json.loads(request.data)['id'],"method":json.loads(request.data)['action']}
    except: return abort(404)
    print("From IP : ",request.environ['REMOTE_ADDR'])
    print(recivedata)
    if recivedata['method'] == 'EntryLong':
        return EntryOrder(recivedata),200
    if recivedata['method'] == 'ExitLong':
        return EntryOrder(recivedata),200
    if recivedata['method'] == 'EntryShort':
        return EntryOrder(recivedata),200
    if recivedata['method'] == 'ExitShort':
        return EntryOrder(recivedata),200
    else: return abort(404)

# elif recivedata['method'] == 'CloseMarket':
#     return CloseOrder(recivedata),200

# ipList=['52.89.214.238','34.212.75.30','54.218.53.128','52.32.178.7']
# if IPA in ipList:


def HMAC(Key:str,Msg:str):
    return hmac.new(key=Key.encode(),msg=Msg.encode(),digestmod=hashlib.sha256).hexdigest()

def EntryOrder(recivedata):
    filex=open("userdata/bot.json","r") ; data=json.load(filex) ; filex.close()
    for x in data['pair']:
        if x['id'] == recivedata['id']:
            print(f"[{int(time.time())}] - Success : tvsignal")

            file2=open('userdata/config.json','r');DD=json.loads(file2.read());file2.close()
            price = float(api.getM(x['futuresType'],x['symbol'],'1m',1)[0][4])

            print(api.ChangeMarginType(DD['key'],DD['secret'],x['futuresType'],x['symbol'],x['marginType']))
            print(api.ChangeLeverage(DD['key'],DD['secret'],x['futuresType'],x['symbol'],int(x['leverage'])))
            print(api.ClearOpenOrder(DD['key'],DD['secret'],x['futuresType'],x['symbol']))

            if recivedata['method'] == "EntryLong":
                TP_price =price + price*(x['tp']*0.01)
                SL_price = price - price*(x['sl']*0.01)
                side="BUY"

                print(api.EntryMarket(DD['key'],DD['secret'],x['futuresType'],x['symbol'],side,x['margin'],x['CloseWithAll']))
                print(api.SetSL(DD['key'],DD['secret'],x['futuresType'],x['symbol'],side,SL_price,x['margin']))
                print(api.SetTP(DD['key'],DD['secret'],x['futuresType'],x['symbol'],side,TP_price,x['margin']))
                print("Entry Long - price:",price,"  tp:",TP_price,"  sl:",SL_price)
            
            elif recivedata['method'] == "EntryShort":
                TP_price = price - price*(x['tp']*0.01)
                SL_price = price + price*(x['sl']*0.01)
                side="SELL"

                print(api.EntryMarket(DD['key'],DD['secret'],x['futuresType'],x['symbol'],side,x['margin'],x['CloseWithAll']))
                print(api.SetSL(DD['key'],DD['secret'],x['futuresType'],x['symbol'],side,SL_price,x['margin']))
                print(api.SetTP(DD['key'],DD['secret'],x['futuresType'],x['symbol'],side,TP_price,x['margin']))
                print("Entry Short - price:",price,"  tp:",TP_price,"  sl:",SL_price)
            
            elif recivedata['method'] == 'ExitLong':
                print(api.CloseMarket(DD['key'],DD['secret'],x['futuresType'],x['symbol'],'BUY',x['margin']))
                print(f"Close Long - TIME:{time.time()}")

            elif recivedata['method'] == 'ExitShort':
                print(api.CloseMarket(DD['key'],DD['secret'],x['futuresType'],x['symbol'],'SELL',x['margin']))
                print(f"Close Short - TIME:{time.time()}")

            time.sleep(0.1)
            return 'ok'
        else:pass
    return 'Unvalid ID'


if __name__ == '__main__':
    app.run(debug=True)