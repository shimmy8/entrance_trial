FROM python:3.11

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install poetry

# disable virtual env, install system-wide
RUN poetry config virtualenvs.create false

RUN poetry install --no-root
