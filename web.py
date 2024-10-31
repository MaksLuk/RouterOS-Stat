from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.types import JsonResponse


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

    def get_current_stat(self) -> JsonResponse:
        data = self.db.get_current_data()
        return {
            'success': True,
            'error': None,
            'data': data
        }

    def get_historical_stat(
        self, start_time: str, end_time: str | datetime = datetime.now()
    ) -> JsonResponse:
        try:
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        except:
            return {
                'success': False,
                'error': 'Неверно указана начальная дата. ' \
                    'Используйте формат %Y-%m-%dT%H:%M:%S',
                'data': []
            }
        if type(end_time) == str:
            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
            except:
                return {
                    'success': False,
                    'error': 'Неверно указана конечная дата. ' \
                        'Используйте формат %Y-%m-%dT%H:%M:%S',
                    'data': []
                }
        data = self.db.get_data_in_period(start_time, end_time)
        return  {
            'success': True,
            'error': None,
            'data': data
        }

    def get_interfaces(self) -> JsonResponse:
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
