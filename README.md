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

**Request example:** `http://localhost:5000/accounts`

**Response example:** `["DU3799451", "DU3243554"]`

### GET /summary/\<account name\>
List of account values for the given account, or of all accounts if account is left blank.

**Request example:** `http://localhost:5000/summary/DU3799451`

**Response example:**
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

**Request example:** `http://localhost:5000/pnl/DU3799451`

**Response example:** 
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

**Request example:** `http://localhost:5000/positions/DU3799451`

**Response example:** 
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

### GET /orders
List of all orders from this session.

**Request example:** `http://localhost:5000/orders`

### GET /orders/open
List of all open orders.

**Request example:** `http://localhost:5000/orders/open`

### GET /orders/completed
Request and return a list of completed trades.

**Request example:** `http://localhost:5000/orders/completed`

### GET /trades
List of all order trades from this session.

**Request example:** `http://localhost:5000/trades`

### GET /trades/open
List of all open order trades.

**Request example:** `http://localhost:5000/trades/open`

### GET /fills
List of all fills from this session.

**Request example:** `http://localhost:5000/fills`

### GET /executions
List of all executions from this session.

**Request example:** `http://localhost:5000/executions`

### GET /reqMktData
Returns live market data (subscription required).

#### Parameters
**symbol** – The contract (or its underlying) symbol.

**secType** - The security type:

    ’STK’ = Stock (or ETF)
    ’OPT’ = Option
    ’FUT’ = Future
    ’IND’ = Index
    ’FOP’ = Futures option
    ’CASH’ = Forex pair
    ’CFD’ = CFD
    ’BAG’ = Combo
    ’WAR’ = Warrant
    ’BOND’= Bond
    ’CMDTY’= Commodity
    ’NEWS’ = News
    ’FUND’= Mutual fund

**exchange** – The destination exchange.

**currency** – The underlying’s currency.

**primaryExchange** – The contract’s primary exchange. For smart routed contracts, used to define contract in case of ambiguity. Should be defined as native exchange of contract, e.g. ISLAND for MSFT. For exchanges which contain a period in name, will only be part of exchange name prior to period, i.e. ENEXT for ENEXT.BE.

*For  more options see: https://ib-insync.readthedocs.io/api.html#module-ib_insync.contract* 

**Request example:** `http://localhost:5000/reqMktData?secType=STK&symbol=AMD&exchange=SMART&currency=USD`

### GET /reqHistoricalTicks
Request historical ticks. The time resolution of the ticks is one second.

#### Parameters
Contract description required. See reqMktData.

**startDateTime** – Can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

**endDateTime** – One of startDateTime or endDateTime can be given, the other must be blank.

**numberOfTicks** – Number of ticks to request (1000 max). The actual result can contain a bit more to accommodate all ticks in the latest second.

**whatToShow** – One of ‘Bid_Ask’, ‘Midpoint’ or ‘Trades’.

**useRTH** – If True then only show data from within Regular Trading Hours, if False then show all data.

**ignoreSize** – Ignore bid/ask ticks that only update the size.

**Request example:** `http://localhost:5000/reqHistoricalTicks?secType=STK&symbol=AMD&exchange=SMART&currency=USD&startDateTime=20210710 10:00:00&numberOfTicks=10&whatToShow=Bid_Ask&useRTH=True&ignoreSize=False`

### GET /reqFundamentalData
Get fundamental data of a contract in XML format.

#### Parameters
Contract description required. See reqMktData.

reportType –

    ‘ReportsFinSummary’: Financial summary
    
    ’ReportsOwnership’: Company’s ownership
    
    ’ReportSnapshot’: Company’s financial overview
    
    ’ReportsFinStatements’: Financial Statements
    
    ’RESC’: Analyst Estimates
    
    ’CalendarReport’: Company’s calendar

**Request example:** `http://localhost:5000/reqFundamentalData?secType=STK&symbol=AMD&exchange=SMART&currency=USD&reportType=ReportsFinSummary`

### GET /tickers
Get a list of all tickers.

**Request example:** `http://localhost:5000/tickers`