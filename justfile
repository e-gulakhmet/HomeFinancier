test-all:
  pytest tests

create-migration NAME:
  dotenv -f src/infrastructure/databases/postgresql/migrations/.env run -- dbmate new {{NAME}}

migrate:
  dotenv -f src/infrastructure/databases/postgresql/migrations/.env run -- dbmate up

rollback-migration:
  dotenv -f src/infrastructure/databases/postgresql/migrations/.env run -- dbmate down
