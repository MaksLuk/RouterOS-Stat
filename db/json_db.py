import json
import os.path

from db import Database
from router_os_stats import StatDict


class JsonDatabase(Database):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def update_data(self, new_data: list[StatDict]) -> None:
        data: list[StatDict] = self.read_data()
        for i, old_element in enumerate(data):
            for new_element in new_data:
                if old_element['name'] == new_element['name']:
                    data[i] = new_element
                    break
        self._save_data(data)

    def read_data(self) -> list[StatDict]:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
        else:
            data = []
        return data

    def _save_data(self, data: list[StatDict]) -> None:
        with open(self.filename, 'w') as f:
            json.dump(data, f)