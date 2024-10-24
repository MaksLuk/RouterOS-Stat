import abc
import json
import os.path
from datetime import datetime

from router_os_stats import StatDict
from utils.types import JsonDatabaseStat


class Database(abc.ABC):
    @abc.abstractmethod
    def update_data(self, data: list[StatDict]) -> None:
        ''' Обновляет статистику роутера в БД '''
        pass

    @abc.abstractmethod
    def write_data(self, data: list[StatDict]) -> None:
        ''' Записывает статистику роутера в БД, история сохраняется '''
        pass


class JsonDatabase(Database):
    def __init__(self, filename: str) -> None:
        self.filename = filename
    
    def update_data(self, new_data: list[StatDict]) -> None:
        data = self.read_data()
        for i, old_element in enumerate(data):
            for new_element in new_data:
                if old_element['name'] == new_element['name']:
                    data[i] = new_element
                    break
        self.write_data(data)

    def write_data(self, new_data: list[StatDict]) -> None:
        new_data_structure: JsonDatabaseStat = {
            'timestamp': datetime.now().strftime('%Y-%d-%m %H:%M:%S'),
            'interfaces': new_data
        }
        data = self.read_data()
        data.append(new_data_structure)
        self.write_data(data)

    def read_data(self) -> list[JsonDatabaseStat|StatDict]:
        ''' Читает данные из файла '''
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
        else:
            data = []
        return data

    def write_data(self, data: list[JsonDatabaseStat|StatDict]) -> None:
        with open(self.filename, 'w') as f:
            json.dump(data, f)
