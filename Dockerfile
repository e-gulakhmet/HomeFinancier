FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install poetry

# Copy the project files into the working directory
COPY . .

# Install project dependencies
run poetry config virtualenvs.create false \
  && poetry install --no-root --only main

# Run the application
CMD ["python", "src/main.py"]
