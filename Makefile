# Create project
start_proj:
    django-admin startproject exchange_api

# Create new app inside all project
cr_app:
    ./manage.py startapp currency_exchange

migrate_doc:
    sudo docker-compose exec web python manage.py migrate --noinput

connect_db:
    sudo docker-compose exec db psql --username=ilya --dbname=movie

run:
    ./manage.py runserver

# Create createsuperuser
cr_sup:
    sudo docker exec -it exchange_api_web_1 python manage.py createsuperuser

mm:
    sudo docker-compose exec web python manage.py makemigrations
migrate:
    sudo docker-compose exec web python manage.py migrate

seed_db:
    sudo docker-compose exec web python manage.py populate_db

run_tests:
    sudo docker-compose exec web python manage.py test currency_exchange.tests

# Run celery worker
run_cel:
    sudo docker-compose exec web celery -A exchange_api worker -l INFO


run_redis:
    sudo docker run -d -p 6379:6379 redis

run_flower:
    flower -A exchange --port=5555