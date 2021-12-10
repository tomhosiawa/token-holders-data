import requests
import os
from dotenv import load_dotenv
import json
import csv

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


# Return list of holders
# cbAppendtoCSV: callback function to save transactions to csv file
def getTokenHolders(tokenName, tokenAddress, cbAppendtoCSV):
  headers = { 'User-Agent': USER_AGENT }
  query = {
    "apiKey" : API_HOLDERS_KEY,
    "limit" : API_HOLDERS_TOP_HOLDERS_LIMIT
  }
  URI = API_HOLDERS_URI + API_HOLDERS_RESOURCE + tokenAddress
  response = requests.get(URI, params=query, headers = headers)
    
  holders = response.json()["holders"]
  for holder in holders:    
    holderAddress = holder["address"]
    
    if DEBUG:
      print (">>> HOLDER: " + holderAddress)
        
    transactions = getHolderTransactions(holderAddress)
    cbAppendtoCSV(tokenName, holderAddress, transactions)
    
    if DEBUG:
      print ("")


# Return list of transactions
# TODO: check if needs to do error/performance checking based on tranactions list size
def getHolderTransactions(holderAddress):
  headers = { 'User-Agent': USER_AGENT }
  # FIXME: go over all pages
  query = {
    "module" : "account",
    "action" : API_TRANSACTION_TYPE,
    "address" : holderAddress,
    "startblock" : 0,
    "endblock" : 99999999,
    "page" : "1",
    "offset" : "1",
    "sort" : "asc",
    "apikey" : API_TRANSACTIONS_KEY
  }
  URI = API_TRANSACTIONS_URI + API_TRANSACTIONS_RESOURCE
  response = requests.get(URI, params=query, headers = headers)
  transactions = response.json()["result"]
  
  if DEBUG:
    print (">>> Transactions of holder: " + holderAddress)
    print (transactions)
    
  return transactions


# Create csv file for tokenName and return it
def createCSVFile(tokenName):
  outFile = open(OUTPUT_DIR_PATH + tokenName + ".csv", 'w')
  outFile.write("holderAddress,blockNumber,timeStamp,hash,nonce,blockHash,transactionIndex,from,to,value,gas,gasPrice,isError,txreceipt_status,input,contractAddress,cumulativeGasUsed,gasUsed,confirmations\n")  
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
tokensAddress = getTokens(TOKENS_FILEPATH)
for tokenName in tokensAddress:
  if DEBUG:
      print (">>> TOKEN:" + tokenName)
    
  createCSVFile(tokenName)
  getTokenHolders(tokenName, tokensAddress[tokenName], appendToCSV)  
  
  if DEBUG:
      print ("")
