# IB Custom
The goal of this project is to present an easy-to-use REST API to access data in Interactive Brokers Trader Workstation (TWS).

## Requirements
- Python 3.6 or higher and PIP
- A running TWS or IB Gateway application (version 972 or higher)

Make sure the API port of the TWS is enabled (https://interactivebrokers.github.io/tws-api/initial_setup.html)

If you need to host IB Custom not on the same machine TWS is running on you also need to disable "Allow connections from 
localhost only" checkbox in TWS API settings.

## Installation/Deployment
1. Download this repository
2. Set TWS IP-address and Port in *settings.ini* (only if it is running on the separate machine)
3. In terminal go to the project root and install python packages using `pip install -r requirements.txt`
4. Run server with `python main.py`
5. You can perform health-check with `curl http://localhost:5000/health`

## Endpoints

### GET /health
Returns OK if IB Custom service is running (health check)

### GET /accounts
Returns the list of managed account names.

Request example: `http://localhost:5000/accounts`

Response example: `["DU3799451", "DU3243554"]`

### GET /summary/\<account name\>
List of account values for the given account, or of all accounts if account is left blank.

Request example: `http://localhost:5000/summary/DU3799451`

Response example:
```
[
    {
        "account": "DU3799451",
        "tag": "AccountType",
        "value": "INDIVIDUAL",
        "currency": "",
        "modelCode": ""
    },
    {
        "account": "DU3799451",
        "tag": "Cushion",
        "value": "0.996056",
        "currency": "",
        "modelCode": ""
    },
    ...
    {
        "account": "DU3799451",
        "tag": "TotalCashValue",
        "value": "986609.00",
        "currency": "USD",
        "modelCode": ""
    }
]
```

### GET /pnl/\<account name\>
List of subscribed PnL objects (profit and loss), optionally filtered by account.

Request example: `http://localhost:5000/pnl/DU3799451`
Response example: 
```
{
    "PnL": {
        "account": "DU3799451",
        "dailyPnL": -223.66070556640443,
        "unrealizedPnL": -266.66070556640625,
        "realizedPnL": 0.0
    }
}
```

### GET /positions/\<account name\>
List of positions for the given account, or of all accounts if account is left blank.
Request example: `http://localhost:5000/positions/DU3799451`
Response example: 
```
[
    {
        "account": "DU3799451",
        "contract": {
            "Stock": {
                "secType": "STK",
                "conId": 265598,
                "symbol": "AAPL",
                "exchange": "NASDAQ",
                "currency": "USD",
                "localSymbol": "AAPL",
                "tradingClass": "NMS"
            }
        },
        "position": 100.0,
        "avgCost": 133.91
    }
]
```