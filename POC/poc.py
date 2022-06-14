import requests
headers = {'accept': 'application/json'}

'''
Solution:
- We get the val set, and get bonded validators. (Redis cache this, recheck every 60 minutes?)
- Update their amount of held amount of commission, if it is lower, we need to see when they withdrew it:
    - get the last time we checked validators, and get the block height. Get latest block height. Loop through all blocks, get all txs which match withdrawing reward.
    - Once we find the block, get the previous block, see how much rewards they had.


Coin Gecko:
- Query coingeko for token price. Redis cache every 1 hour.
'''


# https://v1.cosmos.network/rpc/v0.45.1

INITIAL_HEIGHT = 10449274 # height sg-1 undelegated

# get latest blocks (6 seconds)
# loop through and see if /cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward is in there


# 

# outstanding rewards
# curl -X GET "https://api.cosmos.network/cosmos/distribution/v1beta1/validators/cosmosvaloper196ax4vc0lwpxndu9dyhvca7jhxp70rmcvrj90c/outstanding_rewards" -H "accept: application/json"
import json

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



            #     for event in log:

            #         if event['type'] == "coin_received":
            #             for attr in event['attributes']:
            #                 if attr['key'] == "amount":
            #                     receivedCommission = attr['value']
            #                 elif attr['key'] == "receiver":
            #                     receiverAddr = attr['value']

            #         elif event['type'] == "message":
            #             for attr in event['attributes']:
            #                 if attr['key'] == "action" and attr['value'] == "/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward":
            #                     wasWithdraw = True
                            
            #         if wasWithdraw and len(receivedCommission) > 0:
            #             break
            # print(f"{delegator_address} {validator_address} {timestamp} {receiverAddr} {receivedCommission}")



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


def getLatestBlockHeight() -> int: # anytime we query all validators balances, we also save this to cache
    response = requests.get('https://api.cosmos.network/blocks/latest', headers=headers).json()
    return int(response['block']['header']['height'])


if __name__ == '__main__':
    # print(getLatestBlockHeight())
    getTxDetails('FC8431ACA7444B87DD1DDE14E7FB7BB1BD0BC314B443325DE1268CE362636247')
    pass