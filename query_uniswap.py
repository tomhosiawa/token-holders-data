#Uniswap and Sushiwap requires separate query definitions.
import requests


def runQuery(query):

    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',json={'query': query})
    
    if request.status_code == 200:
        try:
            return request.json()['data']
        except:
            sleep(2)
            runQuery(query)

    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))



def getEthPrice(query_result):
    swap = query_result['swaps'][0]
    token0 = swap["pair"]["token0"]["symbol"]
    ethPrice = 0

    if swap['amount0In'] != '0':
        if swap['amount1Out'] != '0':
            ethPrice = float(swap['amount0In']) /  float(swap['amount1Out'])
        else:
            ethPrice = float(swap['amount0In']) /  float(swap['amount0Out'])
    else:
        ethPrice = float(swap['amount0Out']) /  float(swap['amount1In'])

    return ethPrice


#searches latest ETH/DAI tx since block number and uses the tx to calculate eth price
def getEthPriceAtBlock(block):
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
    return getEthPrice(result)

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
    currentBlock = 13677712

    f = open("./output/ethPrices.txt", "r")

    for n in range(52560):
        block = currentBlock - (n * 50)
        
        [ethPrice, ethAmount] = getEthDataAtBlock(block)
        print(f"Block: {block}, Ether Price: {ethPrice}, Ether Amount: {ethAmount}")
        f.write(f"Block: {block}, Ether Price: {ethPrice}, Ether Amount: {ethAmount}\n")

    f.close()

if __name__ == "__main__":
    main()
