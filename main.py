'''
Logic:

- Every 60 minutes, query all validators (those who are bonded).
  - Save to cache

Loop through validators & query their commission amounts in terms of ATOM (not uatom).
Save this to a MongoDB collection or redis hset with their amount. (This way we can do a chart of their earnings over time every 1 hour)

Show current total value in USD based on coingecko price




'''