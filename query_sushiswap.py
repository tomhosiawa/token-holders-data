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

def getEthPrice(query_result):
    swap = query_result['swaps'][0]
    token0 = swap["pair"]["token0"]["symbol"]
    ethPrice = 0
    
    if swap['amount0In'] != '0':
        ethPrice = float(swap['amount0In']) /  float(swap['amount1Out'])
    else:
        ethPrice = float(swap['amount0Out']) /  float(swap['amount1In'])

    return ethPrice

def getEthAmount(query_result):
    # todo
    return 0

def getEthPriceAtBlock(block):
    #SUSHI/ETH pair contract address
    query = f"""
    {{
        swaps(first: 1, where: {{ pair: "0x795065dcc9f64b5614c407a6efdc400da6221fb0" }} orderBy: timestamp, orderDirection: desc, block: {{number: {block} }}) {{
          transaction {{
            id
            timestamp
          }}
          id
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
          amount0In
          amount0Out
          amount1In
          amount1Out
          amountUSD
          to
        }}
    }}
    """

    result = runQuery(query)
    return getEthPrice(result)




# Main program
def main():
    #random block from etherscan https://etherscan.io/block/13839941
    currentBlock = 13839941

    f = open("./output/ethPrices.txt", "a")

    for n in range(52560):
        block = currentBlock - (n * 50)
        
        [ethPrice, ethAmount] = getEthDataAtBlock(block)
        print(f"Block: {block}, Ether Price: {ethPrice}, Ether Amount: {ethAmount}")
        f.write(f"Block: {block}, Ether Price: {ethPrice}, Ether Amount: {ethAmount}\n")

    f.close()

if __name__ == "__main__":
    main()