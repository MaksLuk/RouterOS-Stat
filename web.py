from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main import db
from utils.types import JsonResponse


app = FastAPI()

origins = [
    'http://localhost:5173',
    'localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/api/get_current_stat')
def get_current_stat() -> JsonResponse:
    data = db.get_current_data()
    return {
        'success': True,
        'error': None,
        'data': data
    }


@app.get('/api/get_historical_stat')
def get_historical_stat(
    start_time: str, end_time: str | datetime = datetime.now()
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
    data = db.get_data_in_period(start_time, end_time)
    return  {
        'success': True,
        'error': None,
        'data': data
    }


@app.get('/api/get_interfaces')
def get_interfaces() -> JsonResponse:
    data = db.get_interfaces()
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
