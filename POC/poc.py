import requests
import json
from CosmosEndpoints import getLatestValidatorSet, getOutstandingCommissionRewards, getTxsAtHeight
import redis

headers = {'accept': 'application/json'}

'''
Solution:
+ We get the val set, and get bonded validators. (Redis cache this, recheck every 60 minutes?)
'''

INITIAL_HEIGHT = 10449274 # height sg-1 withdrew comission
 



# load redis
r = redis.Redis(host="localhost", port=6379, db=0)





def getTxsByHeight(height: int):
    '''
    Loop through all blocks, get all txs, see if they are a match delegator reward
    '''

    Txs = []
    allTxs = getTxsAtHeight(height)
    for msg in allTxs['body']['messages']:
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
            outstandingRewards = getOutstandingCommissionRewards(valKey)
            r.set(k, json.dumps(outstandingRewards), ex=3600)
        else:
            outstandingRewards = json.loads(outstandingRewards.decode('utf-8'))
            fromRedis = True


        print(valKey, validators.get(valKey)['moniker'], outstandingRewards, f"{fromRedis=}")         
        # exit()
        




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