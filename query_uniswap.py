#Uniswap and Sushiwap requires separate query definitions.
import requests
import json
import math
import time
import sys


def runQuery(query):

    request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',json={'query': query})
    
    if request.status_code == 200:
        try:
            return request.json()['data']
        except:
            time.sleep(2)
            runQuery(query)

    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


def roundBlock(block):
    return math.floor(int(block) / 50) * 50 + 12

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
#todo add error handling for invalid block arg
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

def loadLocalEthPrice(block):
    with open('output/ethPrices.json') as f:
        ethPrices = json.load(f)
    
    return ethPrices[str(roundBlock(block))]


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

#script to update json file with new eth prices
def updatePriceData(currentBlock="default"):

    #load currently available eth prices
    ethPrices = {}
    with open('output/ethPrices.json') as f:
        ethPrices = json.load(f)

    #retrieve latest block number
    if currentBlock == "default":
        currentBlock = requests.get("https://api.blockcypher.com/v1/eth/main").json()["height"]
        currentBlock = roundBlock(currentBlock)

    print(f"Current Block: {currentBlock}")
    
    newBlock = True


    #add new price info to json file
    while newBlock:
        
        if str(currentBlock) in ethPrices:
            newBlock = False
        else:
            ethPrices[str(currentBlock)] = getEthPriceAtBlock(currentBlock)
            print(currentBlock)
            print(ethPrices[str(currentBlock)])

            currentBlock -= 50

    with open('output/ethPrices.json', 'w', encoding='utf-8') as f:
        json.dump(ethPrices, f, ensure_ascii=False, indent=4)



# Main program
def main():
    if sys.argv[1] == "updatePrice":
        updatePriceData()

if __name__ == "__main__":
    main()
