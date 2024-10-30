import abc
from datetime import datetime
from router_os_stats import StatDict
from utils.types import CurrentDataDict, HistoricalData, InterfacesData


class Database(abc.ABC):
    @abc.abstractmethod
    def update_data(self, data: list[StatDict]) -> None:
        ''' Добавляет данные в БД '''

    @abc.abstractmethod
    def get_current_data(self) -> list[CurrentDataDict]:
        ''' Возвращает последние данные по интерфейсам '''

    @abc.abstractmethod
    def get_data_in_period(
        self, start_datetime: datetime, end_datetime: datetime
    ) -> list[HistoricalData]:
        ''' Возвращает данные за заданный период '''

    @abc.abstractmethod
    def get_interfaces(self) -> list[InterfacesData]:
        ''' Возвращает данные по интерфейсам '''


