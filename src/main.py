'''
Logic:

- Every 60 minutes, query all BONDED validators.

Loop through validators those validators & query their commission amounts in terms of ATOM.
Save this to a MongoDB collection. (This way we can do a chart of their earnings over time every 1 hour)

Show current total value in USD based on coingecko price
'''
import os, time, json, redis
import operator

from dotenv import load_dotenv
from MongoHelper import MongoHelper
from CosmosEndpoints import getOutstandingCommissionRewards, getLatestValidatorSet, getValidatorSlashes

from util import epochTimeToHumanReadable


load_dotenv()
m = MongoHelper(uri=os.getenv('MONGODB_URI'))
db = os.getenv('MONGO_DB_NAME')
# print(m.get_databases())
r = redis.Redis(host="localhost", port=6379, db=0)

def main():
    addr = "cosmosvaloper1qs8tnw2t8l6amtzvdemnnsq9dzk0ag0z52uzay" # Castlenode
    # takeValidatorSnapshot(addr)

    '''
    gets latest cached version of the validator set
    '''
    valset = getAllValidators(mustBeBonded=True, fromCacheIfThere=True)
    valList = list(valset.keys())
    # print(len(valset), valset.keys()); #print(valset.get(addr)['moniker'])
    takeValidatorSnapshot(valList, breakIdx=-1)


    # getCommissionDifferencesOverTime(addr)


def getCommissionDifferencesOverTime(valop: str):
    print("Commissions for validator: ", valop)    
    # sort commissions by their key which is an epoch time
    commissions = dict(query_validator_commission_held_over_time(valop))
    commissions = sorted(commissions.items(), key=operator.itemgetter(0), reverse=False) # newest time to oldest

    from Coingecko import getPrice
    cosmosPrice = getPrice("cosmos")

    lastCommission, lastTime, isFirst = -1, -1, False
    for comm in commissions:
        t, amt = comm
        # print(t, amt)

        # handles first time & amount in the database as the initial gage
        if lastCommission == -1: lastCommission = amt;  isFirst = True     
        if lastTime == -1: lastTime = t; isFirst = True
        if isFirst: isFirst = False; continue

        # subtract amt from last commission, and print the time difference        
        print(f"\nBetween {epochTimeToHumanReadable(lastTime)} & {epochTimeToHumanReadable(t)}")

        diff = amt-lastCommission
        if diff > 0:        
            # These would always be the same seconds provided we took snapshots at the correct times
            print(f"in {int(t)-int(lastTime)} Seconds their ATOM increased by {diff} (${round(diff*cosmosPrice, 3)}).\tTotal Commission Held: {amt}")
            
        else:
            
            print(f"VALIDATOR WITHDREW REWARDS {diff} ATOM @ a price of $", cosmosPrice)
            print(f"Total Gain: ${round(-(diff)*cosmosPrice, 2)}")
            # add to queue / query them for check blocks for any Txs they have done. 
            # Get their msg withdraw block from last time we checked blocks
            # save the amount they withdrew to a MongoDB instance
            # data should have:
            # {validator: addr, {commissionWithdrawn: amt, time: t, hash: txhash}}
            
        # update values for the next run    
        lastCommission, lastTime = amt, t

    
# ----------------------------------------------------------------------

def getAllValidators(mustBeBonded=True, fromCacheIfThere=True):
    # We may set fromCacheIfThere to be False when we want to get the latest for an update to the set
    # ^ useful when we want to save snapshot latest commissions to the cache
    k = "latest:valset"
    TTL = 60*60
    if fromCacheIfThere:
        # check if we can read it from redis
        # if not, we will query the validator set
        latestVals = r.get(k) 

        if latestVals is None:
            # query the validator set & cache it
            latestVals = getLatestValidatorSet(bondedOnly=mustBeBonded)
            r.set(k, json.dumps(latestVals), ex=TTL)
        else:
            print("getAllValidators CACHED VERSION")
            latestVals = json.loads(r.get(k).decode('utf-8'))
    else:
        # gets an uncached version so we can compare
        print("getAllValidators UN-CACHED VERSION")
        latestVals = getLatestValidatorSet()
        r.set(k, json.dumps(latestVals), ex=TTL) # sets to the cache for the next run we want with cache

    return latestVals


def takeValidatorSnapshot(validatorOps, breakIdx: int = 5, currentEpochTime: str = str(int(time.time()))): # Make async with httpx in the future?
  # loops through all validators & snapshots their current comission
  # TODO: Pass through the time so all keys are the same?
  
  # We could save every 1 hour in "hourly" section. Then have a "daily" as well? still in epoch time?
  # So I guess on hour 23 we move the last hour from hourly to daily collection.
  # for now we just do it every hour

  # validators = getLatestValidatorSet()
  for idx, val in enumerate(validatorOps):    
    pastData = m.find_one(db, 'atom', {'validator': val})
    newData = {currentEpochTime: getOutstandingCommissionRewards(val).get("atom")}

    if pastData is None:
      # they never had a snapshot before
      newData = {"validator": val, "values": newData}
    else:
      # they have a snapshot before
      pastData = dict(pastData.get("values"))
      pastData.update(newData) # appends the new current time -> the document
      updatedData = pastData
      newData = {"validator": val, "values": updatedData} # adds the new time & held token to the valoper

    # in the future we will just update it, this works for now
    m.delete_one(db, 'atom', {'validator': val})
    m.insert(db, 'atom', newData)

    if idx == breakIdx:
        print(f"takeValidatorSnapshot() hit index limit of {breakIdx} due to wanting to break here & reduce load")
        break


def query_validator_commission_held_over_time(valop):
    doc = m.find_one(db, 'atom', {'validator': valop})
    return doc.get("values")



if __name__ == '__main__':
    main()