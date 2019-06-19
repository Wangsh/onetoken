import time
import json
import urllib.parse
import hmac
import hashlib
import requests
class Secret:
    ot_key = ''
    ot_secret = ''


def gen_nonce():
    return str(int(time.time() * 1000000))


"""
def gen_sign(secret, verb, endpoint, nonce, data_str):
    # Parse the url so we can remove the base and extract just the path.

    if data_str is None:
        data_str = ''

    parsed_url = urlparse(endpoint)
    path = parsed_url.path

    # print "Computing HMAC: %s" % verb + path + str(nonce) + data
    message = verb + path + str(nonce) + data_str

    if py3:
        signature = hmac.new(bytes(secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    else:
        signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return signature
"""

def api_call(method, endpoint, params=None, data=None, timeout=15, host='https://1token.trade/api/v1/trade'):
    assert params is None or isinstance(params, dict)
    assert data is None or isinstance(data, dict)
    method = method.upper()

    nonce = gen_nonce()

    url = host + endpoint

    json_str = json.dumps(data) if data else None
    sign = gen_sign(Secret.ot_secret, method, endpoint, nonce, json_str)
    headers = {'Api-Nonce': str(nonce), 'Api-Key': Secret.ot_key, 'Api-Signature': sign,
               'Content-Type': 'application/json'}
    res = requests.request(method, url=url, data=json_str, params=params, headers=headers, timeout=timeout)
    return res


def demo(account):
    print('查看账户信息')
    r = api_call('GET', '/{}/info'.format(account))
    print(r.json())

    print('撤销所有订单')
    r = api_call('DELETE', '/{}/orders/all'.format(account))
    print(r.json())

    print('下单')
    r = api_call('POST', '/{}/orders'.format(account),
                 data={'contract': 'okex/btc.usdt', 'price': 10, 'bs': 'b', 'amount': 1, 'options': {'close': True}})
    print(r.json())
   # assert r.json()['client_oid']
   # exg_oid = r.json()['exchange_oid']

    time.sleep( 3 )
    print('查询挂单 应该有一个挂单')
    r = api_call('GET', '/{}/orders'.format(account))
    print(r.json())
    #assert len(r.json()) == 1

    print('用 exchange oid撤单')
    r = api_call('DELETE', '/{}/orders'.format(account), params={'exchange_oid': exg_oid})
    print(r.json())

    time.sleep(3)
    print('查询挂单 应该没有挂单')
    r = api_call('GET', '/{}/orders'.format(account))
    print(r.json())
    assert len(r.json()) == 0


# 填入你的ot_key
ot_key = '-----'
# 填入你的ot_secret
ot_secret = '-----'

def gen_nonce():
    return str((int(time.time() * 1000000)))


def gen_headers(nonce, key, sig):
    headers = {
        'Api-Nonce': nonce,
        'Api-Key': key,
        'Api-Signature': sig,
        'Content-Type': 'application/json'
    }
    return headers


def gen_sign(secret, verb, path, nonce, data=None):
    if data is None:
        data_str = ''
    else:
    #    assert isinstance(data, dict)
        # server并不要求data_str按key排序，只需此处用来签名的data_str和所发送请求中的data相同即可，是否排序请按实际情况选择
         data_str = json.dumps(data, sort_keys=True)
    parsed_url = urllib.parse.urlparse(path)
    parsed_path = parsed_url.path

    message = verb + parsed_path + str(nonce) + data_str
    signature = hmac.new(bytes(secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    print('nonce:', nonce)
    print('parsed_path:', parsed_path)
    print('data_str:', data_str)
    print('message:', message)
    return signature


def place_order(price,count):
    verb = 'POST'

    # 下单的api前缀如下，具体请查看1token API文档
    url = 'https://1token.trade/api/v1/trade'

    # path的具体构成方法请查看1token API文档
    path = '/okex/mock-wsh2/orders'

    nonce = gen_nonce()
    data = {"contract": "okex/eos.usdt", "price": price, "bs": "b", "amount": count}
    sig = gen_sign(ot_secret, verb, path, nonce, data)
    headers = gen_headers(nonce, ot_key, sig)
    # server并不要求请求中的data按key排序，只需所发送请求中的data与用来签名的data_str和相同即可，是否排序请按实际情况选择
    resp = requests.post(url + path, headers=headers, data=json.dumps(data, sort_keys=True))
    print(resp.json())
def place_order1(price,count):
    verb = 'POST'

    # 下单的api前缀如下，具体请查看1token API文档
    url = 'https://1token.trade/api/v1/trade'

    # path的具体构成方法请查看1token API文档
    path = '/okex/mock-wsh2/orders'

    nonce = gen_nonce()
    data = {"contract": "okex/eos.usdt", "price": price, "bs": "s", "amount": count}
    sig = gen_sign(ot_secret, verb, path, nonce, data)
    headers = gen_headers(nonce, ot_key, sig)
    # server并不要求请求中的data按key排序，只需所发送请求中的data与用来签名的data_str和相同即可，是否排序请按实际情况选择
    resp = requests.post(url + path, headers=headers, data=json.dumps(data, sort_keys=True))
    print(resp.json())

def get_info():
    verb = 'GET'
    url = 'https://1token.trade/api/v1/trade'
    path = '/okex/mock-wsh2/info'
    nonce = gen_nonce()
    sig = gen_sign(ot_secret, verb, path, nonce)
    headers = gen_headers(nonce, ot_key, sig)
    resp = requests.get(url + path, headers=headers)
    print(resp.json())
def eos_usdt_usdk_price():
    res = requests.get('https://1token.trade/api/v1/quote/single-tick/okex/eos.usdt')
    #pprint(res.json(), width=1000)

    #卖一价
    eos_usdt_ask = res.json()['asks'][0]['price']
    #print('eos_usdt_ask:',eos_usdt_ask)

    #买一价
    eos_usdt_bid = res.json()['bids'][0]['price']
    #print('eos_usdt_bid:',eos_usdt_bid)

    res = requests.get( 'https://1token.trade/api/v1/quote/single-tick/okex/eos.usdk' )
    #pprint(res.json(), width=1000)

    #卖一价
    eos_usdk_ask = res.json()['asks'][0]['price']
    #print('eos_usdk_ask:',eos_usdk_ask)

    #买一价
    eos_usdk_bid = res.json()['bids'][0]['price']
    #print('eos_usdk_bid:',eos_usdk_bid)


    res = requests.get( 'https://1token.trade/api/v1/quote/single-tick/okex/usdt.usdk' )
    #pprint(res.json(), width=1000)

    #卖一价
    usdt_usdk_ask = res.json()['asks'][0]['price']
    #print('usdt_usdk_ask:',usdt_usdk_ask)

    #买一价
    usdt_usdk_bid = res.json()['bids'][0]['price']
    #print('usdt_usdk_bid:',usdt_usdk_bid)

    eos_usdt_usdk_eos = eos_usdt_bid * usdt_usdk_bid /eos_usdk_ask / 1.0002/1.0002/1.0002
    eos_usdk_usdt_eos = eos_usdk_bid / usdt_usdk_ask / eos_usdt_ask / 1.0002/1.0002/1.0002

    if eos_usdt_usdk_eos >= 1:
        print( 'eos_usdt_usdk_eos', eos_usdt_usdk_eos )

        print( '下单' )
        r = api_call( 'POST', '/{}/orders'.format( account ),
                      data={'contract': 'okex/eos.usdt', 'price': eos_usdt_bid, 'bs': 's', 'amount': 10,
                            'options': {'close': False}} )
        #print( r.json() )

        r = api_call( 'POST', '/{}/orders'.format( account ),
                      data={'contract': 'okex/usdt.usdk', 'price': usdt_usdk_bid, 'bs': 's', 'amount': 10*eos_usdt_bid,
                            'options': {'close': False}} )
        print( r.json() )

        r = api_call( 'POST', '/{}/orders'.format( account ),
                      data={'contract': 'okex/eos.usdk', 'price': eos_usdk_ask, 'bs': 'b', 'amount': 10*eos_usdt_bid/eos_usdk_ask,
                            'options': {'close': False}} )
        print( r.json() )

    elif eos_usdk_usdt_eos>=1:
        print( 'eos_usdk_usdt_eos', eos_usdk_usdt_eos )

        print( '下单' )
        r = api_call( 'POST', '/{}/orders'.format( account ),
                      data={'contract': 'okex/eos.usdk', 'price': eos_usdk_bid, 'bs': 's', 'amount': 10,
                            'options': {'close': False}} )
        #print( r.json() )

        r = api_call( 'POST', '/{}/orders'.format( account ),
                      data={'contract': 'okex/usdt.usdk', 'price': usdt_usdk_ask, 'bs': 'b',
                            'amount': 10 * usdt_usdk_ask,
                            'options': {'close': False}} )
        #print( r.json() )

        r = api_call( 'POST', '/{}/orders'.format( account ),
                      data={'contract': 'okex/eos.usdk', 'price': eos_usdk_ask, 'bs': 'b',
                            'amount': 10 * usdt_usdk_ask / eos_usdt_ask,
                            'options': {'close': False}} )
        #print( r.json() )
def GetNowTime():
    return time.time()
def GetNowUsd():
    res = requests.get('https://1token.trade/api/v1/quote/single-tick/okex/eos.usdt')
    print(res.json())
    return res.json()['last']
def Buy(price,count):
    place_order(price,count)
def Sell(price,count):
    place_order1(price,count)


def main():
    #place_order()
    #get_info()
    # ot_key = input('ot-key: ')
    #ot_secret = input('ot-secret: ')
   # account = input('请输入交易账号 账号格式是 {交易所}/{交易账户名} 比如 okex/mock-1token: ')
    Secret.ot_key = ot_key
    Secret.ot_secret = ot_secret

    account = 'okex/mock-wsh2'

   # demo(account)
    #while
    starttime = GetNowTime()

    buytime = GetNowTime()
    selltime = GetNowTime()
    lastcheck = GetNowTime()
    curusd=0.000001
    lastusd = 10
    print ("starttime:%s" % starttime)
    bs_state=0
    print("bs_state:%s" % bs_state)
    while True:
        nowtime= GetNowTime()
        #如果时间满足
        if bs_state== 0:
            #
            if (nowtime - lastcheck) > 3:
                # 获取当前价格
                print("start buy caculate")
                curusd = GetNowUsd()
                print("Now price:",curusd)
                if (curusd < lastusd-0.005):
                    Buy(curusd+0.001,10)
                    lastusd=curusd+0.001
                    print("bus success")
                    bs_state = 1
        else:
            if (nowtime-lastcheck)>3:
                #获取当前价格
                print("start shell caculate")
                curusd=GetNowUsd()
                print("Now price:", curusd)
                if(curusd>lastusd+0.005):
                    Sell(curusd-0.001,10)
                    lastusd = curusd - 0.001
                    print("sell success")
                    bs_state = 0



if __name__ == '__main__':
    main()