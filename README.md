# Online_school

Этот проект предоставляет возможности для организации сайта, содержащего обучающие курсы 

## Описание
В проекте представлено веб-приложение, обеспечивающее доступ пользователей к обучающим курсам. 


## Технологии
* Django - веб-фреймворк

* PostgreSQL - база данных

* Redis - кеш и брокер сообщений

* Celery - асинхронные задачи

* Celery Beat - периодические задачи

* Docker - контейнеризация

## Предварительные требования
- Docker Desktop (для Windows/Mac) или Docker Engine + Docker Compose (для Linux)

- Git

## Быстрый запуск
Клонируйте репозиторий:

```
git clone https://github.com/nikita-sychev49ru/Online_school.git
cd Online_school
```
Создайте файл окружения:

```
cp .env.example .env
```
Отредактируйте .env файл, указав свои настройки (секретные ключи, пароли БД и т.д.)
* SECRET_KEY=...
* DEBUG=...
#### настройки базы данных
* POSTGRES_DB=...
* POSTGRES_USER=...
* POSTGRES_PASSWORD=...
* POSTGRES_HOST=...
* POSTGRES_PORT=...

Запустите проект:
```
docker-compose up -d --build
```
Проверьте статус сервисов:
```
docker-compose ps
```
## Проверка работоспособности сервисов
## *1. Django приложение (web)*
### Проверить логи
```
docker-compose logs web
```

### Проверить доступность
Введите в терминале:
```
curl http://localhost:8000
```
или открыть в браузере: http://localhost:8000

### Выполнить команду в контейнере
```
docker-compose exec web python manage.py check
```

## *2. База данных (db)*

### Проверить здоровье БД
```
docker-compose logs db
```
### Проверить подключение к БД
```
docker-compose exec db pg_isready -U postgres
```
### Подключиться к БД
```
docker-compose exec db psql -U postgres -d online_school
```
Выйти из подключения:
```
online_school-# /q
```

## *3. Redis*

### Проверить логи Redis
```
docker-compose logs redis
```
### Проверить подключение к Redis
```
docker-compose exec redis redis-cli ping
```
Должен ответить: PONG


## *4. Celery Worker*

### Проверить логи Celery
```
docker-compose logs celery
```
### Проверить подключения воркера
```
docker-compose exec celery celery -A config.celery_app inspect ping
```
Должен ответить: pong


## *5. Celery Beat*

### Проверить логи Beat на наличие ошибок
```
docker-compose logs beat --tail=50
```


## Тестирование

В рамках проекта реализовано тестирование эндпойнтов с помощью unittest. 


## Зависимости

Проект использует следующие зависимости:

*   Python 3.13
*   Poetry (для управления зависимостями)
*   django (>=5.2.4,<6.0.0)
*   psycopg2-binary (>=2.9.10,<3.0.0)
*   pillow (>=11.3.0,<12.0.0)


## Лицензия

[Университет SkyPro](https://sky.pro/)