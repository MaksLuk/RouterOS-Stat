import json
import os.path
from datetime import datetime

from db import Database
from router_os_stats import StatDict
from utils.types import CurrentDataDict, HistoricalData


class JsonDatabase(Database):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def update_data(self, new_data: list[StatDict]) -> None:
        data = self._read_data()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in new_data:
            i['time'] = current_time
            data.append(i)
        self._save_data(data)

    def get_current_data(self) -> list[CurrentDataDict]:
        data = self._read_data()
        last_time = data[-1]['time']
        result = [i for i in data if i['time'] == last_time]
        for i in range(len(result)):    # удаление лишних данных
            del result[i]['time']
            del result[i]['mac_address']
            del result[i]['mtu']
            del result[i]['last_link_up_time']
            del result[i]['sended_bytes']
            del result[i]['received_bytes']
            del result[i]['sended_packets']
            del result[i]['received_packets']
        return result

    def get_data_in_period(
        self, start_datetime: datetime, end_datetime: datetime
    ) -> list[HistoricalData]:
        data = self._read_data()
        start_datetime = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        end_datetime = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
        filtered_data = [
            i for i in data if start_datetime <= i['time'] <= end_datetime
        ]

        grouped_data = {}   # группировка по времени
        for row in filtered_data:
            key = row['time']
            del row['time']
            del row['mac_address']
            del row['mtu']
            del row['last_link_up_time']
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(row)

        json_result = []    # преобразование к выходному типу данных
        for key in grouped_data:
            json_result.append({
                'datetime': key,
                'interfaces': grouped_data[key]
            })

        return json_result

    def get_interfaces(self) -> dict[str: str]:
        return {'error': 'Метод не поддерживается в выбранной БД'}

    def _read_data(self) -> list[StatDict]:
        ''' Читает данные из файла '''
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
        else:
            data = []
        return data

    def _save_data(self, data: list[StatDict]) -> None:
        ''' Сохраняет данные в файл '''
        with open(self.filename, 'w') as f:
            json.dump(data, f)
