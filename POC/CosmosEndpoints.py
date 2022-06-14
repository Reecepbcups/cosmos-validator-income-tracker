from wsgiref.validate import validator
import requests

API_LINK = ""
headers = {'accept': 'application/json'}
PAGE_LIMIT = "&pagination.limit=1000"

def getOutstandingRewards(valop: str, humanReadable = True) -> dict:
    response = requests.get(f'https://api.cosmos.network/cosmos/distribution/v1beta1/validators/{valop}/outstanding_rewards', headers=headers)

    data = {}
    rewards = response.json()['rewards']['rewards']
    for r in rewards:
        denom = r['denom']
        amt = r['amount']
        if humanReadable:
            if denom.startswith('u'):
                denom = denom[1:]
                amt = float(amt) / 1_000_000        
        data[denom] = amt
    return data

import json
def getLatestValidatorSet(bondedOnly: bool = True):
    from poc import r # imports redis instance for when we need it
    
    link = 'https://api.cosmos.network/cosmos/staking/v1beta1/validators?'
    if bondedOnly: link += 'status=BOND_STATUS_BONDED'
    validators = {}
    
    k = "latestvalset"
    latestVals = r.get(k) 
    
    if latestVals != None:
        print("Loaded val set from cache")
        return json.loads(latestVals.decode('utf-8'))
    
    response = requests.get(link + PAGE_LIMIT, headers=headers).json()
    for val in response['validators']:
        opp_addr = val['operator_address']
        moniker = val['description']['moniker']
        identity = val['description']['identity']
        status = val['status']
        validators[opp_addr] = {'moniker': moniker, 'identity': identity, "status": status}

    print("Set val set to cache for 3600 seconds")
    r.set(k, json.dumps(validators), ex=3600)    

    return validators

    



if __name__ == '__main__':
    print(getLatestValidatorSet(True))