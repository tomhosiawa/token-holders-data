import requests
import os
from dotenv import load_dotenv
import json

TOKENS_FILEPATH = "./tokens.json"

# Load dotevn properties
load_dotenv()
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
API_TRANSACTIONS_TYPE = os.environ.get("API_TRANSACTIONS_TYPE")


# Return list of holders
def getTokenHolders(token):
  headers = { 'User-Agent': USER_AGENT }
  query = {
    "apiKey" : API_HOLDERS_KEY,
    "limit" : API_HOLDERS_TOP_HOLDERS_LIMIT
  }
  URI = API_HOLDERS_URI + API_HOLDERS_RESOURCE + token
  response = requests.get(URI, params=query, headers = headers)
  # FIXME: change to return instead of printing
  print (response.json())
  print ("")
  #getHolderTransactions()


# Return list of transactions
def getHolderTransactions():
  headers = { 'User-Agent': USER_AGENT }
  query = {
    "module" : "account",
    "action" : API_TRANSACTIONS_TYPE,
    "address" : "0xdccc15d1153a6ade7e6aed44d34679b82c7845ca", # Holder's address FIXME: hard coding just to poc test
    "startblock" : 0,
    "endblock" : 99999999,
    "page" : "1",
    "offset" : "1",
    "sort" : "asc",
    "apikey" : API_TRANSACTIONS_KEY
  }
  URI = API_TRANSACTIONS_URI + API_TRANSACTIONS_RESOURCE
  response = requests.get(URI, params=query, headers = headers)
  # FIXME: change to return instead of printing
  print (response.json())


# Return input in csv format   
def toCSV(input):
  print ("stub: convetToCsv")


# Return tokens from json file
def getTokens(filepath):
  with open(filepath) as f:
    return json.load(f)


# Save input to disk
def saveToFile(input, filepath):
  print ("stub: saveToFile")


# Main program
tokensAddress = getTokens(TOKENS_FILEPATH)
for token in tokensAddress:
  getTokenHolders(tokensAddress[token])
  