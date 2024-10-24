from typing import TypedDict


class StatDict(TypedDict):
    ''' Тип данных для функции получения статистики с роутера '''
    name: str
    mac_address: str
    type: str
    status: bool
    mtu: int
    actual_mtu: int
    last_link_up_time: int
    sended_bytes: int
    received_bytes: int
    sended_packets: int
    received_packets: int
    tx_bits_per_second: int
    rx_bits_per_second: int
    tx_packets_per_second: int
    rx_packets_per_second: int


class JsonDatabaseStat(TypedDict):
    ''' Тип данных для сохранения исторических данных в JSON-бд '''
    timestamp: str
    interfaces: list[StatDict]
