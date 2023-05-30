<h1>Приложение для планирования целей</h1>

<h3>Стек:</h3>
<ol>
<li>Python 3.10</li>
<li>Django 4.2.1</li>
<li>Postgres</li>
</ol>

Файл .env для запуска:<br>
<code>SECRET_KEY=django-insecure-b2@k1g=@@ebvl#b1%rhe+_ixuc+s5(7hn_po8tgp(_*gz7g5c=<br>
DEBUG=True<br>
POSTGRES_USER=postgres<br>
POSTGRES_PASSWORD=postgres<br>
POSTGRES_DB=postgres<br>
DB_ENGINE=django.db.backends.postgresql<br>
DB_HOST=localhost<br>
DB_PORT=5432</code>

Команда для запуска БД (из корня проекта):<br>
<code>docker run --name postgresdb --env-file=.env -p 5432:5432 -d postgres<br>
(в папке todolist) python ./manage.py makemigrations<br>
python ./manage.py migrate<br>
</code>