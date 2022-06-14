import requests

'''
Queries all token prices, caches for 1 hour
'''

tokens = 'osmosis,cosmos,juno-network,evmos,secret,akash-network,regen,sentinel,iris-network,starname,e-money,e-money-eur,likecoin,bitcanna,comdex,cheqd-network,vidulum,sifchain,band-protocol,decentr,switcheo,cerberus-2,fetch-ai,neta,terra-krw,ethereum,frax,provenance-blockchain,rizon,injective-protocol,chainlink,maker'.split(",")
priceTTL = 60*60

def getPrice(coin: str) -> float:
    from main import r

    coin = coin.lower()
    if coin not in tokens:
        return Exception(f"Invalid coin: {coin}")

    k = f"price:{coin}"
    price = r.get(k)

    # Query coingecko if we do not have the price cached, then save to cache.
    if price is None:
        url=f'''https://api.coingecko.com/api/v3/simple/price?ids={','.join(tokens)}&vs_currencies=usd'''
        coinData = requests.get(url).json()
        for cName in coinData:
            k = f"price:{cName}"
            usd = coinData[cName]['usd']
            r.set(k, usd, ex=priceTTL)
            # print("Set", k, "to cache for 3600 seconds")            
        price = r.get(k)
        print(f"From redis {k} = {price}")
              
    return float(price.decode('utf-8'))

if __name__ == '__main__':
    print(getPrice('juno-network'))