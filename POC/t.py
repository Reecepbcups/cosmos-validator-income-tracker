# This is just an example Tx from a tx query
# This is so we can check for /cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission action event

# https://docs.cosmos.network/master/modules/distribution/06_events.html#beginblocker

v = {'events': [
    {'type': 'coin_received', 'attributes': [
        {'key': 'receiver', 'value': 'cosmos196ax4vc0lwpxndu9dyhvca7jhxp70rmcfhxsrt'}, 
        {'key': 'amount', 'value': '99044465uatom'}
    ]}, 
    
    {'type': 'coin_spent', 'attributes': [
        {'key': 'spender', 'value': 'cosmos1jv65s3grqf6v6jl3dp4t6c9t9rk99cd88lyufl'}, 
        {'key': 'amount', 'value': '99044465uatom'}
    ]}, 
    {'type': 'message', 'attributes': [
            {'key': 'action', 'value': '/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward'}, 
            {'key': 'sender', 'value': 'cosmos1jv65s3grqf6v6jl3dp4t6c9t9rk99cd88lyufl'}, 
            {'key': 'module', 'value': 'distribution'}, 
            {'key': 'sender', 'value': 'cosmos196ax4vc0lwpxndu9dyhvca7jhxp70rmcfhxsrt'}
    ]}, 
    {'type': 'transfer', 'attributes': [
        {'key': 'recipient', 'value': 'cosmos196ax4vc0lwpxndu9dyhvca7jhxp70rmcfhxsrt'}, 
        {'key': 'sender', 'value': 'cosmos1jv65s3grqf6v6jl3dp4t6c9t9rk99cd88lyufl'}, 
        {'key': 'amount', 'value': '99044465uatom'}
    ]}, 
    {'type': 'withdraw_rewards', 'attributes': [
        {'key': 'amount', 'value': '99044465uatom'}, 
        {'key': 'validator', 'value': 'cosmosvaloper196ax4vc0lwpxndu9dyhvca7jhxp70rmcvrj90c'}
    ]}
]}

{
    'msg_index': 1, 
    'events': [
        {'type': 'coin_received', 'attributes': [
            {'key': 'receiver', 'value': 'cosmos196ax4vc0lwpxndu9dyhvca7jhxp70rmcfhxsrt'}, 
            {'key': 'amount', 'value': '2981065787uatom'}
        ]}, 
        {'type': 'coin_spent', 'attributes': [
            {'key': 'spender', 'value': 'cosmos1jv65s3grqf6v6jl3dp4t6c9t9rk99cd88lyufl'}, 
            {'key': 'amount', 'value': '2981065787uatom'}
        ]}, 
        {'type': 'message', 'attributes': [
                {'key': 'action', 'value': '/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission'}, 
                {'key': 'sender', 'value': 'cosmos1jv65s3grqf6v6jl3dp4t6c9t9rk99cd88lyufl'}, 
                {'key': 'module', 'value': 'distribution'}, 
                {'key': 'sender', 'value': 'cosmosvaloper196ax4vc0lwpxndu9dyhvca7jhxp70rmcvrj90c'}
        ]}, 
        {'type': 'transfer', 'attributes': [
            {'key': 'recipient', 'value': 'cosmos196ax4vc0lwpxndu9dyhvca7jhxp70rmcfhxsrt'}, 
            {'key': 'sender', 'value': 'cosmos1jv65s3grqf6v6jl3dp4t6c9t9rk99cd88lyufl'}, 
            {'key': 'amount', 'value': '2981065787uatom'}]}, 
            {'type': 'withdraw_commission', 'attributes': [
                    {'key': 'amount', 'value': '2981065787uatom'}]}]}