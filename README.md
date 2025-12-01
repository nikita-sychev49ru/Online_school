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

* CI/CD - деплой на сервер

## Предварительные требования
- Docker Desktop (для Windows/Mac) или Docker Engine + Docker Compose (для Linux)

- Git

## Запуск сервера с помощью CI/CD на виртуальной машине
#### Подготовка сервера.
Создайте виртуальную машину, подключитесь к ней.
В рамках учебного проекта сервер развернут на базе Яндекс.Cloud по адресу: http://158.160.84.167/

```
# Подключение к серверу
ssh username@server_ip

# Установка Docker
sudo apt update && sudo apt install docker.io -y

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
# Перезапустите сессию SSH
```
#### Настройка окружения
Создайте на виртуальной машине директорию для развертывания проекта
```
mkdir ~/myproject && cd ~/myproject
```
В созданной директории создайте файл .env с переменными, необходимыми для развертывания проекта:
```
cat > .env << 'EOF'
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-server-ip,localhost,127.0.0.1
STATIC_ROOT=/app/staticfiles
POSTGRES_PASSWORD=your-password
POSTGRES_USER=postgres
POSTGRES_DB=postgres
DATABASE_URL=postgres://postgres:your-password@db:5432/postgres
EOF
```
#### Настройка CI/CD и автоматический деплой

Склонируйте репозиторий проекта 
```
git clone https://github.com/nikita-sychev49ru/Online_school.git
```
В личном кабинете на GitHub в репозитории с проектом в GitHub Secrets добавьте:

* DOCKER_HUB_USERNAME - ваш логин Docker Hub

* DOCKER_HUB_ACCESS_TOKEN - токен Docker Hub

* SSH_KEY - приватный SSH ключ для доступа к серверу, указанный при создании виртуальной машины

* SSH_USER - пользователь сервера, указанный при создании виртуальной машины (например, user)

* SERVER_IP - IP адрес сервера

Сделайте в репозитории push или pull-request, это автоматически запустит тестирование, создание контейнера и деплой на ваш сервер.

#### Клонирование проекта и запуск контейнера (ручной деплой, если нужно)
```
# Копирование файлов проекта
git clone https://github.com/nikita-sychev49ru/Online_school.git ~/myproject

# Запуск приложения
cd ~/myproject && docker-compose up -d

# Проверка контейнеров
docker-compose ps

# Просмотр логов
docker-compose logs web

# Проверка доступности
curl http://your-server-ip/
```
#### Проверка работоспособности
Перейдите по IP-адресу вашего сервера


## Быстрый запуск с помощью Docker на локальной машине
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