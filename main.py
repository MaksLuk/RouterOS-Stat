import argparse
import logging
import threading

from rocketry import Rocketry
from rocketry.conds import every
from fastapi import FastAPI
import uvicorn

from router_os_stats import Stat
from db import Database
from utils.utils import (
    parse_address_url_string, check_period_correct, get_database
)
from utils.types import MyParseResult, JsonResponse


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

rocketry_app = Rocketry()
web_app = FastAPI()


args = parser.parse_args()
router, router_data = parse_address_url_string(args.address)
if not check_period_correct(args.period):
    raise TypeError(
        'Период должен соответствовать паттерну число[s|m|h|d]'
    )
db = get_database(args.db)


@rocketry_app.task(every(args.period))
def write_data() -> None:
    try:
        stat = router.get_stat(
            router_data.hostname, router_data.port,
            router_data.username, router_data.password
        )
        db.update_data(stat)
        logging.info('Данные записаны')
    except Exception as e:
        logging.error(e)


@web_app.get('/api/get_stat')
def get_stat() -> JsonResponse:
    data = db.read_data()
    if data:
        return {
            'success': True,
            'error': None,
            'interfaces': data
        }
    return {
        'success': False,
        'error': 'Нет данных',
        'interfaces': []
    }


if __name__ == '__main__':
    threading.Thread(target=rocketry_app.run).start()
    uvicorn.run(web_app, host="0.0.0.0", port=8000)
