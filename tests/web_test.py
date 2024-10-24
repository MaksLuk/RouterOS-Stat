import requests


response = requests.get('http://127.0.0.1:8000/api/get_stat')
print(response.json())
