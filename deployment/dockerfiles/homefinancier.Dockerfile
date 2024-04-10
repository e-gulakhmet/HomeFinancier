FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
  make curl

RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 && chmod +x /usr/local/bin/dbmate

RUN pip install poetry

COPY Makefile pyproject.toml poetry.lock .env .
COPY ./src ./src
COPY ./databases ./databases

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --only main

CMD ["make", "serve"]
