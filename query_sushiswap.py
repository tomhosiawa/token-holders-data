#Uniswap and Sushiwap requires separate query definitions.
import requests
def runQuery(query):

    # Query request with sushiswap endpoint
    sushi_endpoint = 'https://gateway.thegraph.com/api/[api-key]/subgraphs/id/0x4bb4c1b0745ef7b4642feeccd0740dec417ca0a0-0'
    request = requests.post(sushi_endpoint,json={'query': query})
    
    # 200 means your request was successful and the server responded with the data you were requesting
    if request.status_code == 200:
        return request.json()['data']
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

    with open('output/wl_univ2_contracts.json', 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=4)
        
def getEthAmountFromTx(txId):
    #todo





# Main program
def main():
    

if __name__ == "__main__":
    main()
