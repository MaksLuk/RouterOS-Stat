import re
import os.path
from typing import TypedDict

from router_os_stats import RouterType, RouterOsApiStat
from db import JsonDatabase, DatabaseType
from utils.types import AddressDict


def parse_address_url_string(address: str) -> tuple[RouterType, AddressDict]:
    ''' 
    Принимает на вход строку формата protocol://username:password@url:port
    И возвращает объект роутера и словарь данных для подключения к нему
    '''
    pattern = r'(?P<protocol>\S+)://(?P<username>\S+):(?P<password>\S+)@(?P<ip>\S+):(?P<port>\d+)$'

    match_object = re.match(pattern, address)
    if not match_object:
        raise TypeError(
            'Адрес должен соответствовать паттерну '\
            'protocol://username:password@url:port'
        )

    result = match_object.groupdict()
    result['port'] = int(result['port'])

    if result['protocol'] == 'routerosapi':
        # не создаю объект, так как метод получения данных статический
        db_object = RouterOsApiStat
    else:
        raise TypeError(
            'Указан некорректный протокол. Доступные протоколы: routerosapi'
        )
    del result['protocol']  # чтобы передавать данные как f(**data)

    return db_object, result


def check_period_correct(period: str) -> None:
    ''' Проверяет, корректно ли введён период, вызывает исключение если нет '''
    pattern = r'\d+[smhd]{1}$'
    if not re.match(pattern, period):
        raise TypeError(
            'Период должен соответствовать паттерну число[s|m|h|d]'
        )


def get_database(db_string: str) -> DatabaseType:
    '''
    Проверяет, корректно ли введён параметр базы данных,
    возвращает объект БД
    '''
    pattern = r'(?P<protocol>\S+)://(?P<path>\S+)$'
    match_object = re.match(pattern, db_string)
    if not match_object:
        raise TypeError(
            'БД должена соответствовать паттерну протокол://путь'
        )
    db_data = match_object.groupdict()

    if db_data['protocol'] == 'json':
        # в случае с json бд может не существовать, получаем путь до файла
        db_path_dir = os.path.dirname(db_data['path'])
        if not db_path_dir:
            db_path_dir = '.'
        if not os.path.exists(db_path_dir):
            raise TypeError('Указан некорректный путь до БД')
        return JsonDatabase(db_data['path'])

    raise TypeError('Указан некорректный протокол. Доступные протоколы: json')