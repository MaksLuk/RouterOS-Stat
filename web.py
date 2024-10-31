from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.types import CurrentDataDict, HistoricalData, InterfacesData


class WebApp(FastAPI):
    def __init__(self, db):
        self.db = db
        self.app = FastAPI()

        origins = [
            'http://localhost:5173',
            'localhost:5173'
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )

        self.app.add_api_route('/api/current_stat', self.get_current_stat)
        self.app.add_api_route('/api/historical_stat', self.get_historical_stat)
        self.app.add_api_route('/api/interfaces', self.get_interfaces)

    def get_current_stat(self) -> list[CurrentDataDict]:
        data = self.db.get_current_data()
        return data

    def get_historical_stat(
        self, start_time: datetime, end_time: datetime = datetime.now()
    ) -> list[HistoricalData]:
        data = self.db.get_data_in_period(start_time, end_time)
        return data

    def get_interfaces(self) -> list[InterfacesData]:
        data = self.db.get_interfaces()
        if type(data) == dict and data.get('error'):
            raise HTTPException(status_code=400, detail=data['error'])
        return data
