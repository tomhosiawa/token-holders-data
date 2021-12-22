#Uniswap and Sushiwap requires separate query definitions.
import requests
import json
import math
import time
import sys

def runQuery(query):

    # Query request with sushiswap endpoint
    sushi_endpoint = 'https://gateway.thegraph.com/api/[api-key]/subgraphs/id/0x4bb4c1b0745ef7b4642feeccd0740dec417ca0a0-0'
    request = requests.post(sushi_endpoint,json={'query': query})
    
    # 200 means your request was successful and the server responded with the data you were requesting
     if request.status_code == 200:
        try:
            return request.json()['data']
        except:
            print("error")
            time.sleep(2)
            runQuery(query)

    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))
        
#get top 5000 pairs in sushi for whitelist 
def getTopPairs():
    
    pairs = {}
    for n in range(5):
        print(n * 1000)
        
        #query definition identical to uni v2
        query = f"""
                {{
             pairs(first: 1000, 
             orderBy: reserveUSD, 
             orderDirection: desc, 
             skip: {n * 1000}) {{
               id
             }}
            }}
        """
   
        result = runQuery(query)["pairs"]

        for pair in result:
            pairs[pair['id']] = "sushiswap"

    with open('output/wl_sushiswap_contracts.json', 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=4)

#returns amount transacted in ETH given a txID
def getEthAmountFromTx(txId):
    query = f"""
        query swaps {{
      swaps(where:{{transaction:"{txId}"}}) {{
        id
        timestamp
        amount0In
        amount1In
        amount0Out
        amount1Out
        amountUSD
        pair {{
          token0 {{
            id
            symbol
          }}
          token1 {{
            id
            symbol
          }}
        }}
      }}
    }}
    """
    result = runQuery(query)["swaps"]

    #to handle liquidity removal/add or other non swap functions
    if result == []:
        return 0
    else:
        result = result[0]

    print(result)
    
    #if token0 is eth or eth equivalent, return whatever amount of token 0 was transacted
    if result['pair']['token0']['symbol'] == 'ETH' or result['pair']['token0']['symbol'] == 'WETH':
        return max(float(result['amount0In']), float(result['amount0Out']))
    else:
        return max(float(result['amount1In']), float(result['amount1Out'])) 

# Main program
def main():
    

if __name__ == "__main__":
    main()
