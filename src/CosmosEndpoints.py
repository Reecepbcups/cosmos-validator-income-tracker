import requests

# NO REDIS THINGS IN HERE

REST_ENDPOINT = "https://api.cosmos.network"
# REST_ENDPOINT = "https://lcd.cosmos.ezstaking.io"
headers = {'accept': 'application/json'}
PAGE_LIMIT = "&pagination.limit=1000"

# https://v1.cosmos.network/rpc/v0.45.1

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



if __name__ == '__main__':
    print(getLatestValidatorSet(True))