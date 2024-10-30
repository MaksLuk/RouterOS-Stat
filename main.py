import argparse
import logging
import threading
from datetime import datetime

from rocketry import Rocketry
from rocketry.conds import every
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from utils.utils import (
    parse_address_url_string, check_period_correct,
    get_database, check_server_port_correct
)
from utils.types import JsonResponse, CurrentDataDict, HistoricalData


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
web_app = FastAPI()


origins = [
    'http://localhost:5173',
    'localhost:5173'
]

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


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


@web_app.get('/api/get_current_stat')
def get_current_stat() -> JsonResponse:
    data = db.get_current_data()
    return {
        'success': True,
        'error': None,
        'data': data
    }


@web_app.get('/api/get_historical_stat')
def get_historical_stat(
    start_time: str, end_time: str | datetime = datetime.now()
) -> JsonResponse:
    try:
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    except:
        return {
            'success': False,
            'error': 'Неверно указана начальная дата. ' \
                'Используйте формат %Y-%m-%dT%H:%M:%S',
            'data': []
        }
    if type(end_time) == str:
        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        except:
            return {
                'success': False,
                'error': 'Неверно указана конечная дата. ' \
                    'Используйте формат %Y-%m-%dT%H:%M:%S',
                'data': []
            }
    data = db.get_data_in_period(start_time, end_time)
    return  {
        'success': True,
        'error': None,
        'data': data
    }


@web_app.get('/api/get_interfaces')
def get_interfaces() -> JsonResponse:
    data = db.get_interfaces()
    if type(data) == dict and data.get('error'):
        return {
            'success': False,
            'error': data['error'],
            'data': []
        }
    return {
        'success': True,
        'error': None,
        'data': data
    }


if __name__ == '__main__':
    threading.Thread(target=rocketry_app.run).start()
    uvicorn.run(web_app, host="0.0.0.0", port=int(args.serverport))
