
import requests  
headers = {'accept': 'application/json'}

'''
The thing is, we dont need to query the actual tx claim amount, just that they did
which we can meassure from the last time we queried until the time they withdrew.
'''

def getTxDetails(txHash: str):
    # this def needs more work
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




def getDocuments():
    '''Get mongodb documents from a collection in order based on the time field (epoch)'''
    # latest documents first
    documents = m.client[db]['atom'].find().sort(key_or_list='time', direction=-1)
    # for doc in documents:
    #   epoch = doc.get("time")
    #   commissions = doc.get("commissions")
    #   print(epoch, commissions, "\n'")
    # if time is older than 1 day, we move to the 1 day collection I guess?
    return documents