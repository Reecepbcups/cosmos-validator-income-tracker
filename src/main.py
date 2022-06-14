'''
Logic:

- Every 60 minutes, query all validators (those who are bonded).
  - Save to cache

Loop through validators & query their commission amounts in terms of ATOM (not uatom).
Save this to a MongoDB collection or redis hset with their amount. (This way we can do a chart of their earnings over time every 1 hour)

Show current total value in USD based on coingecko price
'''
import os, time

from dotenv import load_dotenv
from MongoHelper import MongoHelper
from CosmosEndpoints import getOutstandingCommissionRewards, getLatestValidatorSet, getValidatorSlashes


load_dotenv()
m = MongoHelper(uri=os.getenv('MONGODB_URI'))
db = os.getenv('MONGO_DB_NAME')
# print(m.get_databases())


def main():
  takeValidatorCommissionSnapshot()
  # getDocuments()


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

# ----------------------------------------------------------------------

def getAllValidators(fromCacheIfThere=True):
  pass



def takeValidatorCommissionSnapshot():
  # loops through all validators & snapshots their current comission
  
  # MOngodb doesnt work yet

  validators = getLatestValidatorSet()
  for idx, val in enumerate(validators.keys()):
    
    pastData = m.find_one(db, 'atom', {'validator': val})
    newData = {str(int(time.time())): getOutstandingCommissionRewards(val).get("atom")}

    if pastData is None:
      # they never had a snapshot before
      data = {"validator": val, "values": newData}
    else:
      # they have a snapshot before
      pastData = dict(pastData.get("values"))
      pastData.update(newData)
      updatedData = pastData
      newData = {"validator": val, "values": updatedData} # adds the new time & held token to the valoper

    m.insert(db, 'atom', newData)  


    # m.insert(db, collectionName="atom", values=data)  
    if idx == 2:
      break

  


# based on their "time" key
def compareDocumentTimes(time1, time2):
  pass
  
    





if __name__ == '__main__':
    main()