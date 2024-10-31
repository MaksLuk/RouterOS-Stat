import argparse
import logging
import threading
import uvicorn

from web import WebApp
from schedule import Scheduler
from utils.utils import (
    parse_address_url_string, check_period_correct,
    get_database, check_server_port_correct
)


logging.basicConfig(
    level=logging.INFO, filename='log.log', filemode='a',
    format='%(asctime)s %(levelname)s %(message)s'
)

parser = argparse.ArgumentParser(
    prog='RouterOsStat',
    description='Periodically receiving RouterOS statistics',
)
parser.add_argument('-a', '--address')
parser.add_argument('-p', '--period')
parser.add_argument('-db', '--db')
parser.add_argument('-sp', '--serverport')

args = parser.parse_args()
router, router_data = parse_address_url_string(args.address)
if not check_period_correct(args.period):
    raise TypeError(
        'Период должен соответствовать паттерну число[s|m|h|d]'
    )
if not check_server_port_correct(args.serverport):
    raise TypeError(
        'Указан неверный порт для веб-приложения'
    )
db = get_database(args.db)


if __name__ == '__main__':
    web_app = WebApp(db)
    schedule_app = Scheduler(router, router_data, db, args.period)

    threading.Thread(target=schedule_app.app.run).start()
    uvicorn.run(web_app.app, host="0.0.0.0", port=int(args.serverport))
