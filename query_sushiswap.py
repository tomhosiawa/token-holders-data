#Uniswap and Sushiwap requires separate query definitions.
import requests

# Function to use requests.post to make an API call to the subgraph url
def runQuery(query):

    # Query request with sushiswap endpoint
    sushi_endpoint = 'https://gateway.thegraph.com/api/[api-key]/subgraphs/id/0x4bb4c1b0745ef7b4642feeccd0740dec417ca0a0-0'
    request = requests.post(sushi_endpoint,json={'query': query})
    
    # 200 means your request was successful and the server responded with the data you were requesting
    if request.status_code == 200:
        return request.json()['data']
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))



def getEthAmountFromTx(txId):
    #todo





# Main program
def main():
    

if __name__ == "__main__":
    main()
