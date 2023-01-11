![example workflow](https://github.com/Tralalaca/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Foodgram - помощник по поиску вкусного обеда, завтрака или ужина. Удобная система скачивания списка продуктов для рицептов, а так же самим публиковать свои рицепты.

### Технологии
Django, React, Django Reset Framework, NGINX, Gunicorn, PostgreSQL

### Запуск проекта

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
