import re
import os.path
import urllib
from urllib.parse import ParseResult

from router_os_stats import RouterOsApiStat
from db import JsonDatabase, Database


def parse_address_url_string(
        address: str
    ) -> tuple[type[RouterOsApiStat], ParseResult]:
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

    return router_object, address_object


def check_period_correct(period: str) -> bool:
    ''' Проверяет, корректно ли введён период, вызывает исключение если нет '''
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

    raise TypeError('Указан некорректный протокол. Доступные протоколы: json')