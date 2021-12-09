import requests
import os
from dotenv import load_dotenv

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
API_TRANSACTIONS_KEY = os.environ.get("API_TRANSACTIONS_KEY")
API_TRANSACTIONS_RESOURCE = os.environ.get("API_TRANSACTIONS_RESOURCE")

TOKEN_ADDRESS = {
  "GM": "0xbc7250c8c3eca1dfc1728620af835fca489bfdf3"
}

# Return list of holders
def getHolders():
  headers = { 'User-Agent': USER_AGENT }
  query = {
    "apiKey" : API_HOLDERS_KEY,
    "limit" : 1000
  }
  URI = API_HOLDERS_URI + API_HOLDERS_RESOURCE + TOKEN_ADDRESS["GM"]
  response = requests.get(URI, params=query, headers = headers)
  # FIXME: change to return instead of printing
  print (response.json())


# Return list of transactions
def getTransactions():
  headers = { 'User-Agent': USER_AGENT }
  query = {
    "module" : "account",
    "action" : "txlist",
    "address" : "0xdccc15d1153a6ade7e6aed44d34679b82c7845ca", # FIXME: hard coding just to poc test
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

getHolders()
print ("")
getTransactions()
