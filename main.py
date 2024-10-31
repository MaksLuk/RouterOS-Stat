import argparse
import logging
import threading

from rocketry import Rocketry
from rocketry.conds import every
import uvicorn

from web import app as web_app
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

rocketry_app = Rocketry()


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


@rocketry_app.task(every(args.period))
def write_data() -> None:
    try:
        stat = router.get_stat(
            router_data['hostname'], router_data['port'],
            router_data['username'], router_data['password']
        )
        db.update_data(stat)
        logging.info('Данные записаны')
    except Exception as e:
        logging.error(e)
    db.get_current_data()


if __name__ == '__main__':
    threading.Thread(target=rocketry_app.run).start()
    uvicorn.run(web_app, host="0.0.0.0", port=int(args.serverport))
