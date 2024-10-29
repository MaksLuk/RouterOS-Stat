from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime

from db import Database
from router_os_stats import StatDict


class Interface(SQLModel, table=True):
    ''' Таблица интерфейсов '''
    id: int = Field(primary_key=True)
    name: str
    mac_address: str
    type: str
    mtu: int


class Stat(SQLModel, table=True):
    ''' Таблица данных '''
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


class SQLDatabase(Database):
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url, echo=True)
        SQLModel.metadata.create_all(self.engine)

    def update_data(self, new_data: list[StatDict]) -> None:
        ''' Добавляет запись в БД '''
        with Session(self.engine) as session:
            for data in new_data:
                interface_id = self._get_interface_id(session, data['name'])
                if not interface_id:
                    interface_id = self._insert_interface(session, data)
                self._add_data(session, data)

    def _get_interface_id(self, session: Session, name: str) -> int | None:
        ''' Ищет интерфейс в БД по имени, возвращает его id либо None '''
        statement = select(Interface.id).where(Interface.name == name)
        interface_id = session.exec(statement).first()
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
        return self._get_interface_id(session, data['name'])

    def _add_data(
            self, session: Session, data: StatDict, interface_id: int
        ) -> None:
        ''' Добавление статистики в БД '''
        new_row = Stat(
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
