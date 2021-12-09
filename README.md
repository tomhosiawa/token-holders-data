# Token Holder Data

Get holders transactions for top X holders of a coin.

---

## Install dependencies

Install python dependencies

`pip install requests`

`pip install python-dotenv`

---

## Setup environment

1. Set api keys with your own

    In ".env" file, paste api keys for

    `API_HOLDERS_KEY: from etherscan`

    `API_TRANSACTIONS_KEY: from ethportal`

2. (Optional) Set limit for top holders to get data on
    API_HOLDERS_TOP_HOLDERS_LIMIT = 1000 (default)

3. Set type of transactions to fetch from holders

    In ".env" file, paste

    For Normal Transaction: `API_TRANSACTION_TYPE="txlist"`

    For ERC20 - Token Transfer Events: `API_TRANSACTION_TYPE="tokentx"`

4. Set tokens to fetch holders from

    Paste token's key and it's address into `tokens.json`

5. (Optional) Turn on print output, set

   In ".env" file, change
   DEBUG = True

---

## Usage

Development

`yarn start`

Production

`yarn prod`

CSV files are writen to OUTPUT_DIR_PATH defined in ".env"
