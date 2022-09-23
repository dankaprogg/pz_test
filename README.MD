# Тестовое задание
## Подготовка
1) Убедитесь что у вас установлен python 3.10. 
2) Заполните .env файл по примеру .env.example.
```bash
pip install poetry # установка пакетного менеджера poetry
poetry install # установка зависимостей проекта
alembic upgrade head # миграции для БД
```
## Тестирование
```bash
poetry run pytest 
```