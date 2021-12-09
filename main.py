import requests
import os
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.environ.get("USER_AGENT")
API_HOLDERS_KEY = os.environ.get("API_HOLDERS_KEY")
API_TRANSACTIONS_KEY = os.environ.get("API_TRANSACTIONS_KEY")

API_HOLDERS_URI_PROD = os.environ.get("API_HOLDERS_URI_PROD")
API_HOLDERS_URI_DEV = os.environ.get("API_HOLDERS_URI_DEV")
API_HOLDERS_RESOURCE = os.environ.get("API_HOLDERS_RESOURCE")

API_TRANSACTIONS_URI_PROD = os.environ.get("API_TRANSACTIONS_URI_PROD")
API_TRANSACTIONS_URI_DEV = os.environ.get("API_TRANSACTIONS_URI_DEV")
API_TRANSACTIONS_RESOURCE = os.environ.get("API_TRANSACTIONS_RESOURCE")

TOKEN_ADDRESS = {
  "GM": "0xbc7250c8c3eca1dfc1728620af835fca489bfdf3#balances"
}

# Return list of holders
def getHolders():
  headers = { 'User-Agent': USER_AGENT }
  query = {
    "apiKey" : API_TRANSACTIONS_KEY
  }
  URI = API_HOLDERS_URI_DEV + API_HOLDERS_RESOURCE + TOKEN_ADDRESS["GM"]
  response = requests.get(URI, params=query, headers = headers)
  # FIXME: change to return instead of printing
  print (response.json)


# Return list of transactions
def getTransactions():
  headers = { 'User-Agent': USER_AGENT }
  query = {
    "module" : "account",
    "action" : "txlist",
    "address" : "0xDCCc15d1153A6ADE7E6aeD44d34679b82C7845cA", # FIXME: hard coding just to poc test
    "startblock" : 0,
    "endblock" : 99999999,
    "page" : "1",
    "offset" : "1",
    "sort" : "asc",
    "apikey" : API_TRANSACTIONS_KEY
  }
  URI = API_TRANSACTIONS_URI_DEV + API_TRANSACTIONS_RESOURCE
  response = requests.get(URI, params=query, headers = headers)
  # FIXME: change to return instead of printing
  print (response)

getHolders()
#getTransactions()
