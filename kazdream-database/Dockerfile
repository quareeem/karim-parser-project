FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update -yqq && apt-get upgrade -yqq && apt-get install -y --no-install-recommends

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt


