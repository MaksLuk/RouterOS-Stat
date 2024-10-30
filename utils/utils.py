import re
import os.path
import urllib

from router_os_stats import RouterOsApiStat
from db import JsonDatabase, SQLDatabase, Database
from utils.types import MyParseResult


def parse_address_url_string(
        address: str
    ) -> tuple[type[RouterOsApiStat], MyParseResult]:
    ''' 
    Принимает на вход строку формата protocol://username:password@url:port
    И возвращает объект роутера и словарь данных для подключения к нему
    '''
    address_object = urllib.parse.urlparse(address)
    if address_object.port is None:
        raise TypeError(
            'Не указан порт'
        )
    if address_object.port is None:
        raise TypeError(
            'Не указан ip'
        )
    
    if address_object.scheme == 'routerosapi':
        # не создаю объект, так как метод получения данных статический
        router_object = RouterOsApiStat
    else:
        raise TypeError(
            'Указан некорректный протокол. Доступные протоколы: routerosapi'
        )
    
    address_object: MyParseResult = {
        'hostname': address_object.hostname,
        'port': address_object.port,
        'username': address_object.username,
        'password': address_object.password,
    }

    return router_object, address_object


def check_period_correct(period: str) -> bool:
    ''' Проверяет, корректно ли введён период '''
    pattern = r'\d+[smhd]{1}$'
    return bool(re.match(pattern, period))


def get_database(db_string: str) -> Database:
    '''
    Проверяет, корректно ли введён параметр базы данных,
    возвращает объект БД
    '''
    db_data = urllib.parse.urlparse(db_string)
    if db_data.scheme == 'json':
        # в случае с json бд может не существовать, получаем путь до файла
        if db_data.hostname is None:
            raise TypeError('Указан некорректный путь до БД')
        if db_data.path is None:
            db_data.path = ''
        path = db_data.hostname + db_data.path
        db_path_dir = os.path.dirname(path)
        if not db_path_dir:
            db_path_dir = '.'
        if not os.path.exists(db_path_dir):
            raise TypeError('Указан некорректный путь до БД')
        return JsonDatabase(path)
    else:
        try:
            return SQLDatabase(db_string)
        except Exception as e:
            raise TypeError(
                f'Указан некорректный адрес базы данных. Ошибка: {e}'
            )


def check_server_port_correct(period: str) -> bool:
    ''' Проверяет, корректно ли введён порт '''
    return period.isdigit()
