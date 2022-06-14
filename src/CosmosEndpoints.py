import requests

# NO REDIS IN HERE

REST_ENDPOINT = "https://api.cosmos.network"
# REST_ENDPOINT = "https://lcd.cosmos.ezstaking.io"
headers = {'accept': 'application/json'}
PAGE_LIMIT = "&pagination.limit=1000"

# https://v1.cosmos.network/rpc/v0.45.1


'''
https://github.com/cosmos/cosmos-sdk/blob/main/docs/core/events.md < docs on events
Looks like I could subscribe via RPC
'''

def getOutstandingCommissionRewards(valop: str, humanReadable = True) -> dict:
    # I assume /outstanding_rewards is their commission AND their self bonded rewards? Look into API
    response = requests.get(f'{REST_ENDPOINT}/cosmos/distribution/v1beta1/validators/{valop}/commission', headers=headers)
    print(f'{REST_ENDPOINT}/cosmos/distribution/v1beta1/validators/{valop}/commission')

    data = {}
    rewards = response.json()['commission']['commission'] # /outstanding_rewards is 'rewards' 'rewards'
    for r in rewards:
        denom = r['denom']
        amt = r['amount']
        if humanReadable:
            if denom.startswith('u'):
                denom = denom[1:]
                amt = float(amt) / 1_000_000        
        data[denom] = amt
    return data


def getLatestBlockHeight() -> int:
    response = requests.get('https://api.cosmos.network/blocks/latest', headers=headers).json()
    return int(response['block']['header']['height'])
    

def getLatestBlockTransactions(block: str = "latest") -> list:
    l = f'https://api.cosmos.network/blocks/{block}'
    print(l)
    response = requests.get(l, headers=headers).json()
    return response['block']['data']['txs']


def getLatestValidatorSet(bondedOnly: bool = True):    
    link = f'{REST_ENDPOINT}/cosmos/staking/v1beta1/validators?'
    if bondedOnly: link += 'status=BOND_STATUS_BONDED'
    validators = {}

    response = requests.get(link + PAGE_LIMIT, headers=headers).json()
    for val in response['validators']:
        opp_addr = val['operator_address']
        moniker = val['description']['moniker']
        identity = val['description']['identity']
        status = val['status']
        validators[opp_addr] = {'moniker': moniker, 'identity': identity, "status": status}
       
    return validators


def getValidatorSlashes(valop: str) -> list:
    response = requests.get(f'{REST_ENDPOINT}/cosmos/distribution/v1beta1/validators/{valop}/slashes').json()
    return response['slashes']


# More specific
def getTxsAtHeight(height: int, msgType: str = ""):
    params = {
        'events': f'tx.height={height}',
        'order_by': 'ORDER_BY_UNSPECIFIED',
    }
    response = requests.get('https://api.cosmos.network/cosmos/tx/v1beta1/txs', params=params, headers=headers).json()
    if len(msgType) == 0:
        return response['txs']
    
    TxsWeWant = [] # from poc.py getTxsByHeight(
    for msg in response['txs']['body']['messages']:
        if msg['@type'] == msgType:
            TxsWeWant.append(msg)


def getTxEvents(height: int, key = "txs"): # or tx_responses
    params = {
    'events': [
        f'tx.height={height}',
        'message.module=\'distribution\'',
    ],
    'order_by': 'ORDER_BY_UNSPECIFIED',
    }
    # curl -X GET "https://api.cosmos.network/cosmos/tx/v1beta1/txs?events=tx.height%3D10449274&events=message.module%3D'distribution'&order_by=ORDER_BY_UNSPECIFIED" -H "accept: application/json"
    return requests.get('https://api.cosmos.network/cosmos/tx/v1beta1/txs', params=params, headers=headers).json()[key]


if __name__ == '__main__': 
    # print(getLatestValidatorSet(True))
    # txs = getLatestBlockTransactions("10449274")
    # import base64
    # for t in txs:
    #     t = base64.b64decode(t)

    #     if b'/cosmos.distribution.v1beta1.MsgWithdrawcValidatorCommission' in t:
    #         print(t)
    #         print()


    # This is not even required bc we know how much they withdrew since we grab the commissions
    # tx = getTxEvents(10449274, 'tx_responses')
    # for t in tx:
    #     print(t['raw_log'])
    #     body = t['body']
    #     messages = body['messages']
    #     for msg in messages:
    #         if msg['@type'] == '/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission':
    #             print(msg)

    pass