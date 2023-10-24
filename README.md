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

### Задание на работу с чужим кодом:
<details>
<summary>Было так:</summary>

```python
class html_copy_to:
    ###  
    def download_source(self):
        headers = { 'User-Agent' : self.ua }

        if self.ref != '':
            o = urlparse.urlparse(self.ref)
            self.scheme = o.scheme
            self.host = o.netloc

            headers['Referer'] = self.ref

        if self.http_username != '' or self.http_password != '':
            auth = self.http_username + ':' + self.http_password
            auth = auth.encode('ascii')
            auth = base64.b64encode(auth)

            headers['Authorization'] = 'Basic ' + auth

        try:
            req = urllib2.Request(self.url, None, headers)
            r = urllib2.urlopen(req)
            h = r.info()

            if h['Content-Type'] != '' and h['Content-Type'] != None:
                if re.match('^(image|text|application)\/', h['Content-Type']) is None:
                    self.set_response('error:Invalid mime-type: ' + h['Content-Type'])
                else:
                    mime = str(re.sub('[;]([\s\S]+)$', '', h['Content-Type'])).strip().lower()
                    mime = re.sub('/x-', '/', mime)

                    if mime in self.mimes:
                        self.data = r.read()

                        extension = re.sub('^(image|text|application)\/', '', mime)
                        extension = re.sub('(windows[-]bmp|ms[-]bmp)', 'bmp', extension)
                        extension = re.sub('(svg[+]xml|svg[-]xml)', 'svg', extension)
                        extension = extension.replace('xhtml[+]xml', 'xhtml')
                        extension = extension.replace('jpeg', 'jpg')

                        self.real_extension = extension
                        self.real_mimetype  = mime

                        cp = h['Content-Type'].find(';');

                        if cp != -1:
                            cp = cp + 1
                            charset = h['Content-Type']
                            self.real_charset = ';' + charset[cp:].strip()

                        self.save_file()
                    else:
                        self.set_response('error:Invalid mime-type: ' + h['Content-Type'])
            else:
                self.set_response('error:No mime-type defined')

            r.close()
        except urllib2.URLError, e:
            self.set_response('error:SOCKET: ' + str(e.reason))
```

</details>

<details>
<summary>Изменил на:</summary>

```python
class HTMLCopyTo:
    ###
    def download_source(self):
        headers = {'User-Agent': self.user_agent}

        if self.ref:
            parsed_ref = urlparse.urlparse(self.ref)
            self.scheme = parsed_ref.scheme
            self.host = parsed_ref.netloc
            headers['Referer'] = self.ref

        if self.http_username and self.http_password:
            raw_auth = '{}:{}'.format(self.http_username, self.http_password)
            auth = base64.b64encode(raw_auth.encode('ascii'))
            headers['Authorization'] = 'Basic {}'.format(auth)

        response = None
        try:
            request = urllib2.Request(self.url, None, headers)
            response = urllib2.urlopen(request)
            header = response.info()

            if not header['Content-Type']:
                self.set_response('error:No mime-type defined')
                return

            mime, params = cgi.parse_header(header['Content-Type'])

            if mime not in self.mimes:
                self.set_response('error:Invalid mime-type: {}'.format(header["Content-Type"]))
                return

            if params.get('charset'):
                self.real_charset = 'charset={}'.format(params.get('charset'))

            self.data = response.read()
            self.real_extension = mimetypes.guess_extension(mime, strict=True)
            self.real_mimetype = mime

            self.save_file()

        except urllib2.URLError as err:
            self.set_response('error:SOCKET: {}'.format(str(e.reason)))

        finally:
            if response:
                response.close()
```

</details>
