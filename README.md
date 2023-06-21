<h1>Приложение для планирования целей</h1>

<h3>Стек:</h3>
<ol>
<li>Python 3.10</li>
<li>Django 4.2.1</li>
<li>Postgres</li>
</ol>

Файл .env для локального запуска:<br>
<code>SECRET_KEY=django-insecure-b2@k1g=@@ebvl#b1%rhe+_ixuc+s5(7hn_po8tgp(_*gz7g5c=<br>
DEBUG=True<br>
POSTGRES_USER=postgres<br>
POSTGRES_PASSWORD=postgres<br>
POSTGRES_DB=postgres<br>
DB_HOST=postgres<br>
DB_PORT=5432</code>

Команда для локального запуска запуска (из корня проекта):<br>
<code>docker compose -f docker-compose-dev.yaml up -d --build</code>