import configparser
import json
import logging.config
from typing import Optional, Union

import nest_asyncio
from ib_insync import IB, util, Stock, Forex, Contract
from quart import Quart, request

# Frameworks
nest_asyncio.apply()
qrt = Quart(__name__)
ib = IB()

# Configuration
config = configparser.ConfigParser()
config.read('settings.ini')

host = config['TWS']['host']
port = int(config['TWS']['port'])
client_id = int(config['TWS']['client_id'])

# Logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('ib-custom')


# Routes
@qrt.route('/health', methods=['GET'])
def health():
    return 'OK'


@qrt.route('/accounts')
async def account():
    with await IB().connectAsync(host, port, client_id) as ibi:
        acct = json.dumps(ibi.managedAccounts())
    return acct


@qrt.route('/summary')
async def summary():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _summary = ibi.accountSummary()
        resp = json.dumps(util.tree(_summary))
    return resp


@qrt.route('/summary/<account>')
async def summary_for_account(account):
    with await IB().connectAsync(host, port, client_id) as ibi:
        _summary = ibi.accountSummary(account)
        resp = json.dumps(util.tree(_summary))
    return resp


@qrt.route('/pnl')
async def pnl():
    with await IB().connectAsync(host, port, client_id) as ibi:
        acct = ibi.managedAccounts()[0]
        pnl = ibi.reqPnL(acct)
        await ibi.pnlEvent
        resp = json.dumps(util.tree(pnl))
    return resp


@qrt.route('/pnl/<account>')
async def pnl_for_account(account):
    with await IB().connectAsync(host, port, client_id) as ibi:
        pnl = ibi.reqPnL(account)
        await ibi.pnlEvent
        resp = json.dumps(util.tree(pnl))
    return resp


@qrt.route('/positions')
async def positions():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _positions = ibi.positions()
        resp = json.dumps(util.tree(_positions))
    return resp


@qrt.route('/positions/<account>')
async def positions_for_account(account):
    with await IB().connectAsync(host, port, client_id) as ibi:
        _positions = ibi.positions(account)
        resp = json.dumps(util.tree(_positions))
    return resp


@qrt.route('/orders')
async def orders():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _orders = ibi.orders()
        resp = json.dumps(util.tree(_orders))
    return resp


@qrt.route('/orders/open')
async def open_orders():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _orders = ibi.openOrders()
        resp = json.dumps(util.tree(_orders))
    return resp


@qrt.route('/orders/completed')
async def completed_orders():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _orders = ibi.reqCompletedOrders(False)
        resp = json.dumps(util.tree(_orders))
    return resp


@qrt.route('/trades')
async def trades():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _trades = ibi.trades()
        resp = json.dumps(util.tree(_trades))
    return resp


@qrt.route('/trades/open')
async def open_trades():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _trades = ibi.openTrades()
        resp = json.dumps(util.tree(_trades))
    return resp


@qrt.route('/fills')
async def fills():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _fills = ibi.fills()
        resp = json.dumps(util.tree(_fills))
    return resp


@qrt.route('/executions')
async def executions():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _executions = ibi.executions()
        resp = json.dumps(util.tree(_executions))
    return resp


@qrt.route('/reqMktData')
async def req_mkt_data():
    data = request.args.to_dict()
    with await IB().connectAsync(host, port, client_id) as ibi:
        ticker = ibi.reqMktData(Contract(**data))
        ib.sleep(2)
        resp = json.dumps(util.tree(ticker))
    return resp


@qrt.route('/reqHistoricalTicks')
async def req_historical_ticks():
    data = request.args.to_dict()
    start_date_time = get_and_exclude(data, 'startDateTime')
    end_date_time = get_and_exclude(data, 'endDateTime')
    number_of_ticks = to_int(get_and_exclude(data, 'numberOfTicks'))
    what_to_show = get_and_exclude(data, 'whatToShow')
    use_rth = bool(get_and_exclude(data, 'useRTH'))
    ignore_size = bool(get_and_exclude(data, 'ignoreSize'))

    with await IB().connectAsync(host, port, client_id) as ibi:
        _tickers = ibi.reqHistoricalTicks(Contract(**data), start_date_time, end_date_time, number_of_ticks,
                                          what_to_show, use_rth, ignore_size)
        ib.sleep(2)
        resp = json.dumps(util.tree(_tickers))
    return resp


@qrt.route('/reqFundamentalData')
async def req_fundamental_data():
    data = request.args.to_dict()
    report_type = get_and_exclude(data, 'reportType')
    with await IB().connectAsync(host, port, client_id) as ibi:
        fundamentals = ibi.reqFundamentalData(Contract(**data), report_type)
        ib.sleep(2)
        return fundamentals


@qrt.route('/tickers')
async def tickers():
    with await IB().connectAsync(host, port, client_id) as ibi:
        _tickers = ibi.tickers()
        resp = json.dumps(util.tree(_tickers))
    return resp


def get_and_exclude(dictionary: dict, key: str) -> Optional[str]:
    if key in dictionary:
        res = dictionary[key]
        del dictionary[key]
        return res
    else:
        return None


def to_int(value: Union[None, str]) -> Optional[int]:
    if value is None:
        return None
    else:
        return int(value)


if __name__ == '__main__':
    logger.info('Application started')
    qrt.run(host='0.0.0.0', debug=True)
