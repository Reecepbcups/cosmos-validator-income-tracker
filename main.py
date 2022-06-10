#  https://github.com/Reecepbcups/cosmos-governance-bot/blob/main/ChainApis.py

#  https://v1.cosmos.network/rpc/v0.45.1


# Get latest validators
# curl -X GET "https://api.cosmos.network/cosmos/staking/v1beta1/validators" -H "accept: application/json"


# get commission
# curl -X GET "https://api.cosmos.network/cosmos/distribution/v1beta1/validators/cosmosvaloper1q9p73lx07tjqc34vs8jrsu5pg3q4ha534uqv4w/commission" -H "accept: application/json"

# outstanding reqwards
# curl -X GET "https://api.cosmos.network/cosmos/distribution/v1beta1/validators/cosmosvaloper1q9p73lx07tjqc34vs8jrsu5pg3q4ha534uqv4w/outstanding_rewards" -H "accept: application/json"

# slashes
# curl -X GET "https://api.cosmos.network/cosmos/distribution/v1beta1/validators/cosmosvaloper1q9p73lx07tjqc34vs8jrsu5pg3q4ha534uqv4w/slashes" -H "accept: application/json"


# get validator information
# curl -X GET "https://api.cosmos.network/cosmos/staking/v1beta1/validators/cosmosvaloper1q9p73lx07tjqc34vs8jrsu5pg3q4ha534uqv4w" -H "accept: application/json"