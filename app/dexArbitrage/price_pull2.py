# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# ### Have to do this for it to work in 1.9.x!
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()


from websocket import create_connection, WebSocketApp
import json
from .models import Pair, Deals
import time
from datetime import timedelta
import collections
from django.utils import timezone
import itertools
from threading import Thread
# from .tasks import dealWork


def get_pages(tz, net, exch, user_agent):
    ws = create_connection(f"wss://io.dexscreener.com/dex/screener/pairs/{tz}/1?filters[chainIds][0]={net}&filters[dexIds][0]={exch}",header=[user_agent])
    while True:
        result =  ws.recv()
        if "ping" in result:
            ws.send(json.dumps("pong"))
            continue
        
        result = json.loads(result)
        total_pairs = result.get('pairsCount')
        if total_pairs==0:
            return
        if not total_pairs:
            continue
        
        ws.close()
        break
    return total_pairs




def update_price():
    objs = Pair.objects.all()
    if objs:
        tz = "m5"
    else:
        tz = "h24"
    init_time = time.time()
    exchanges = {
    "ethereum" : ["uniswap","sushiswap","balancer","defiswap",'shibaswap','swapr'],
    "bsc": ["pancakeswap","kyberswap","balancer","apeswap","bakeryswap",'mdex','biswap']}

    custom_protocol = "CVuC1pc5IFbH1RtiLtgWBA=="
    protocol_str = "Sec-WebSocket-Key: " + custom_protocol

    user_agent = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    for net in list(exchanges.keys()):
        
        for exch in exchanges[net]:
            # process_socket(net, exch, 1, user_agent, tz)
            total_pairs = get_pages(tz, net, exch, user_agent)
            print(f"Exhcnage: {exch} | Pairs: {total_pairs}")
            if not total_pairs:
                continue
            if int(total_pairs)>100:
                remaining_pages = int(total_pairs)/100
                if int(remaining_pages)<int(total_pairs)/100:
                    remaining_pages = int(int(total_pairs)/100) + 1
                else:
                    remaining_pages = int(int(total_pairs)/100) 

            if remaining_pages>1:
                if remaining_pages>7:
                    remaining_pages = 7
                for i in range(remaining_pages-1):
                    process_socket(net, exch, i+1, user_agent, tz)
            else:
                process_socket(net, exch, 1, user_agent, tz)
    print(time.time()-init_time)

def process_socket(net,exch,pg,user_agent,tz):
    def on_connection(ws):
        print(f"Connected to {exch} | {pg}")

    def on_error(ws,error):
        print(f"Error connecting to {exch} | {pg} | {error}")
        try:
            ws.close()
        except:
            pass
        process_socket(net,exch,pg,user_agent,tz)

    def on_message(ws, message):
        result =  message
        print(f"Message Received: {exch} | {pg}")
        if "ping" in result:
            ws.send(json.dumps("pong"))
            return
        
        result = json.loads(result)
        total_pairs = result.get('pairsCount')
        if total_pairs==0:
            return
        if not total_pairs:
            return
    
        for pair in result['pairs']:
            base_token = pair['baseToken']
            quote_token = pair['quoteToken']
            liquidity = pair.get('liquidity')
            pr =pair['price'].replace(',','')
            prusd =  pair.get('priceUsd')
            if prusd:
                prusd = prusd.replace(',','')
            if liquidity:
                liquidity = liquidity.get('usd')
            try:
                Pair.objects.update_or_create(
                            name=base_token['name'],
                            baseAsset = base_token['symbol'],
                            quoteAsset = quote_token['symbol'],
                            symbol = f"{base_token['symbol']}/{quote_token['symbol']}",
                            exchange = exch,
                            network = net,
                            defaults = {'price' : pr,
                            "priceUSD" : prusd,
                            "liquidity" : liquidity}
                        )
            except:
                pass
    
        process_data()
        return
    
    url = f"wss://io.dexscreener.com/dex/screener/pairs/{tz}/{pg}?filters[chainIds][0]={net}&filters[dexIds][0]={exch}"
    
    ws = WebSocketApp(
            url,
            header=[user_agent],
            on_open=on_connection,
            on_message=on_message,
            on_error=on_error)
    ws_worker_thread = Thread(
                            target=ws.run_forever)
    ws_worker_thread.daemon = True
    ws_worker_thread.start() 
    

def get_percent(num1, num2):
    if num1 == 0 and num2 == 0:
        return 0
    if num1 < num2:
        return 100 - (num1 / num2 * 100)
    else:
        return 100 - (num2 / num1 * 100)       

def process_data():
    time = timezone.now() - timedelta(minutes=3)
    data = Pair.objects.filter(updated__gte=time)
    done_symbols = [d.symbol for d in data]
    opps = [item for item, count in collections.Counter(done_symbols).items() if count > 1]
    for sym in opps:
        subset = (data.filter(symbol=sym))
        for comb in itertools.combinations(subset,2):
            if comb[0].name==comb[1].name:
            # print(comb)
                pct = get_percent(comb[0].price,comb[1].price)
                if pct>5:
                    
                    if comb[0].price<comb[1].price:
                        buy = comb[0]
                        sell = comb[1]
                    else:
                        buy = comb[1]
                        sell = comb[0]
                    Deals.objects.create(
                        dealPair1=buy,
                        dealPair2=sell,
                        percentChange=pct
                    )
    return