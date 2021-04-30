import configparser
import json
import logging.config
import nest_asyncio

from quart import Quart
from ib_insync import IB, util

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


@qrt.route('/summary')
async def summary():
    with await IB().connectAsync(host, port, client_id) as ibi:
        acct = ibi.managedAccounts()[0]
        _summary = ibi.accountSummary(acct)
        await ibi.accountSummaryEvent
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


if __name__ == '__main__':
    logger.info('Application started')
    qrt.run(host='0.0.0.0', debug=True)
