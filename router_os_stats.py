import abc
from typing import TypeVar
from routeros_api import RouterOsApiPool
import ros_api

from utils.types import StatDict


class Stat(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_stat(
        cls, ip: str, port: int, username: str, password: str
    ) -> list[StatDict]:
        '''
        Возвращает данные об интерфейсах:
        - Название, тип, статус (работает ли)
        - MTU, MAC-адрес, время последней передачи
        - Переданные и полученные пакеты/байты с момента последней перезагрузки роутера
        - Текущая скорость передачи данных
        Возвращает часть данных, получаемых через API
        Все доступные атрибуты API есть в папке res
        '''

    @staticmethod
    def _create_interface_dict(
        data: dict[str, str], traffic_data: dict[str, str]
    ) -> StatDict:
        ''' Преобразует данные об интерфейсе в словарь StatDict '''
        result = {
            'name': data['name'],
            'mac_address': data['mac-address'],
            'type': data['type'],
            'status': data['running'] == 'true',
            'mtu': int(data['mtu']),
            'actual_mtu': int(data.get('actual-mtu', 0)),
            'last_link_up_time': data['last-link-up-time'],
            'sended_bytes': int(data['tx-byte']),
            'received_bytes': int(data['rx-byte']),
            'sended_packets': int(data['tx-packet']),
            'received_packets': int(data['rx-packet']),
            'tx_bits_per_second': int(traffic_data['tx-bits-per-second']),
            'rx_bits_per_second': int(traffic_data['rx-bits-per-second']),
            'tx_packets_per_second': int(traffic_data['tx-packets-per-second']),
            'rx_packets_per_second': int(traffic_data['rx-packets-per-second']),
        }
        return result


# Тип определяет любой класс для подключения к роутеру
RouterType = TypeVar('RouterType', bound=Stat)


class RouterOsApiStat(Stat):
    @classmethod
    def get_stat(
        cls, ip: str, port: int, username: str, password: str
    ) -> list[StatDict]:
        connection = RouterOsApiPool(
            ip,
            username=username,
            password=password,
            port=port,
            plaintext_login=True
        )
        router = connection.get_api()

        result = []
        interfaces_data = router.get_resource('/interface')

        for interface in interfaces_data.get():
            traffic_data = interfaces_data.call(
                'monitor-traffic',
                {'interface': interface['name'], 'once': ''}
            )
            data = cls._create_interface_dict(interface, traffic_data[0])
            result.append(data)

        connection.disconnect()        
        return result


class LaiartusRosApiStat(Stat):
    @classmethod
    def get_stat(
        cls, ip: str, port: int, username: str, password: str
    ) -> list[StatDict]:
        router = ros_api.Api(ip, user=username, password=password, port=port)

        result = []
        interfaces_data = router.talk('/interface/print')

        for interface in interfaces_data:
            traffic_data = router.talk(
                f'/interface/monitor-traffic\n=interface={interface["name"]} =once='
            )
            data = cls._create_interface_dict(interface, traffic_data[0])
            result.append(data)

        return result


if __name__ == '__main__':
    print('ТЕСТ RouterOsApiStat')
    data1 = RouterOsApiStat.get_stat('localhost', 8728, 'admin', 'admin')
    print(data1)

    print('ТЕСТ LaiartusRosApiStat')
    data2 = LaiartusRosApiStat.get_stat('localhost', 8728, 'admin', 'admin')
    print(data2)
    
