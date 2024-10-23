import argparse
from rocketry import Rocketry
from rocketry.conds import every

from router_os_stats import RouterType
from db import DatabaseType
from utils.types import AddressDict
from utils.utils import (
    parse_address_url_string, check_period_correct, get_database
)


parser = argparse.ArgumentParser(
    prog='RouterOsStat',
    description='Periodically receiving RouterOS statistics',
)
parser.add_argument('address')
parser.add_argument('period')
parser.add_argument('db')

app = Rocketry()


def write_data(
    router: RouterType, router_data: AddressDict, db: DatabaseType
) -> None:
    stat = router.get_stat(**router_data)
    db.write_data(stat)


def main() -> None:
    args = parser.parse_args()
    router, router_data = parse_address_url_string(args.address)
    check_period_correct(args.period)
    db = get_database(args.db)

    app.task(
        every(args.period),
        func=write_data,
        parameters={'router': router, 'router_data': router_data, 'db': db}
    )


if __name__ == '__main__':
    main()
    app.run()
