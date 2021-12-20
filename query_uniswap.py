import requests


def runQuery(query):

    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',json={'query': query})
    
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

def getEthDataAtBlock(block):
    
    query = f"""
    {{
        swaps(first: 1, where: {{ pair: "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11" }} orderBy: timestamp, orderDirection: desc, block: {{number: {block} }}) {{
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
    return [getEthPrice(result), getEthAmount(result)]

# Main program
def main():
    currentBlock = 13677712

    f = open("./output/ethPrices.txt", "a")

    for n in range(52560):
        block = currentBlock - (n * 50)
        
        [ethPrice, ethAmount] = getEthDataAtBlock(block)
        print(f"Block: {block}, Ether Price: {ethPrice}, Ether Amount: {ethAmount}")
        f.write(f"Block: {block}, Ether Price: {ethPrice}, Ether Amount: {ethAmount}\n")

    f.close()

if __name__ == "__main__":
    main()
