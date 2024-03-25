FROM python:3.8

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./config/requirements.txt .
RUN pip3 install -r ./requirements.txt

COPY . /usr/src/app
