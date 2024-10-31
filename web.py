from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.types import CurrentStatResponse, HistoricalResponse, InterfacesResponse


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

    def get_current_stat(self) -> CurrentStatResponse:
        data = self.db.get_current_data()
        return {
            'success': True,
            'error': None,
            'data': data
        }

    def get_historical_stat(
        self, start_time: datetime, end_time: datetime = datetime.now()
    ) -> HistoricalResponse:
        data = self.db.get_data_in_period(start_time, end_time)
        return  {
            'success': True,
            'error': None,
            'data': data
        }

    def get_interfaces(self) -> InterfacesResponse:
        data = self.db.get_interfaces()
        if type(data) == dict and data.get('error'):
            return {
                'success': False,
                'error': data['error'],
                'data': []
            }
        return {
            'success': True,
            'error': None,
            'data': data
        }
