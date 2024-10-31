from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime
from typing import Optional, Any

from db import Database
from router_os_stats import StatDict
from utils.types import (
    CurrentDataDict, HistoricalData, HistoricalDataDict, InterfacesData
)


class Interface(SQLModel, table=True):
    ''' Таблица интерфейсов '''
    id: int = Field(primary_key=True)
    name: str
    mac_address: str
    type: str
    mtu: int


class Stat(SQLModel, table=True):
    ''' Таблица данных '''
    # id тут по-сути не нужен, но он обязателен в sqlmodel
    # можно составной первичный ключ сделать из time и interface_id
    # кстати time можно тоже выделить в отдельную таблицу для экономии места
    id: Optional[int] = Field(default=None, primary_key=True)
    time: datetime = Field(default_factory=lambda: datetime.now())
    interface_id: int = Field(foreign_key="interface.id")
    status: bool
    actual_mtu: int
    last_link_up_time: datetime | None
    sended_bytes: int
    received_bytes: int
    sended_packets: int
    received_packets: int
    tx_bits_per_second: int
    rx_bits_per_second: int
    tx_packets_per_second: int
    rx_packets_per_second: int


class SQLDatabase():    # (Database):
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def update_data(self, new_data: list[StatDict]) -> None:
        ''' Добавляет запись в БД '''
        current_time = datetime.now()   # чтобы было одним у всех записей
        with Session(self.engine) as session:
            for data in new_data:
                interface_id = self._get_interface_id(session, data['name'])
                if not interface_id:
                    interface_id = self._insert_interface(session, data)
                self._add_data(session, data, interface_id, current_time)

    def _get_interface_id(self, session: Session, name: str) -> int | None:
        ''' Ищет интерфейс в БД по имени, возвращает его id либо None '''
        query = select(Interface.id).where(Interface.name == name)
        interface_id = session.exec(query).first()
        return interface_id

    def _insert_interface(self, session: Session, data: StatDict) -> int:
        ''' Добавляет интерфейс в БД, возвращает его id '''
        new_interface = Interface(
            name=data['name'],
            mac_address=data['mac_address'],
            type=data['type'],
            mtu=data['mtu']
        )
        session.add(new_interface)
        session.commit()
        session.refresh(new_interface)
        return new_interface.id

    def _add_data(
        self, session: Session, data: StatDict,
        interface_id: int, current_time: datetime
    ) -> None:
        ''' Добавление статистики в БД '''
        new_row = Stat(
            time=current_time,
            interface_id=interface_id,
            status=data['status'],
            actual_mtu=data['actual_mtu'],
            last_link_up_time=data['last_link_up_time'],
            sended_bytes=data['sended_bytes'],
            received_bytes=data['received_bytes'],
            sended_packets=data['sended_packets'],
            received_packets=data['received_packets'],
            tx_bits_per_second=data['tx_bits_per_second'],
            rx_bits_per_second=data['rx_bits_per_second'],
            tx_packets_per_second=data['tx_packets_per_second'],
            rx_packets_per_second=data['rx_packets_per_second']
        )
        session.add(new_row)
        session.commit()

    def get_current_data(self) -> list[CurrentDataDict]:
        ''' Возвращает текущие значения (последние из БД) '''
        with Session(self.engine) as session:
            # получение последней даты
            query = select(Stat.time).order_by(Stat.time.desc()).limit(1)
            last_time = session.exec(query).first()
            if not last_time:
                return []
            # записи с этой датой
            query = select(
                Interface.name, Interface.type,
                Stat.status, Stat.actual_mtu,
                Stat.tx_bits_per_second, Stat.rx_bits_per_second,
                Stat.tx_packets_per_second, Stat.rx_packets_per_second
            ).join(Interface).where(Stat.time == last_time)
            result = session.exec(query)
        json_result = self._objects_to_dict(result)
        return json_result

    def get_data_in_period(
        self, start_datetime: datetime, end_datetime: datetime
    ) -> list[HistoricalData]:
        ''' Возвращает данные об интерфейсах за период '''
        with Session(self.engine) as session:
            query = select(
                Interface.name, Stat.time,
                Stat.status, Stat.actual_mtu,
                Stat.sended_bytes, Stat.received_bytes,
                Stat.sended_packets, Stat.received_packets,
                Stat.tx_bits_per_second, Stat.rx_bits_per_second,
                Stat.tx_packets_per_second, Stat.rx_packets_per_second
            ).join(Interface).where(start_datetime <= Stat.time, Stat.time <= end_datetime)
            data = session.exec(query)

        grouped_data = {}   # группировка по времени
        for row in data:
            key = row.time
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(row)

        json_result = []    # преобразование к выходному типу данных
        for key in grouped_data:
            json_result.append({
                'datetime': key,
                'interfaces': self._objects_to_historical_dict(grouped_data[key])
            })

        return json_result

    def get_interfaces(self) -> list[InterfacesData]:
        ''' Возвращает данные о всех интерфейсах '''
        with Session(self.engine) as session:
            query = select(Interface)
            interfaces = session.exec(query)
            json_result = self._objects_to_interfaces_dict(interfaces)
        return json_result

    def _objects_to_dict(self, objects: Any) -> list[CurrentDataDict]:
        ''' Преобразует полученный от БД объект к формату JSON '''
        result = [{
            'name': object.name,
            'type': object.type,
            'status': object.status,
            'actual_mtu': object.actual_mtu,
            'tx_bits_per_second': object.tx_bits_per_second,
            'rx_bits_per_second': object.rx_bits_per_second,
            'tx_packets_per_second': object.tx_packets_per_second,
            'rx_packets_per_second': object.rx_packets_per_second,
        } for object in objects]
        return result

    def _objects_to_historical_dict(
        self, objects: Any
    ) -> list[HistoricalDataDict]:
        ''' Преобразует полученный от БД объект к формату JSON '''
        result = [{
            'name': object.name,
            'status': object.status,
            'actual_mtu': object.actual_mtu,
            'sended_bytes': object.sended_bytes,
            'received_bytes': object.received_bytes,
            'sended_packets': object.sended_packets,
            'received_packets': object.received_packets,
            'tx_bits_per_second': object.tx_bits_per_second,
            'rx_bits_per_second': object.rx_bits_per_second,
            'tx_packets_per_second': object.tx_packets_per_second,
            'rx_packets_per_second': object.rx_packets_per_second,
        } for object in objects]
        return result

    def _objects_to_interfaces_dict(self, objects: Any) -> list[InterfacesData]:
        ''' Преобразует полученный от БД объект к формату JSON '''
        result = [{
            'id': object.id,
            'name': object.name,
            'mac_address': object.mac_address,
            'type': object.type,
            'mtu': object.mtu,
        } for object in objects]
        return result

