import requests
import os
from dotenv import load_dotenv
import json
import csv

from query_uniswap import loadLocalEthPrice
from query_uniswap import getEthAmountFromTx

TOKENS_FILEPATH = "./tokens.json"

# Load dotevn properties
load_dotenv()
if os.environ.get("DEBUG").lower() == "true":
    DEBUG = True
else:
    DEBUG = False
OUTPUT_DIR_PATH = os.environ.get("OUTPUT_DIR_PATH")
USER_AGENT = os.environ.get("USER_AGENT")

if os.environ.get("ENV") == "PROD":
    API_HOLDERS_URI = os.environ.get("API_HOLDERS_URI_PROD")
    API_TRANSACTIONS_URI = os.environ.get("API_TRANSACTIONS_URI_PROD")
else:
    API_HOLDERS_URI = os.environ.get("API_HOLDERS_URI_DEV")
    API_TRANSACTIONS_URI = os.environ.get("API_TRANSACTIONS_URI_DEV")

API_HOLDERS_KEY = os.environ.get("API_HOLDERS_KEY")
API_HOLDERS_RESOURCE = os.environ.get("API_HOLDERS_RESOURCE")
API_HOLDERS_TOP_HOLDERS_LIMIT = os.environ.get("API_HOLDERS_TOP_HOLDERS_LIMIT")
API_TRANSACTIONS_KEY = os.environ.get("API_TRANSACTIONS_KEY")
API_TRANSACTIONS_RESOURCE = os.environ.get("API_TRANSACTIONS_RESOURCE")
API_TRANSACTION_TYPE = os.environ.get("API_TRANSACTION_TYPE")

if DEBUG:
    API_TRANSACTION_PAGE_SIZE = os.environ.get("API_TRANSACTION_PAGE_SIZE_DEBUG")
else:
    API_TRANSACTION_PAGE_SIZE = os.environ.get("API_TRANSACTION_PAGE_SIZE")

# Return list of holders
# cbAppendtoCSV: callback function to save transactions to csv file
def getTokenHolders(tokenName, tokenAddress, cbAppendtoCSV):
    headers = { 'User-Agent': USER_AGENT }
    query = {
        "apiKey" : API_HOLDERS_KEY,
        "limit" : API_HOLDERS_TOP_HOLDERS_LIMIT
    }
    URI = API_HOLDERS_URI + API_HOLDERS_RESOURCE + tokenAddress
    response = requests.get(URI, params=query, headers = headers).json()
    
    holders = response["holders"] 
    for holder in holders:    
        holderAddress = holder["address"]
        
        if DEBUG:
            print (">>> HOLDER: " + holderAddress)
            
        getHolderTransactions(tokenName, holderAddress, cbAppendtoCSV)    
        
        if DEBUG:
            print ("")


# Return list of transactions
# TODO: check if needs to do error/performance checking based on tranactions list size
def getHolderTransactions(tokenSymbol, holderAddress, cbAppendtoCSV):
    page = 1
    
    headers = { 'User-Agent': USER_AGENT }
    query = {
        "module" : "account",
        "action" : API_TRANSACTION_TYPE,
        "address" : holderAddress,
        "startblock" : 0,
        "endblock" : 99999999,
        "page" : page,
        "offset" : API_TRANSACTION_PAGE_SIZE,
        "sort" : "desc",
        "apikey" : API_TRANSACTIONS_KEY
    }
    URI = API_TRANSACTIONS_URI + API_TRANSACTIONS_RESOURCE
      
    # FIXME: convert status to a bool, can't get it to work with bool(status)
    status = "1"
    while status == "1":
        response = requests.get(URI, params=query, headers = headers).json()
        status = response["status"]    
        if status == "1":
            transactions = response["result"]
            print(holderAddress)
            transactions = getAugmentedTransactions(tokenSymbol, holderAddress, transactions)
            cbAppendtoCSV(tokenSymbol, holderAddress, transactions)

            if DEBUG:
                print (">>> Transactions of holder: " + holderAddress)
                print (">>> Page: " + str(page) + " Status: " + str(status))
                if transactions:
                  print (transactions[0])
                break
            
            page = page + 1
            query["page"] = page
    
    return transactions

def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open('whitelistedContracts.json', 'w') as output_file:
        json.dump(result, output_file)
        
# getAugmentedTransactions() update the whitelistedContracts variable to contain all 3
# Return transactions with action field: buy or sell
def getAugmentedTransactions(tokenSymbol, holderAddress, transactions):
    newTransactions = []
    newTransactionsCount = 0

    #whitelist Uni v2, Uni v3, Sushi
    #currently has GM and MONGOOSE hardcoded in
    # todo, add an expanded whitelist in separate file
    files = ['output/wl_univ2_contracts.json',
             'output/wl_univ3_contracts.json',
             'output/wl_sushiswap_contracts.json']
    merge_JsonFiles(files)
    
    for i, transaction in enumerate(transactions, start=0):
        # Omit transaction if not correct token
        # Omit if older than 300 days
        # Omit if not interacting with whitelisted contract

        #set contract equal to whatever isn't the holder addresss
        contract = transaction['to'] if transaction['to'] != holderAddress else transaction['from'] 

        if transaction["tokenSymbol"] == tokenSymbol and int(transaction["blockNumber"]) > 11922562 and contract in whitelistedContracts:
          
          #only increment transactionCount on valid transaction
          newTransactions.append(transactions[i])
          newTransactionsCount += 1

        else:
            continue
        
        # Add ethPrice field
        blockNumber = transaction["blockNumber"]
        txId = transaction["hash"]

        ethPrice = loadLocalEthPrice(blockNumber)
        ethAmount = getEthAmountFromTx(txId)


        newTransactions[newTransactionsCount - 1]["ethPrice"] = ethPrice
        
        # Add action field
        if transaction["from"] == holderAddress:
            newTransactions[newTransactionsCount - 1]["action"] = "Sell"
        elif transaction["to"] == holderAddress:
            newTransactions[newTransactionsCount - 1]["action"] = "Buy"
        else:
            newTransactions[newTransactionsCount - 1]["action"] = "error"

        # Add costBasis        
        transactions[newTransactionsCount - 1]["costBasis"] = float(ethPrice) * float(ethAmount)
        
    return newTransactions


# Create csv file dataset for tokenName and return it
def createCSVFile(tokenName):
    outFile = open(OUTPUT_DIR_PATH + tokenName + ".csv", 'w')
    outFile.write("holderAddress,blockNumber,timeStamp,hash,nonce,blockHash,from,contractAddress,to,"\
                  "value,tokenName,tokenSymbol,tokenDecimal,transactionIndex,gas,gasPrice,gasUsed,"\
                  "cumulativeGasUsed,input,confirmations,ethPrice,action,costBasis\n")
    outFile.close()


# Return input in csv format
def appendToCSV(tokenName, holderAddress, transactions):
    outFile = open(OUTPUT_DIR_PATH + tokenName + ".csv", 'a')
    csvWriter = csv.writer(outFile)
    
    for transaction in transactions:
        transaction = [holderAddress] + list(transaction.values())
        csvWriter.writerow(transaction)
    
    outFile.close()


# Return tokens from json file
def getTokens(filepath):
    with open(filepath) as f:
        return json.load(f)


# Main program
def main():
    #Store token address from filepath in "tokensAddress"
    #tokensAddress is a json object, containing key/value pairs
    tokensAddress = getTokens(TOKENS_FILEPATH)
    
    #Iterate through token addresses 
    for tokenName in tokensAddress:
        if DEBUG:
            print (">>> TOKEN:" + tokenName)
            
        #Create csv dataset for tokenName
        createCSVFile(tokenName)
        
        #Return list of holders for tokenName
        getTokenHolders(tokenName, tokensAddress[tokenName], appendToCSV)  
        
        if DEBUG:
            print ("")

if __name__ == "__main__":
    main()
