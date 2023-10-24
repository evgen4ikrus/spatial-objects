# spatial-objects
Проект создан на основе тестового задания на позицию backend-developer

### Установка и запуск dev-версии проекта:
<details>
<summary>с помощью docker-compose:</summary>

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
docker-compose up
```
В новом терминале накатите свежие миграции БД:
```shell
docker-compose run --rm web-app sh -c "python manage.py migrate"
```
Создайте суперпользователя (логин и пароль пригодиться для доступа к сайту):
```shell
docker-compose run --rm web-app sh -c "python manage.py  createsuperuser"
```
Проверьте, что всё установилось успешно, перейдите по адресу в админку: http://127.0.0.1:8000/admin/

Создайте таблицы в БД:
```shell
docker-compose run --rm web-app sh -c "python manage.py create_db_tables"
```
Наполните таблицы данными из csv-файлов, которые находятся в директории `db_data`:
```shell
docker-compose run --rm web-app sh -c "python manage.py fill_db"
```

Всё готово. Перейдите по ссылке: http://127.0.0.1:8000/
</details>

<details>
<summary>без docker-compose:</summary>

Клонируйте репозиторий:
```shell
git clone https://github.com/evgen4ikrus/spatial-objects.git
```
Перейдите в директорию проекта:
```commandline
cd spatial_objects/
```
У вас уже должна быть создана БД PostgreSQL. (Если ее нет, создайте, например можете воспользоваться [инструкцией](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04))

Создайте файл .env и запишите в него переменные окружения связанные с БД в формате `KEY=VALUE` (`DB_HOST`, `DB_NAME`, 
`DB_USER`, `DB_PASSWORD`), например:
```
DB_HOST=localhost
DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=pass
```

Создайте и активируйте виртуальное окружение:
```shell
python3 -m venv venv
source venv/bin/activate
```
Установите зависимости:
```shell
pip install -r requirements.txt
```
Накатите свежие миграции БД:
```shell
python3 manage.py migrate
```
Создайте суперпользователя (логин и пароль пригодиться для доступа к сайту):
```shell
python3 manage.py  createsuperuser
```
Проверьте, что всё установилось успешно, перейдите по адресу в админку: http://127.0.0.1:8000/admin/

Создайте таблицы в БД:
```shell
python3 manage.py create_db_tables
```
Наполните таблицы данными из csv-файлов, которые находятся в директории `db_data`:
```shell
python3 manage.py fill_db
```
Запустите web-приложение:
```shell
python3 manage.py runserver
```
Всё готово. Перейдите по ссылке: http://127.0.0.1:8000/
</details>

### Скрипт find_route.py
Скрипт выводит информацию о маршрутах до центра земельного участка от переданной координаты

Для запуска через docker-compose:
```shell
docker-compose run --rm web-app sh -c "python manage.py find_route <land_plot_id> <coordinate>"
# например: docker-compose run --rm web-app sh -c "python manage.py find_route 64 '46.44182986,60.323853125'"
```
без docker-compose:
```shell
python3 manage.py find_route <land_plot_id> <coordinate>
# например python3 manage.py find_route 64 '46.44182986,60.323853125'
```
