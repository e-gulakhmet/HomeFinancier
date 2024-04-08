FROM python:3.12-slim

ARG DATABASE_URL

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
  curl

RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 \
  && chmod +x /usr/local/bin/dbmate

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --only main

# Run migrations
RUN dbmate up
# Run the application
CMD ["python", "src/main.py"]
