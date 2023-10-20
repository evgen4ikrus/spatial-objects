# spatial-objects

Клонируйте репозиторий:
```shell
git clone https://github.com/evgen4ikrus/spatial-objects.git
```
Скачайте и соберите докер-образы с помощью Docker-Сompose:
```shell
docker-compose build
``` 
Запустите докер-контейнеры:
``` shell
docker compose up
```
В новом терминале накатите свежие миграции БД:
```shell
docker-compose run --rm web-app sh -c "python manage.py migrate"
```
Вход в админку находится по адресу http://127.0.0.1:8000/admin/
