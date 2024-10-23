import abc
import json
import os.path
from typing import TypeVar
from datetime import datetime

from router_os_stats import StatDict


class Database(abc.ABC):
    @abc.abstractmethod
    def write_data(data: list[StatDict]) -> None:
        ''' Записывает статистику роутера в БД '''
        pass


# Тип определяет любой класс для подключения к БД
DatabaseType = TypeVar('DatabaseType', bound=Database)


class JsonDatabase(Database):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write_data(self, new_data: list[StatDict]) -> None:
        ''' Записывает данные. Если файла БД нет - создаёт его '''
        new_data_structure = {
            'timestamp': datetime.now().strftime('%Y-%d-%m %H:%M:%S'),
            'interfaces': new_data
        }
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
            data.append(new_data_structure)
        else:
            data = [new_data_structure]

        with open(self.filename, 'w') as f:
            json.dump(data, f)
