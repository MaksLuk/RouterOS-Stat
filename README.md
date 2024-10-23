# Получение статистики из RouterOS

Запуск:
`python3 main.py routerosapi://admin:admin@localhost:8728 10s json://tests/main_test.json`

Файлы:
- main.py - точка входа в проект
- db.py - файл подключения к БД
- router_os_stats.py - файл подключения к роутеру
- utils/ - папка с утилитами (.py)
- res - скриншоты возможностей RouterOS
- tests - тесты


Подводные камни:
- rocketry не совместима с последней версией pydantic, нужен pydantic <= 1.10.13
