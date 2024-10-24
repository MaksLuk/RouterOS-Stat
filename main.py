import argparse
from rocketry import Rocketry
from rocketry.conds import every
from urllib.parse import ParseResult
import logging

from router_os_stats import Stat
from db import Database
from utils.utils import (
    parse_address_url_string, check_period_correct, get_database
)


parser = argparse.ArgumentParser(
    prog='RouterOsStat',
    description='Periodically receiving RouterOS statistics',
)
# сделать именованные параметры
parser.add_argument('-a', '--address')
parser.add_argument('-p', '--period')
parser.add_argument('-db', '--db')

app = Rocketry()


def write_data(
    router: Stat, router_data: ParseResult, db: Database
) -> None:
    try:
        stat = router.get_stat(
            router_data.hostname, router_data.port,
            router_data.username, router_data.password
        )
        db.update_data(stat)
        logging.info('Данные записаны')
    except Exception as e:
        logging.error(e)


def main() -> None:
    args = parser.parse_args()
    router, router_data = parse_address_url_string(args.address)
    if not check_period_correct(args.period):
        raise TypeError(
            'Период должен соответствовать паттерну число[s|m|h|d]'
        )
    db = get_database(args.db)
    #db.update_data(stat)

    app.task(
        every(args.period),
        func=write_data,
        parameters={'router': router, 'router_data': router_data, 'db': db}
    )
    app.run()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, filename='log.log', filemode='a',
        format='%(asctime)s %(levelname)s %(message)s'
    )
    main()
