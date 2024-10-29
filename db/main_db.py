import abc
from router_os_stats import StatDict


class Database(abc.ABC):
    @abc.abstractmethod
    def update_data(self, data: list[StatDict]) -> None:
        ''' Обновляет статистику роутера в БД '''

    @abc.abstractmethod
    def read_data(self) -> list[StatDict]:
        ''' Читает данные из БД '''

    @abc.abstractmethod
    def _save_data(self, data: list[StatDict]) -> None:
        ''' Записывает данные в БД '''


