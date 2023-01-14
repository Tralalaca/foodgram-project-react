![example workflow](https://github.com/Tralalaca/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Foodgram - помощник по поиску вкусного обеда, завтрака или ужина. Удобная система скачивания списка продуктов для рицептов, а так же самим публиковать свои рицепты.

### Технологии
Django, React, Django Reset Framework, NGINX, Gunicorn, PostgreSQL

### Запуск проекта через докер

Кронирование репозитория

```
git clone git@github.com:Tralalaca/foodgram-project-react.git
```

Запуск докер контейнера

```
cd infra
docker-compose up
```

Миграции и загрузка ингредиентов и тегов

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
docker-compose exec backend python manage.py load
```

### Запуск проекта на сервере 

Кронирование репозитория

```
git clone git@github.com:Tralalaca/foodgram-project-react.git
```

Передаём файл из /infra  default.conf, docker-compose.yml

```
scp foodgram-project-react/infra/  default.conf {имя сервера}@{хост}:/home/{имя сервера}
scp foodgram-project-react/infra/  docker-compose.yml {имя сервера}@{хост}:/home/{имя сервера}
```
Создаём файл .env

```
touch .env 
nano .env
```
Заполнеть файл .env свои данными

```
DB_ENGINE='django.db.backends.postgresql'
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=db
DB_PORT='5432'
```


Сервер для подключения

```
 http://158.160.3.131/recipes
```
