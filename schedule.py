from rocketry import Rocketry
from rocketry.conds import every
import logging


class Scheduler:
    def __init__(self, router, router_data, db, period):
        self.db = db
        self.app = Rocketry()
        
        self.app.task(
            every(period),
            func=self.write_data,
            parameters={'router': router, 'router_data': router_data}
        )

    def write_data(self, router, router_data) -> None:
        try:
            stat = router.get_stat(
                router_data['hostname'], router_data['port'],
                router_data['username'], router_data['password']
            )
            self.db.update_data(stat)
            logging.info('Данные записаны')
        except Exception as e:
            logging.error(e)
