# Create project
start_proj:
    django-admin startproject exchange_api

# Create new app inside all project
cr_app:
    ./manage.py startapp currency_exchange

connect_db:
    sudo docker-compose exec db psql --username=ilya --dbname=currency

run:
    ./manage.py runserver

# Create createsuperuser
cr_sup:
    sudo docker exec -it exchange_api_web_1 python manage.py createsuperuser

# make migrations (create migration file)

mm:
    sudo docker-compose exec web python manage.py makemigrations

# apply migrations
migrate:
    sudo docker-compose exec web python manage.py migrate

# Run tests
run_tests:
    sudo docker-compose exec web python manage.py test currency_exchange.tests

# Run celery worker in docker container
run_cel:
    sudo docker-compose exec web celery -A exchange_api worker -l INFO

# Run redis in docker
run_redis:
    sudo docker run -d -p 6379:6379 redis

# Run flowe for celery tasks
run_flower:
    flower -A exchange_api --port=5555

# Create dump data:

dump:
    sudo docker-compose exec web python manage.py dumpdata > testdata.json