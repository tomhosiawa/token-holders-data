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

2. Set type of transactions to fetch from holders

    In ".env" file, paste

    For Normal Transaction: `API_TRANSACTION_TYPE="txlist"`

    For ERC20 - Token Transfer Events: `API_TRANSACTION_TYPE="tokentx"`

3. Set tokens to fetch holders from

    Paste token's key and it's address into `tokens.json`

---

## Usage

Development

`yarn start`

Production

`yarn prod`
