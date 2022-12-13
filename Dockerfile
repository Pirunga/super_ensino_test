FROM python:3.9

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update \ 
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

WORKDIR /super_ensino
COPY . /super_ensino/