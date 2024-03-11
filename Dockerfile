FROM python:3.11-slim-bullseye
WORKDIR /api
COPY ./ ./
RUN apt-get update \
  && apt-get upgrade -y \
  && pip install -U pip \
  && pip install poetry \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
RUN pip install -r ./app/requirements.txt
ENV PYTHONPATH=/app
ENV LANG ja_JP.UTF-8
