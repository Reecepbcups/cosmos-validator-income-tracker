import requests
import json
from CosmosEndpoints import getLatestValidatorSet, getOutstandingCommissionRewards
import redis

headers = {'accept': 'application/json'}

'''
Solution:
+ We get the val set, and get bonded validators. (Redis cache this, recheck every 60 minutes?)



Coin Gecko:
- Query coingeko for token price. Redis cache every 1 hour.
'''

INITIAL_HEIGHT = 10449274 # height sg-1 withdrew comission
 



# load redis
r = redis.Redis(host="localhost", port=6379, db=0)

def getTxDetails(txHash: str):
    '''
    Before running this function, we should have already looped through all validators & got their held tokens. 
        If new held < previous held, we need to loop through blocks since last time we checked
    
    '''
    link = f'https://api.cosmos.network/cosmos/tx/v1beta1/txs/{txHash}'
    response = requests.get(link, headers=headers).json()
    
    print(link)
    messages = list(response['tx']['body']['messages'])

    # print(len(messages), len(log_events)); # exit()

    for msg in messages:
        if msg['@type'] != '/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission':
            # print("Skipping " + msg['@type'])
            continue

        # delegator_address = msg['delegator_address']
        # validator_address = msg['validator_address']
        # timestamp = msg['tx_response']['timestamp'] # 2022-05-11T13:23:20Z
        
        receiverAddr = ""
        receiverValAddr = ""
        receivedCommission = "" # 99044465uatom
        wasWithdraw = False
        
        j = json.loads(response['tx_response']['raw_log'])
        isWithdrawCommission = False
        for m in j:
            for k in m['events']:
                t = k['type'] # coin_received, coin_spent, message, transfer
                if t == 'message':
                    for attr in list(k['attributes']):
                        # print(attr['value'])
                        if attr['key'] == 'action' and attr['value'] == '/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission':
                            isWithdrawCommission = True
                        elif attr['key'] == 'sender':
                            addr = attr['value']
                            if 'valop' in addr:
                                receiverValAddr = addr
                            else:
                                receiverAddr = addr
                elif (t == 'transfer' or t == "coin_received") and isWithdrawCommission:
                    for attr in list(k['attributes']):
                        if attr['key'] == 'amount':
                            receivedCommission = attr['value']
                        elif attr['key'] == 'receiver':
                            receiverAddr = attr['value']


                            

                        
        print('MsgWithdrawValidatorCommission', isWithdrawCommission, receiverAddr, receiverValAddr, receivedCommission)                    
        exit()



def getTxsByHeight(height: int):
    '''
    Loop through all blocks, get all txs, see if they are a match delegator reward
    '''
    params = {
        'events': f'tx.height={height}',
        'order_by': 'ORDER_BY_UNSPECIFIED',
    }
    Txs = []
    response = requests.get('https://api.cosmos.network/cosmos/tx/v1beta1/txs', params=params, headers=headers).json()
    for tx in response['txs']:        
        for msg in tx['body']['messages']:
            if msg['@type'] == '/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission':
                valAddr = msg['validator_address']
                delAddr = msg['delegator_address']
                Txs.append({'valAddr': valAddr, 'delAddr': delAddr})
                # If they do this, we need to get their commission BEFORE they withdrew it (height-1)
                break

    print(Txs)
    exit(1)



import json


def getAllValidatorsOutstandingRewards(fromCache=True):    
    if fromCache == False:
        validators = getLatestValidatorSet(True)
    else: # get from cache          
        k = "latestvalset"
        latestVals = r.get(k) 
        if latestVals != None:
            print("Loaded val set from cache")
            validators = json.loads(latestVals.decode('utf-8'))

        r.set(k, json.dumps(validators), ex=3600)
        

    for valKey in validators.keys():
        k = f"commission:{valKey}"        
        outstandingRewards = r.get(k)
        fromRedis = False

        if outstandingRewards is None:
            outstandingRewards = getOutstandingRewards(valKey)
            r.set(k, json.dumps(outstandingRewards), ex=3600)
        else:
            outstandingRewards = json.loads(outstandingRewards.decode('utf-8'))
            fromRedis = True


        print(valKey, validators.get(valKey)['moniker'], outstandingRewards, f"{fromRedis=}")         
        # exit()
        
import re
def compareOutstandingRewards():
    rewards = {}
    '''
    - Update their amount of held amount of commission, if it is lower, we need to see when they withdrew it:
    - get the last time we checked validators, and get the block height. Get latest block height. Loop through all blocks, get all txs which match withdrawing reward.
    - Once we find the block, get the previous block, see how much rewards they had.
    '''
    # get latest rewards commissions, compare from the previous rewards.
    # if they are lower, we have to scan all blocks & txs since last query & find where they withdrew
    # if they are higher, we just append {"currentTime": amountGained} to their value

    cachedRewards = getAllValidatorsOutstandingRewards(fromCache=True)
    # currentRewards = getAllValidatorsOutstandingRewards(fromCache=False)

    

    # re.sub('\D', '', 'aas30dsa20') # removes all letters from string

    # save latest block height to redis
    pass


def getLatestBlockHeight() -> int: # anytime we query all validators balances, we also save this to cache
    response = requests.get('https://api.cosmos.network/blocks/latest', headers=headers).json()
    return int(response['block']['header']['height'])

import time
if __name__ == '__main__':
    # print(getLatestBlockHeight())
    # getTxDetails('FC8431ACA7444B87DD1DDE14E7FB7BB1BD0BC314B443325DE1268CE362636247')


    # getAllValidatorsOutstandingRewards()
    # compareOutstandingRewards()

    acc = 'cosmosvaloper1uepjmgfuk6rnd0djsglu88w7d0t49lmljdpae2'
    token = "atom"
    secondsSinceQuery = 25

    outstanding = getOutstandingCommissionRewards(acc, True).get(token)
    print(outstanding)
    time.sleep(secondsSinceQuery)
    
    n2 = getOutstandingCommissionRewards(acc, True).get(token)
    print(n2)

    print(f"{acc} gained:", n2-outstanding, token, f" in the last {secondsSinceQuery} seconds")



    pass