FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
  make curl

RUN pip install poetry

COPY Makefile ./pyproject.toml ./poetry.lock .
COPY ./src ./src
COPY ./databases ./databases

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --only main

CMD ["make", "serve"]
