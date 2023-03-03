[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat&logo=FastAPI&logoColor=ffffff&color=043A6B)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&logo=SQLAlchemy&logoColor=ffffff&color=043A6B)](https://pypi.org/project/SQLAlchemy/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat&logo=Alembic&logoColor=ffffff&color=043A6B)](https://pypi.org/project/alembic/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?style=flat&logo=Pydantic&logoColor=ffffff&color=043A6B)](https://pypi.org/project/pydantic/)
[![Asyncio](https://img.shields.io/badge/-Asyncio-464646?style=flat&logo=Asyncio&logoColor=ffffff&color=043A6B)](https://docs.python.org/3/library/asyncio.html)

# QRkot | Сat сharity fund

## Описание

Учебный проект для изучения работы во фреймворке FastAPI.

**QRkot** - это API Благотворительного фонда поддержки котиков. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.


## Возможности
В сервисе реализована возможность регистрации пользователей, добавления благотворительных проектов и пожертвований, которые распределяются по открытым проектам.

Настроено автоматическое создание первого суперпользователя при запуске проекта.

## Установка
1. Склонируйте репозиторий:
```
git clone git@github.com:Hastred45/cat_charity_fund.git
```
2. Активируйте venv и установите зависимости:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Создайте в корневой директории файл .env со следующим наполнением:
```
APP_TITLE=Приложение QRKot.
DESCRIPTION=Спасем котиков вместе!
DATABASE_URL=sqlite+aiosqlite:///./<название базы данных>.db
SECRET=<секретное слово>
FIRST_SUPERUSER_EMAIL=<email суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль суперюзера>
```
4. Примените миграции для создания базы данных SQLite:
```
alembic upgrade head
```
5. Проект готов к запуску.

## Управление:
Для локального запуска выполните команду:
```
uvicorn app.main:app --reload
```
Сервис будет запущен и доступен по следующим адресам:
- http://127.0.0.1:8000 - API
- http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger
- http://127.0.0.1:8000/redoc - автоматически сгенерированная документация ReDoc

После запуска доступны следующие эндпоинты:
- Регистрация и аутентификация:
    - **/auth/register** - регистрация пользователя
    - **/auth/jwt/login** - аутентификация пользователя (получение jwt-токена)
    - **/auth/jwt/logout** - выход (сброс jwt-токена)
- Пользователи:
    - **/users/me** - получение и изменение данных аутентифицированного пользователя
    - **/users/{id}** - получение и изменение данных пользователя по id
- Благотворительные проекты:
    - **/charity_project/** - получение списка проектов и создание нового
    - **/charity_project/{project_id}** - изменение и удаление существующего проекта
- Пожертвования:
    - **/donation/** - получение списка всех пожертвований и создание пожертвования
    - **/donation/my** - получение списка всех пожертвований аутентифицированного пользователя

## Примеры API запросов

### Благотворительные проекты

#### 1. Получение списка всех проектов:
GET-запрос /charity_project/

*Доступно всем пользователям*

> Ответ:
>```json
>[    
>    {
>       "name": "string",
>       "description": "string",
>       "full_amount": 0,
>       "id": 0,
>       "invested_amount": 0,
>       "fully_invested": true,
>       "create_date": "2019-08-24T14:15:22Z",
>       "close_date": "2019-08-24T14:15:22Z"
>    }
>]
>```

#### 2. Создание благотворительного проекта:
POST-запрос /charity_project/

*Обязательные поля*: **name**, **description**, **full_amount**

*Только для суперюзеров*

> Тело запроса:
>```json
>{
>    "name": "string",
>    "description": "string",
>    "full_amount": 0
>}
>```

> Ответ:
>```json
>{
>   "name": "string",
>   "description": "string",
>   "full_amount": 0,
>   "id": 0,
>   "invested_amount": 0,
>   "fully_invested": true,
>   "create_date": "2019-08-24T14:15:22Z",
>   "close_date": "2019-08-24T14:15:22Z"
>}
>```

#### 3. Удаление благотворительного проекта:
DELETE-запрос /charity_project/{project_id}

*Обязательный path-параметр*: **project_id**

*Только для суперюзеров*

> Ответ:
>```json
>{
>   "name": "string",
>   "description": "string",
>   "full_amount": 0,
>   "id": 0,
>   "invested_amount": 0,
>   "fully_invested": true,
>   "create_date": "2019-08-24T14:15:22Z",
>   "close_date": "2019-08-24T14:15:22Z"
>}
>```

#### 4. Обновление благотворительного проекта:
PATCH-запрос /charity_project/{project_id}

*Обязательный path-параметр*: **project_id**

*Только для суперюзеров*

> Тело запроса:
>```json
>{
>    "name": "string",
>    "description": "string",
>    "full_amount": 0
>}
>```

> Ответ:
>```json
>{
>    "name": "string",
>    "description": "string",
>    "full_amount": 0,
>    "id": 0,
>    "invested_amount": 0,
>    "fully_invested": true,
>    "create_date": "2019-08-24T14:15:22Z",
>    "close_date": "2019-08-24T14:15:22Z"
>}
>```

### Пожертвования
#### 1. Получение всех пожертвований:
GET-запрос /donation/

*Только для суперюзеров*

> Ответ:
>```json
>[    
>    {
>        "full_amount": 0,
>        "comment": "string",
>        "id": 0,
>        "create_date": "2019-08-24T14:15:22Z",
>        "user_id": 0,
>        "invested_amount": 0,
>        "fully_invested": true,
>        "close_date": "2019-08-24T14:15:22Z"
>    }
>]
>```

#### 2. Создание пожертвования:
POST-запрос /donation/

*Обязательные поля*: **full_amount**

*Только для авторизованных пользователей*

> Тело запроса:
>```json
>{
>    "full_amount": 0,
>    "comment": "string"
>}
>```

> Ответ:
>```json
>{
>   
>    "full_amount": 0,
>    "comment": "string",
>    "id": 0,
>    "create_date": "2019-08-24T14:15:22Z"
>}
>```

#### 3. Получение всех пожертвований конкретного пользователя:
GET-запрос /donation/my

*Только для авторизованных пользователей*

> Ответ:
>```json
>[    
>    {
>        "full_amount": 0,
>        "comment": "string",
>        "id": 0,
>        "create_date": "2019-08-24T14:15:22Z"
>    }
>]
>```

### Регистрация и аутентификация

#### 1. Регистрация пользователя:
POST-запрос /auth/register

> Тело запроса:
>```json
>{  
>    "email": "user@example.com",
>    "password": "string",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

> Ответ:
>```json
>{
>    "id": null,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 2. Аутентификация:
POST-запрос /auth/jwt/login

*Обязательные поля*: **username**, **password**

> Тело запроса:
>```json
>{  
>    "username": "user",
>    "password": "password",
>}
>```

> Ответ:
>```json
>{
>    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9yJ1c2VyX2lkIjoiOTIyMWZmYzktNjQ",
>    "token_type": "bearer"
>}
>```

#### 3. Разлогинивание:
POST-запрос /auth/jwt/logout

## Пользователи

В проекте реализована возможность автоматического создания суперпользователя.

### Примеры API запросов

#### 1. Текущий пользователь:
GET-запрос /users/me

*Только для авторизованных*

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 2. Изменить свои данные:
PATCH-запрос /users/me

*Только для авторизованных пользователей*

> Тело запроса:
>```json
>{
>    "password": "string",
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": true,
>    "is_verified": true
>}
>```

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 3. Получить пользователя по ID:
GET-запрос /donation/my

*Обязательный path-параметр*: **id**
*Только для авторизованных пользователей*

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 4. Удаление пользователя:
GET-запрос /users/{id}

Функция удаления пользователей не предусмотрена. Необходимо деактивировать пользователей.

#### 5. Изменить данные конкретного пользователя:
PATCH-запрос /users/{id}

*Только для авторизованных пользователей*

> Тело запроса:
>```json
>{
>    "password": "string",
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": true,
>    "is_verified": true
>}
>```

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```