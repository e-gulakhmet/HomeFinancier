include .env
export $(shell sed 's/=.*//' .env)

dbmate:
	@dbmate --version 2>/dev/null || (echo "dbmate is not installed, installing..." && curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 && chmod +x /usr/local/bin/dbmate)

.PHONY: create-migration rollback-migration migrate up-test-env drop-test-env test-all serve

create-migration: dbmate
	@read -p "Enter migration name: " NAME; \
	dbmate new $$NAME

rollback-migration: dbmate
	dbmate down

migrate: dbmate
	dbmate up

serve: migrate
	poetry run python ./src/main.py

up-test-env:
	dbmate -e TEST_DATABASE_URL up

drop-test-env: dbmate
	dbmate -e TEST_DATABASE_URL drop

test-all: up-test-env
	poetry run pytest tests
	$(MAKE) drop-test-env
