# Check dbmate and install it if it's not installed
dbmate:
	@dbmate --version 2>/dev/null || (echo "dbmate is not installed, installing..." && curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 && chmod +x /usr/local/bin/dbmate)

.PHONY: create-migration rollback-migration migrate up-test-env drop-test-env test-all run

create-migration: dbmate
	@read -p "Enter migration name: " NAME; \
	dbmate new $$NAME

rollback-migration: dbmate
	dbmate down

migrate: dbmate
	dbmate up

up-test-env: dbmate
	dbmate up

drop-test-env: dbmate
	dbmate drop

test-all: up-test-env
	pytest tests
	$(MAKE) drop-test-env
