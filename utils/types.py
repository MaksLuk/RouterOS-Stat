from typing import TypedDict, Optional
from datetime import datetime


class StatDict(TypedDict):
    ''' Тип данных для функции получения статистики с роутера '''
    time: Optional[datetime]
    name: str
    mac_address: str
    type: str
    status: bool
    mtu: int
    actual_mtu: int
    last_link_up_time: str
    sended_bytes: int
    received_bytes: int
    sended_packets: int
    received_packets: int
    tx_bits_per_second: int
    rx_bits_per_second: int
    tx_packets_per_second: int
    rx_packets_per_second: int


class CurrentDataDict(TypedDict):
    name: str
    status: bool
    actual_mtu: int
    tx_bits_per_second: int
    rx_bits_per_second: int
    tx_packets_per_second: int
    rx_packets_per_second: int


class HistoricalDataDict(CurrentDataDict):
    sended_bytes: int
    received_bytes: int
    sended_packets: int
    received_packets: int


class HistoricalData(TypedDict):
    datetime: datetime
    interfaces: list[HistoricalDataDict]


class InterfacesData(TypedDict):
    id: int
    name: str
    mac_address: str
    type: str
    mtu: int


class JsonResponse(TypedDict):
    ''' Тип данных для отправки ответа по API '''
    success: bool
    error: str|None
    data: list[CurrentDataDict | HistoricalData | InterfacesData]


class MyParseResult(TypedDict):
    '''
    Нужен для соответствия типов у аргумента командной строки
    Убирает возможность None
    '''
    hostname: str
    port: int
    username: str
    password: str
