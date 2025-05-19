FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
RUN mkdir -p /app/staticfiles
