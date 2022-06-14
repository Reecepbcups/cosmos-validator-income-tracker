'''
Logic:

- Every 60 minutes, query all validators (those who are bonded).
  - Save to cache

Loop through validators & query their commission amounts in terms of ATOM (not uatom).
Save this to a MongoDB collection or redis hset with their amount. (This way we can do a chart of their earnings over time every 1 hour)

Show current total value in USD based on coingecko price
'''
import os

from dotenv import load_dotenv
from MongoHelper import MongoHelper

load_dotenv()
m = MongoHelper(uri=os.getenv('MONGO_URI'))
print(m.get_databases())