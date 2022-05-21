FROM python:3.8.10-alpine
# setup environment variable
WORKDIR /usr/src/exchange_api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev && apk add libffi-dev


# install dependencies
COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system --ignore-pipfile



# copy project
COPY . .