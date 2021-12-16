# Token Holder Data

Get holders transactions for top X holders of a coin.

---

## Install dependencies

Install python dependencies

`pip install requests`

`pip install python-dotenv`

---

## Setup environment

1. Create a ".env" file

2. Set api keys with your own

    In ".env" file, paste api keys for

    `API_HOLDERS_KEY: from etherscan`

    `API_TRANSACTIONS_KEY: from ethportal`

3. (Optional) Set limit for top holders to get data on
    API_HOLDERS_TOP_HOLDERS_LIMIT = 1000 (default)

4. (Optional) Turn on debugging
   `DEBUG = True`

5. Set type of transactions to fetch from holders

    In ".env" file, paste

    For Normal Transaction: `API_TRANSACTION_TYPE="txlist"`

    For ERC20 - Token Transfer Events: `API_TRANSACTION_TYPE="tokentx"`

6. Set tokens to fetch holders from

    Paste token's key and it's address into `tokens.json`

7. Set number of transactions per api call
   API_TRANSACTION_PAGE_SIZE = 10,000 (default) - 10,000 is max supported by etherscan

8. (Optional) Turn on print output, set

   In ".env" file, change
   DEBUG = True

---

## Usage

Development

`yarn start`

Production

`yarn prod`

CSV files are writen to OUTPUT_DIR_PATH defined in ".env"
